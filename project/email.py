from flask import request, current_app, Blueprint
from cloudevents.http import from_http
import smtplib
from email.message import EmailMessage


bp = Blueprint("email", __name__)


@bp.route("/", methods=["POST"])
def receiveEvent():
    event = from_http(request.headers, request.get_data())
    current_app.logger.info(
        "Received CloudEvent of type %s and data %s", event["type"], event.data
    )
    recipient = event.data['parameters']['email']
    deployment = event.data['deployment']
    algorithmExecution = event.data['algorithmExecution']
    level = event.data['level']
    rawResult = event.data['rawResult']
    message = "Deployment: {}\nAlgorithm Execution: {}\nLevel: {}\nRaw result: {}".format(
        deployment, algorithmExecution, level, rawResult)
    notifyUser(message, recipient)
    return "ok"


def notifyUser(message, recipient):
    msg = EmailMessage()
    msg['subject'] = 'Panoptes notification'
    msg['From'] = 'panoptes@bt.com'
    msg['To'] = recipient
    msg.set_content(message)

    try:
        smtpObj = smtplib.SMTP(host='smtp.intra.bt.com', port=25)
        smtpObj.send_message(msg)
        smtpObj.quit()
        current_app.logger.info("Successfully sent email")
    except smtplib.SMTPException as e:
        print(type(e).__name__, e.args)

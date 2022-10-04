import pytest
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_structured
from project import create_app


@pytest.fixture
def app():
    return create_app()


def test_random_type(app):
    attributes = {
        "source": "from-galaxy-far-far-away",
        "type": "cloudevent.greet.you",
    }

    data = {
        "deployment": "testDeployment",
        "algorithmExecution": "testAlgorithmExecution",
        "level": 1,
        "rawResult": 0.05,
        "parameters": {"email": "panagiotis.kourouklidis@bt.com"}
    }

    event = CloudEvent(attributes, data)
    headers, data = to_structured(event)

    with app.test_client() as test_client:

        response = test_client.post("/", data=data, headers=headers)
        assert response.status_code == 200

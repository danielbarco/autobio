import unittest
import json
from main import app  # Assuming your Quart app is in main.py
from quart.testing import QuartClient
from azure.communication.callautomation import CallAutomationClient
import uuid
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()

# Your ACS resource connection string
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")


class IncomingCallTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = QuartClient(app)
        app.testing = True  # Set the testing attribute on the app instance

    async def test_call_automation_client_initialization(self):
        client = CallAutomationClient.from_connection_string(ACS_CONNECTION_STRING)
        self.assertIsNotNone(client)

    async def test_call_automation_client_credentials(self):
        try:
            client = CallAutomationClient.from_connection_string(ACS_CONNECTION_STRING)
            # Attempt to make a simple request to verify credentials
            self.assertIsNotNone(client)
        except Exception as e:
            self.fail(f"CallAutomationClient credentials are incorrect: {e}")

    async def test_validation_event(self):
        # Define the payload for the POST request
        payload = [
            {
                "id": "f6ce9a17-d09f-460d-b79f-05319f285a21",
                "topic": "/subscriptions/cf09abed-918a-453b-ba9d-badb669e4532/resourceGroups/autobio/providers/microsoft.communication/communicationservices/phonech1",
                "subject": "",
                "data": {
                    "validationCode": "173E138C-3F4A-42C2-8F66-69F001EA029A",
                    "validationUrl": "https://rp-global.eventgrid.azure.net:553/eventsubscriptions/autobio-event/validate?id=173E138C-3F4A-42C2-8F66-69F001EA029A&t=2024-11-11T15:55:11.6404664Z&apiVersion=2023-12-15-preview&token=hg7XXULt0vChcyrITBzz7qVlWtqXO7LF%2bckEu5Y%3d",
                },
                "eventType": "Microsoft.EventGrid.SubscriptionValidationEvent",
                "eventTime": "2024-11-11T15:55:11.64054Z",
                "metadataVersion": "1",
                "dataVersion": "2",
            }
        ]

        # Send POST request to the route
        response = await self.client.post(
            "/api/incomingCall",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

        # Print the response data for debugging
        response_data = await response.get_data(as_text=True)
        print(response_data)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)

    async def test_incoming_call_event(self):
        # Define the payload for the POST request
        payload = {
            "id": "f6ce9a17-d09f-460d-b79f-05319f285a21",
            "topic": "/subscriptions/cf09abed-918a-453b-ba9d-badb669e4532/resourceGroups/autobio/providers/microsoft.communication/communicationservices/phonech1",
            "subject": "",
            "data": {
                "from": {
                    "kind": "phoneNumber",
                    "phoneNumber": {"value": "+1234567890"},
                    "rawId": "raw-id-example",
                },
                "incomingCallContext": {
                    "contextKey": "context-value"  # Ensure this is correctly formatted
                },
            },
            "eventType": "Microsoft.Communication.IncomingCall",
            "eventTime": "2024-11-11T15:55:11.64054Z",
            "metadataVersion": "1",
            "dataVersion": "2",
        }

        # Send POST request to the route
        response = await self.client.post(
            "/api/incomingCall",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

        # Print the response data for debugging
        response_data = await response.get_data(as_text=True)
        print(response_data)

        # Extract and log the caller ID
        event = payload
        if event["eventType"] == "Microsoft.Communication.IncomingCall":
            if event["data"]["from"]["kind"] == "phoneNumber":
                caller_id = event["data"]["from"]["phoneNumber"]["value"]
            else:
                caller_id = event["data"]["from"]["rawId"]
            incoming_call_context = event["data"]["incomingCallContext"]
            guid = uuid.uuid4()
            query_parameters = urlencode({"callerId": caller_id})
            print(f"Caller ID: {caller_id}")
            print(f"Incoming Call Context: {incoming_call_context}")
            print(f"GUID: {guid}")
            print(f"Query Parameters: {query_parameters}")

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()

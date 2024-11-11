import unittest
import requests
import uuid
from urllib.parse import urlencode


class IncomingCallTestCase(unittest.TestCase):
    def test_incoming_call(self):
        # Define the Dev Tunnel URL
        dev_tunnel_url = "https://sj2f46dh.euw.devtunnels.ms:8080/api/incomingCall"

        # Define the payload for the POST request
        payload = [
            {
                "id": "f6ce9a17-d09f-460d-b79f-05319f285a21",
                "topic": "/subscriptions/cf09abed-918a-453b-ba9d-badb669e4532/resourceGroups/autobio/providers/microsoft.communication/communicationservices/phonech1",
                "subject": "",
                "data": {
                    "validationCode": "173E138C-3F4A-42C2-8F66-69F001EA029A",
                    "validationUrl": "https://rp-global.eventgrid.azure.net:553/eventsubscriptions/autobio-event/validate?id=173E138C-3F4A-42C2-8F66-69F001EA029A&t=2024-11-11T15:55:11.6404664Z&apiVersion=2023-12-15-preview&token=hg7XXULt0AYvChcyrITBzz7qVl52WtqXO7LF%2bckEu5Y%3d",
                },
                "eventType": "Microsoft.EventGrid.SubscriptionValidationEvent",
                "eventTime": "2024-11-11T15:55:11.64054Z",
                "metadataVersion": "1",
                "dataVersion": "2",
            }
        ]

        # Perform the HTTP POST request
        response = requests.post(
            dev_tunnel_url,
            json=payload,
        )

        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_incoming_call_event(self):
        # Define the Dev Tunnel URL
        dev_tunnel_url = "https://sj2f46dh.euw.devtunnels.ms:8080/api/incomingCall"

        # Define the payload for the POST request
        payload = [
            {
                "id": "f6ce9a17-d09f-460d-b79f-05319f285a21",
                "topic": "/subscriptions/cf09abed-918a-453b-ba9d-badb669e4532/resourceGroups/autobio/providers/microsoft.communication/communicationservices/phonech1",
                "subject": "",
                "data": {
                    "from": {
                        "kind": "phoneNumber",
                        "phoneNumber": {"value": "+1234567890"},
                        "rawId": "raw-id-example",
                    },
                    "incomingCallContext": "context-example",
                },
                "eventType": "Microsoft.Communication.IncomingCall",
                "eventTime": "2024-11-11T15:55:11.64054Z",
                "metadataVersion": "1",
                "dataVersion": "2",
            }
        ]

        # Perform the HTTP POST request
        response = requests.post(
            dev_tunnel_url,
            json=payload,
        )

        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        # Extract and log the caller ID
        event = payload[0]
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

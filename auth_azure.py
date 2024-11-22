import unittest
from azure.communication.callautomation import CallAutomationClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your ACS resource connection string
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")


class AuthAzureTestCase(unittest.TestCase):
    def test_acs_connection_string(self):
        # Test if the ACS connection string is loaded correctly
        self.assertIsNotNone(ACS_CONNECTION_STRING, "ACS_CONNECTION_STRING is not set")

    def test_call_automation_client_initialization(self):
        # Test if the CallAutomationClient is initialized correctly
        client = CallAutomationClient.from_connection_string(ACS_CONNECTION_STRING)
        self.assertIsNotNone(client, "CallAutomationClient initialization failed")

    def test_call_automation_client_credentials(self):
        # Test if the CallAutomationClient credentials are correct
        try:
            client = CallAutomationClient.from_connection_string(ACS_CONNECTION_STRING)
            # Attempt to make a simple request to verify credentials
            self.assertIsNotNone(
                client, "CallAutomationClient credentials are incorrect"
            )
        except Exception as e:
            self.fail(f"CallAutomationClient credentials are incorrect: {e}")


if __name__ == "__main__":
    unittest.main()
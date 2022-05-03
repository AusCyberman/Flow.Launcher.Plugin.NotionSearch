"""Notion search plugin for Flow Launcher"""

import webbrowser
import logging
from flowlauncher import FlowLauncher
from notional.session import SessionError
from . helper import NOTION_ICON, GITHUB_URL
from . helper import error_messages
from . helper import session_test, results_processor, show_msg

logging.basicConfig(level=logging.INFO)


class NotionSearch(FlowLauncher):
    """The main class for the plugin"""

    def query(self, query):
        """Search method using using the notional package."""

        user_settings = self.rpc_request.get("settings", {})

        try:  # Check if the user has a token in settings
            token = self.settings_test(user_settings)
        except self.SettingsError as error_message:
            flow_msg = show_msg(error_message, "SettingsException")
            return flow_msg
        try:  # Check if the token is accepted by the Notion API
            client = session_test(token)
        except SessionError as error_message:
            flow_msg = show_msg(error_message, "SessionException")
            return flow_msg
        return results_processor(query, client)


    class SettingsError(Exception):
        """Raised when Notion API token is not found."""


    def settings_test(self, user_settings):
        """Check if the user has a token in settings."""

        if token := user_settings.get("notion_token"):
            logging.info("Integration token found.")
            return token
        raise self.SettingsError(error_messages["SettingsException"]["SysMsg"])


    def context_menu(self, data):
        """Placeholder for context menu."""
        return [
            {
                "Title": "Placeholder context menu",
                "SubTitle": "Press enter to visit the Notion search plugin GitHub repository.",
                "IcoPath": NOTION_ICON,
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": [GITHUB_URL]
                }
            },
        ]


    def open_url(self, url):
        """Open a URL in the default browser."""
        webbrowser.open(url)


if __name__ == "__main__":
    NotionSearch()

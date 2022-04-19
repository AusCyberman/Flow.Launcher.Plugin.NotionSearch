import webbrowser
import logging
import sys
import os
import requests

from flowlauncher import FlowLauncher
from notion_client import Client, APIErrorCode, APIResponseError
from helper import process_result


class NotionSearch(FlowLauncher):

    def query(self, query):

        settings = self.rpc_request.get("settings", {})

        # Check if the user has set an integration token
        try:
            NOTION_TOKEN = settings.get("notion_token")
            if not NOTION_TOKEN:
                raise Exception("No token found")
        except Exception as e:
            logging.error(e)

            return [{
                "Title": "Notion integration token not found.",
                "SubTitle": "Please set the token in the settings of the plugin in the flow launcher application.",
                "IcoPath": "Images/notion.png",
                "JsonRPCAction": {
                    "method": "Flow.Launcher.OpenSettingDialog",
                    "parameters": []
                }
            }]

        try:
            # Initialize the client with the token
            notion = Client(auth=NOTION_TOKEN)

            # Query notion API
            api_results = notion.search(query=query).get("results")

            # If the request has errors, return an error message
            # TODO: Check if the error is a 404 or a 401 so that empty results can be returned
            if not api_results:
                raise Exception("No results returned")
        except Exception as e:
            logging.error(e)

            return [{
                "Title": "Notion API returned an error.",
                "SubTitle": "Check that your integration token is valid in the settings of the plugin in the flow launcher application.",
                "IcoPath": "Images/notion.png",
                "JsonRPCAction": {
                    "method": "Flow.Launcher.OpenSettingDialog",
                    "parameters": []
                }
            }]

        return [process_result(result) for result in api_results]

    def context_menu(self, data):
        return [
            {
                "Title": "Copy link",
                "SubTitle": "Press enter to copy the link to this page",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
                }
            },
            {
                "Title": "Open in browser",
                "SubTitle": "Press enter to open this page in your browser",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython"]
                }
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    NotionSearch()
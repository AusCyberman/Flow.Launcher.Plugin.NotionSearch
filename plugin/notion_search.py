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

        # Get user defined notion token from plugin settings in the flow launcher application
        NOTION_TOKEN = settings.get("notion_token")
        # Initialize the client with the token
        notion = Client(auth=NOTION_TOKEN)

        # Query notion API
        api_results = notion.search(query=query).get("results")

        # Process the results with the helper function
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
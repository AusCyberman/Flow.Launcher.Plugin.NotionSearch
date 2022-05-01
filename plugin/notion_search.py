import notional
import webbrowser
import logging

from flowlauncher import FlowLauncher
from notion_client import Client, APIErrorCode, APIResponseError
from notional.query import SortDirection, TimestampKind

logging.basicConfig(level=logging.INFO)

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
        # Check if the integration token is valid
        try:
            notion = Client(auth=NOTION_TOKEN)
            api_results = notion.search(query=query).get("results")
            # If the request is 'APIResponseError: API token is invalid' raise an exception.
            if isinstance(api_results, APIResponseError) and api_results.code == APIErrorCode.INVALID_TOKEN:
                raise Exception("Invalid token")
        except Exception as e:
            logging.error(e)
            return [{
                "Title": "Invalid Notion token",
                "SubTitle": "Check the integration token in the settings of the plugin in the flow launcher application.",
                "IcoPath": "Images/notion.png",
                "JsonRPCAction": {
                    "method": "Flow.Launcher.OpenSettingDialog",
                    "parameters": []
                }
            }]
        # Notional wrapper for the Notion Python SDK
        auth_token = NOTION_TOKEN
        notion = notional.connect(auth=auth_token)
        query = notion.search(query).sort(
            timestamp=TimestampKind.LAST_EDITED_TIME, direction=SortDirection.ASCENDING
        )
        results = []
        for result in query.execute():
            title = result.Title
            url = result.url
            last_edited_time = result.last_edited_time
            parent = result.parent
            results_dict = {"Title": title, "SubTitle": f'Notion TYPE',
                            "IcoPath": "Images/notion.png", 
                            "JsonRPCAction": 
                                {"method": "open_url", "parameters": [url]}}
            results.append(results_dict)
        return results


    def context_menu(self, data):
        return [
            {
                "Title": "Placeholder context menu",
                "SubTitle": "Press enter to visit the GitHub repository for this plugin",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://github.com/danielduckworth/Flow.Launcher.Plugin.NotionSearch"]
                }
            },
        ]


    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    NotionSearch()

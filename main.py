# -*- coding: utf-8 -*-

import webbrowser
import logging
import sys
import os

from lib.flowlauncher import FlowLauncher
from lib.notion_client import Client, APIErrorCode, APIResponseError

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

class NotionSearch(FlowLauncher):

    def query(self, query):

        self.logger
        try:
                self.settings.get('notion_token', '')
                if self.settings.get('notion_token') is None or self.settings.get('notion_token') == '':
                    self.settings['notion_token'] = str(self.notion_token)
        except Exception:
                self.add_item(
                    title="Notion token not found",
                    subtitle="Please set a notion token in the settings",
                    method=self.open_setting_dialog,
                    icon="Images\\notion-black.svg"
                )
                return

        NOTION_TOKEN = self.settings['notion_token']

        # Initialize the client with the token
        notion = Client(auth=NOTION_TOKEN)

        api_results = notion.search(query=query).get("results")
        results = []

        for result in api_results:
            result_icon = result['icon']
            # Check if the result has an icon
            result_icon_bool = result_icon is not None
            # Check if the result has an emoji icon
            result_icon_emoji_bool = result_icon_bool and result_icon['type'] == 'emoji'
            # Check if the result has an external icon
            result_icon_external_bool = result_icon_bool and result_icon['type'] == 'external'
            result_id = result['id']
            result_last_edited_time = result['last_edited_time']
            result_object = result['object']
            result_parent = result['parent']
            result_parent_name = notion.databases.retrieve(
                database_id=result_parent['database_id'])['title'][0]['plain_text']
            result_title = result['properties']['\ufeffName']['title'][0]['plain_text']
            result_url = result['url']

            results.append(
                {
                    "Title": result_title,
                    "SubTitle": f"Notion {result_object} in {result_parent_name}",
                    "IcoPath": result_icon['emoji'] if result_icon_emoji_bool else result_icon['external']['url'] if result_icon_external_bool else None,
                    "JsonRPCAction":
                    {"method":
                     "open_url", "parameters": [result_url]
                     }
                }
            )

        return results

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

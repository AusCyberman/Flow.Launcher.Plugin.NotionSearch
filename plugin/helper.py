"""Global variables and helper functions."""

import logging
from datetime import datetime
import notional
from notional.query import SortDirection, TimestampKind
from notional.session import SessionError


NOTION_ICON = "Images/notion.png"
GITHUB_URL = "https://github.com/danielduckworth/Flow.Launcher.Plugin.NotionSearch"
NOTION_URL = "https://www.notion.so/help/create-integrations-with-the-notion-api"


default_rpc = {
    "Title": "",
    "SubTitle": "",
    "IcoPath": NOTION_ICON,
    "JsonRPCAction": {
                "method": "",
                "parameters": []
    }
}
error_messages = {
    "SettingsException": {
        "SysMsg": "Integration token not found",
        "UsrMsg": "Press enter to open the Notion integration settings webpage."
    },
    "SessionException": {
        "SysMsg": "Integration token is invalid",
        "UsrMsg": "Press enter to open Flow Launcher settings."
    }
}


def session_test(token):
    """Check if token is accepted by the Notion API."""

    client = notional.connect(auth=token)
    if client.ping() is True:
        logging.info("API token is valid.")
        return client
    raise SessionError


def show_msg(error_message, arg):
    """Show error message to the user."""

    logging.error(error_message)

    flow_msg = default_rpc.copy()
    flow_msg["Title"] = f"{str(error_message)} ☹️"
    flow_msg["SubTitle"] = error_messages[arg]["UsrMsg"]
    if arg == "SettingsException":
        flow_msg["JsonRPCAction"]["method"] = "open_url"
        flow_msg["JsonRPCAction"]["parameters"] = [NOTION_URL]
    elif arg == "SessionException":
        flow_msg["JsonRPCAction"]["method"] = "Flow.Launcher.OpenSettingDialog"
    return [flow_msg]


def results_processor(query, client):
    """Process the raw results from the Notion search."""

    data = client.search(query).sort(
        timestamp=TimestampKind.LAST_EDITED_TIME,
        direction=SortDirection.ASCENDING
    )
    logging.info("Processing results.")
    results = []
    for result in data.execute():
        obj_type = result.dict()["object"]
        url = result.url
        title = result.Title
        icon = result.icon
        if icon is not None:
            icon = icon.dict()
            emoji = icon.get("emoji")
            title = f"{emoji} {title}"
        last_edited_time = result.last_edited_time
        delta = edit_delta(last_edited_time)
        #parent = result.parent
        results_dict = {"Title": f"{title}",
                        "SubTitle": f"Notion {obj_type} | last edited {delta}",
                        "IcoPath": "Images/notion.png",
                        "JsonRPCAction": {"method": "open_url", "parameters": [url]}}
        results.append(results_dict)
    return results


def edit_delta(last_edited_time: datetime):    # sourcery skip: aware-datetime-for-utc
    """
    Takes a date time object and returns a string representing the time since the last edit.
    """

    last_edited_time = last_edited_time.replace(tzinfo=None)
    time_now = datetime.utcnow()
    delta_seconds = int((time_now - last_edited_time).seconds)
    delta_minutes = delta_seconds // 60
    delta_hours = delta_minutes // 60
    delta_days = (time_now - last_edited_time).days

    if delta_seconds < 60:
        return "just now"
    elif delta_minutes < 60:
        return f"{delta_minutes} minutes ago"
    elif delta_hours < 24:
        return f"{delta_hours} hours ago"
    elif delta_days < 2:
        return "yesterday"
    else:
        return f"{delta_days} days ago"

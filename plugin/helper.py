def result_processor(result):

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
    result_parent_name = notion.databases.retrieve(database_id=result_parent['database_id'])['title'][0]['plain_text']
    result_title = result['properties']['\ufeffName']['title'][0]['plain_text']
    result_url = result['url']

    return {
        "Title": result_title,
        "SubTitle": f"Notion {result_object} in {result_parent_name}",
        "IcoPath": result_icon['emoji'] if result_icon_emoji_bool else result_icon['external']['url'] if result_icon_external_bool else None,
        "JsonRPCAction":
        {"method":
         "open_url", "parameters": [result_url]
         }
    }

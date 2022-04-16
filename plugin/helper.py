def process_result(result):

    # Check the object type
    object_type = result.get("object")

    if object_type == "page":
        title = result['properties']['Name']['title'][0]['plain_text']
    elif object_type == "database":
        title = result['title'][0]['plain_text']
    else:
        title = None

    return {
                "Title": title,
                "SubTitle": f"Notion {object_type}",
                "IcoPath": "Images/notion.png",
                "JsonRPCAction": {
                    "method": "open_url",
                    "parameters": [result['url']]
                }
            }
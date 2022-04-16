def process_result(result):

    # Check the object type
    object_type = result.get("object")

    if object_type == "page":
        title = result['properties']['Name']['title'][0]['plain_text']
    else:
        title = result['title'][0]['plain_text']

    return {
        "Title": title,
        "SubTtitle": f"Notion {object_type}",
        "IcoPath": "Images\\notion-black.svg",
        "JsonRPCAction":
        {
            "method": "open_url", 
            "parameters": result['url']
            }}
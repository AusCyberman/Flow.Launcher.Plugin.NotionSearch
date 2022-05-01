# Notion search Flow Launcher plugin 🔍

The Notion search plugin for Flow Launcher searches for pages and databases in a Notion workspace.

Install the plugin in Flow Launcher using the plugin manager hotkey, `pm install Notion Search`.

## Prerequisites

- 🔌[A Notion integration](notion.com/my-integrations) and integration token (**See Notion's docs**: [Create integrations with the Notion API](notion.so/help/create-integrations-with-the-notion-api)).
- 👀 The integration needs to be configured with read content permission.
- 🔑 The integration must be added to at least one page in the Notion work space using the Share settings (**See Notion's docs**: [Add integrations to pages](notion.so/help/add-and-manage-integrations-with-the-api#add-integrations-to-pages)).

## Feature ideas

- Integrate semantic search to improve on keyword matching with [Haystack](https://github.com/deepset-ai/haystack).
- Add context menu actions for querying databases, editing properties etc.

## References

- [Python Hello World Flow Launcher template](https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython).
- [Unofficial Notion SDK Rewrite in Python, notion-sdk-py](https://ramnes.github.io/notion-sdk-py/).
- [A high level interface and object model for the Notion SDK, Notional](https://jheddings.github.io/notional/).

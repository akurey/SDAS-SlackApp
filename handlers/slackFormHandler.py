import json
from handlers.jsonDataHandler import get_project_list, get_actions


def add_options(property):
    options = []
    for index in range(len(property)):
        options.append({"text": {"type": "plain_text", "text": str(property[index])}, "value": str(index)})
    return options


FORM_HANDLER = {
    "type": 'modal',
    "title": {
        "type": 'plain_text',
        "text": 'PUF'
    },
    "callback_id": 'SSOTRequest',
    "submit": {
        "type": 'plain_text',
        "text": 'Submit'
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":memo: Single source of truth update"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Projects"
                },
                "options": add_options(get_project_list()),
                "action_id": "projectSelect"
            },
            "label": {
                "type": "plain_text",
                "text": "Project name"
            }
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Actions"
                },
                "options": add_options(get_actions()),
                "action_id": "actionSelect"
            },
            "label": {
                "type": "plain_text",
                "text": "Action type",
                
            }
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "notesAction",
                "multiline": True
            },
            "label": {
                "type": "plain_text",
                "text": "Description (optional)",
                
            },
            "optional": True
        },
        {
            "type": "divider"
        },
        {
            "type": "input",
            "optional": True,
            "element": {
                "type": "multi_conversations_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select conversations",
                    
                },
                "action_id": "conversationsAction"
            },
            "label": {
                "type": "plain_text",
                "text": "Additional notification to: ",
                
            }
        }
    ]
}

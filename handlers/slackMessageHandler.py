from handlers.jsonDataHandler import get_project_list, get_actions


def get_image_section(image_list, message_block):
    if image_list:
        for image in image_list:
            image_property = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'<{image["url"]}|{image["name"]}>'
                },
                "accessory": {
                    "type": "image",
                    "image_url": image['url'],
                    "alt_text": image['name']
                }
            }
            message_block.append(image_property);
    return message_block


def get_message_block(username, project_id, action_id, notes, message, image_list):
    project = get_project_list()[int(project_id)]
    action_type = get_actions()[int(action_id)]
    message_block = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":triangular_flag_on_post:PUF",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f':mega:*UPDATE FROM:* {username}\n:desktop_computer:*PROJECT:* {project}\n:rocket:*ACTION TYPE:* {action_type}\n:mag_right:*MESSAGE:*\n{message}\n:crystal_ball:*ADDITIONAL NOTES:*\n{notes}'
            },
            "accessory": {
                "type": "image",
                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/approvalsNewDevice.png",
                "alt_text": "computer thumbnail"
            }
        }
    ]
    return get_image_section(image_list, message_block)

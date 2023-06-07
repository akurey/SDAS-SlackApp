import os
import datetime
import re
from slack.errors import SlackApiError
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_bolt.adapter.aws_lambda.lambda_s3_oauth_flow import LambdaS3OAuthFlow

from handlers.slackFormHandler import FORM_HANDLER
from handlers.slackMessageHandler import get_message_block
from handlers.jsonDataHandler import get_specific_action, get_emails, get_channels

message_text = ""
image_list = []


# Initializes app with bot token and signing secret
app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


def find_object_property(obj, prop):
    sub_objects = []
    if isinstance(obj, dict):
        for value in obj.values():
            sub_objects.append(value)
    sub_object = next((sub_obj for sub_obj in sub_objects if prop in sub_obj), None)
    return sub_object[prop]


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)


@app.shortcut("messageUpdateSSOT")
async def open_modal(ack, client, logger, body):
    await ack()

    logger.info(body)
    api_response = await client.views_open(
        trigger_id=body['trigger_id'],
        view=FORM_HANDLER
    )

    global user_id
    user_id = body['user']['id']

    if 'message' in body:
        message = body['message']

        global message_text
        message_text = body['message']['text']

        if 'files' in message:
            image_files = body['message']['files']
            global image_list
            image_list = list(
                map(lambda image_file: {"name": image_file['name'], "url": image_file['url_private']}, image_files))

    logger.info(api_response)


async def get_username(uid):
    rex = r'<@|>'
    uid = re.sub(rex, "", uid)
    username = await app.client.users_info(
        user=uid
    )
    return username['user']['real_name']


async def get_user_id_by_email(email):
    try:
        user_data = await app.client.users_lookupByEmail(email=email)
        return user_data['user']['id']
    # This error will be constantly thrown because of slack private and public channels listing bug
    except SlackApiError as error:
        print.error(error)


async def get_channel_id(channel_name, channel_type):
    try:
        channel_list = await app.client.conversations_list(types=channel_type)
        filtered_id = next((channel["id"] for channel in channel_list["channels"] if channel["name"] == channel_name),
                           None)
        return filtered_id
    except SlackApiError as error:
        # This console.error will be constantly thrown because of the slack private and public channels listing bug
        print.error(error)


async def get_conversations(conversations, project_id, action_id):
    user_emails = get_emails(project_id, action_id)
    channels = get_channels(project_id, action_id)
    conversation_list = []

    for email in user_emails:
        conversation_list.append(await get_user_id_by_email(email))
    list(map(lambda conversation: conversation_list.append(conversation), conversations))

    # This for was implemented this way since there is a known bug on the slack apy where
    # if the application has joined the channels, requesting the api
    # conversations.list with parameter: types = "private_channel,public_channel" only returns public channels
    # instead of both public and private channels
    channel_id = ""
    for channel in channels:
        channel_id = await get_channel_id(channel, "private_channel")
        if not channel_id:
            channel_id = await get_channel_id(channel, "public_channel")
        conversation_list.append(channel_id)
    filtered = list(dict.fromkeys(conversation_list))
    return filtered


async def publish_message(username, project, action, notes, conversations, message):
    try:
        message_block = get_message_block(username, project, action, notes, message, image_list);
        for conversation in conversations:
            await app.client.chat_postMessage(
                text='fallback text, check update in SSOTFile',
                blocks=message_block,
                channel=conversation)
    except SlackApiError as error:
        print.error(error)


@app.view("SSOTRequest")
async def view_submission(ack, view, logger):
    await ack()
    view_values = view['state']['values']
    project_id = find_object_property(view_values, 'projectSelect')['selected_option']['value']
    action_id = find_object_property(view_values, 'actionSelect')['selected_option']['value']
    notes = find_object_property(view_values, 'notesAction')['value']
    conversations = find_object_property(view_values, 'conversationsAction')['selected_conversations']
    username = await get_username(user_id)
    conversations = await get_conversations(conversations, project_id, action_id)
    await publish_message(username, project_id, action_id, notes, conversations, message_text)
    logger.info(view["state"]["values"])


if __name__ == "__main__":
    app.start(port=3000)

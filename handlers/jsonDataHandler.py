import json

file = open('./data.json')
data = json.load(file)


def get_project_list():
    return data['projectList']


def get_actions():
    return data['actions']


def get_specific_action(action_id):
    return data['actions'][action_id]


def get_emails(project_id, action_id):
    project_name = get_project_list()[int(project_id)].lower()
    action_type = get_actions()[int(action_id)].lower()
    notifications = data['projects'][project_name]['notifications'][action_type]
    return notifications['people']


def get_channels(project_id, action_id):
    project_name = get_project_list()[int(project_id)].lower()
    action_type = get_actions()[int(action_id)].lower()
    notifications = data['projects'][project_name]['notifications'][action_type]
    return notifications['channels']


file.close()

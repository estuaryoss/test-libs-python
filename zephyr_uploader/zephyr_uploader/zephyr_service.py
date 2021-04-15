import json

import requests

from .constants.cli_constants import CliConstants


class ZephyrService:
    def __init__(self, zephyr_config):
        self.zephyr_config = zephyr_config
        self.jira_url = zephyr_config.get(CliConstants.JIRA_URL)
        self.username = zephyr_config.get(CliConstants.USERNAME)
        self.password = zephyr_config.get(CliConstants.PASSWORD)
        self.project_key = zephyr_config.get(CliConstants.PROJECT_KEY)
        self.cycle_name = zephyr_config.get(CliConstants.TEST_CYCLE)
        self.folder_name = zephyr_config.get(CliConstants.FOLDER_NAME)
        self.version_name = zephyr_config.get(CliConstants.RELEASE_VERSION)
        self.single_update_uri = 'zapi/latest/execution/{}/execute'
        self.auth = (self.username, self.password)

    def get_zephyr_config(self):
        return self.zephyr_config

    def get_issue_by_key(self, issue_key):
        url = self.jira_url + "api/2/issue/" + issue_key

        resp = requests.get(url, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)

        return resp.json()['id']

    def create_new_execution(self, issue_id):
        cycle_id = self.get_cycle_id()
        project_id = self.get_project_id_by_key()
        version_id = self.get_version_for_project_id()
        folder_id = self.get_folder_id()

        url = self.jira_url + "zapi/latest/execution"

        post_data = json.dumps({
            "cycleId": cycle_id,
            "projectId": project_id,
            "versionId": version_id,
            "assigneeType": "assignee",
            "assignee": self.zephyr_config.get(CliConstants.USERNAME),
            "folderId": folder_id,
            "issueId": issue_id
        })

        resp = requests.post(url, data=post_data, auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)
        body = resp.json()

        return dict.keys(body)[0]

    def update_execution(self, issue_key, status_number, comment=None):
        issue_id = self.get_issue_by_key(issue_key)

        url = self.jira_url + self.single_update_uri.format(str(issue_id))

        if comment is None:
            data = {"status": status_number}
        else:
            data = {
                "status": status_number,
                "comment": comment
            }
        headers = {'content-type': 'application/json'}
        resp = requests.put(url, headers=headers, data=json.dumps(data), auth=self.auth)

        if resp.status_code != 200:
            raise Exception(resp.content)

    def get_project_id_by_key(self, project_key=None):
        if project_key is not None:
            p_key = project_key
        else:
            p_key = self.project_key

        url = self.jira_url + 'api/2/project/' + p_key

        project = requests.get(url, headers={'accept': 'application/json'}, auth=self.auth)
        return project.json()['id']

    def get_version_for_project_id(self, version_name=None, project_id=None):
        if version_name is not None:
            v_name = version_name
        else:
            v_name = self.version_name

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_by_key(self.project_key)

        url = self.jira_url + 'zapi/latest/util/versionBoard-list?projectId=' + p_id

        headers = {'accept': 'application/json'}
        project = requests.get(url, headers=headers, auth=self.auth)
        for version in project.json()['unreleasedVersions']:
            if version['label'] == v_name:
                return version['value']

    def create_test_cycle(self, cycle_name, start_date, end_date, description=None):
        url = self.jira_url + 'zapi/latest/cycle'

        version_id = self.get_version_for_project_id()
        project_id = self.get_project_by_key()

        headers = {'content-type': 'application/json'}
        new_cycle_values = json.dumps({
            "clonedCycleId": "",
            "name": cycle_name,
            "build": "",
            "environment": "",
            "description": description,
            "projectId": project_id,
            "versionId": version_id
        })
        resp = requests.post(url, data=new_cycle_values, headers=headers, auth=self.auth)

        return resp.json()['id']

    def get_cycle_id(self, cycle_name=None, project_id=None, version_id=None):
        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_by_key(self.project_key)

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.get_version_for_project_id()

        url = self.jira_url + 'zapi/latest/cycle?projectId=' + p_id + '&versionId=' + v_id
        resp = requests.get(url, auth=self.auth)
        if cycle_name is not None:
            c_name = cycle_name
        else:
            c_name = self.cycle_name
        for key, value in resp.json().items():
            try:
                if c_name.strip() == value['name'].strip():
                    return key
            except Exception as e:
                raise Exception(f'Cycle name not found {e.__str__()}')

    def delete_folder_from_cycle(self, folder_id=None):
        if folder_id is not None:
            f_id = folder_id
        else:
            f_id = self.get_folder_id()

        cycle_id = self.get_cycle_id()
        project_id = self.get_project_id_by_key()
        version_id = self.get_version_for_project_id()

        post_data = json.dumps({
            "versionId": version_id,
            "cycleId": cycle_id,
            "projectId": project_id
        })
        headers = {'content-type': 'application/json'}
        url = self.jira_url + f"zapi/latest/folder/{f_id}"
        resp = requests.delete(url, data=post_data, headers=headers, auth=self.auth)
        if resp.status_code != 200:
            raise Exception(f'Could not delete folder id {folder_id} for versionId: {version_id}, cycleId: {cycle_id}, '
                            f'projectId: {project_id}')

    def get_folder_id(self, cycle_id=None, project_id=None, version_id=None, folder_name=None):
        if cycle_id is not None:
            c_id = cycle_id
        else:
            c_id = self.get_cycle_id(self.cycle_name)

        if project_id is not None:
            p_id = project_id
        else:
            p_id = self.get_project_by_key()

        if version_id is not None:
            v_id = version_id
        else:
            v_id = self.get_version_for_project_id()

        url = self.jira_url + 'zapi/latest/cycle/' + c_id + '/folders?projectId=' + p_id + '&versionId=' + v_id

        if folder_name:
            f_name = folder_name
        else:
            f_name = self.folder_name

        resp = requests.get(url, auth=self.auth)
        for folder in resp.json():
            if folder['folderName'] == f_name:
                return folder['folderId']

    def create_folder_under_cycle(self, folder_name, cycle_name=None):
        url = self.jira_url + 'zapi/latest/folder/create'

        if cycle_name is not None:
            cycle_id = self.get_cycle_id(cycle_name)
        else:
            cycle_id = self.get_cycle_id(self.cycle_name)
        project_id = self.get_project_id_by_key()
        version_id = self.get_version_for_project_id()
        post_data = json.dumps({
            "versionId": version_id,
            "cycleId": cycle_id,
            "projectId": project_id,
            "name": folder_name
        })
        headers = {'content-type': 'application/json'}
        resp = requests.post(url, data=post_data, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            return self.get_folder_id(cycle_name, folder_name)
        else:
            raise Exception(f'Unable to create folder {resp.content}')

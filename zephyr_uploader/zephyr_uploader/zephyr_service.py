import json

import requests

from .constants.cli_constants import CliConstants


class ZephyrService:
    def __init__(self, zephyr_config):
        self.jira_url = zephyr_config.get(CliConstants.JIRA_URL)
        self.username = zephyr_config.get(CliConstants.USERNAME)
        self.password = zephyr_config.get(CliConstants.PASSWORD)
        self.project_key = zephyr_config.get(CliConstants.PROJECT_KEY)
        self.cycle_name = zephyr_config.get(CliConstants.TEST_CYCLE)
        self.folder_name = zephyr_config.get(CliConstants.FOLDER_NAME)
        self.version_name = zephyr_config.get(CliConstants.RELEASE_VERSION)
        self.executionCountUri = '/rest/zapi/latest/zql/executeSearch'
        self.singleUpdateUri = '/rest/zapi/latest/execution/id/execute'

        self.auth = (self.username, self.password)

    def get_zephyr_config(self):
        return self.get_zephyr_config()

    def _generate_issue_ids(self):
        issues = {}
        # zqlQuery = 'project="' + self.projectid + '" AND cycleName="' + self.cyclename + '" AND folderName="' + self.foldername +'"'
        url = self.jira_url + self.executionCountUri + '?zqlQuery=' + self.zqlQuery + '&maxRecords=9999'
        resp = requests.get(url, auth=self.auth)
        # import pdb; pdb.set_trace()
        resp_json = json.loads(resp.text)
        for testcase in resp_json['executions']:
            issues[testcase['issueKey']] = testcase['id']
        return (issues)

    def _get_status_number(self, status):
        if status.upper() == 'PASS':
            number = 1
        elif status.upper() == 'FAIL':
            number = 2
        elif status.upper() == 'WIP':
            number = 3
        elif status.upper() == 'BLOCKED':
            number = 4
        elif status.upper() == 'DEFERRED':
            number = 5
        elif status.upper() == 'OUT OF SCOPE':
            number = 6
        elif status.upper() == 'UNEXECUTED':
            number = 7
        else:
            number = 7
        return str(number)

    def logAttach(self, executionId, logFilePath):
        url = self.jira_url + '/rest/zapi/latest/attachment'
        filename = logFilePath.split('/')[-1]
        files = {
            'file': (filename, open(logFilePath, 'rb'), "multipart/form-data"),
        }
        headers = {
            'X-Atlassian-Token': 'nocheck',
            'Accept': 'application/json'
        }
        params = (
            ('entityId', executionId),
            ('entityType', 'execution'),
        )
        response = requests.post(url, headers=headers, params=params, files=files, auth=self.auth)
        return (response.status_code, response.content)

    def updateExecution(self, issueKey, status, logFilePath=None):
        issues = self._generate_issue_ids()
        id = issues[issueKey]
        status_number = self._get_status_number(status)
        singleUpdateUri = self.singleUpdateUri.replace('id', str(id))
        url = self.jira_url + singleUpdateUri
        data = '{"status": "' + status_number + '"}'
        headers = {'content-type': 'application/json'}
        try:
            resp = requests.put(url, headers=headers, data=data, auth=self.auth)
            if resp.status_code != 200:
                raise Exception(resp.content)
            else:
                if logFilePath:
                    resp_upload, body_upload = self.logAttach(id, logFilePath)
                    if resp_upload != 200:
                        raise Exception('Unable upload content :' + body_upload)
        except Exception as exp:
            raise Exception(str(exp))

    def get_testcases(self, label):
        testcaseKeys = []
        jira_server = self.jira_url
        project = self.project_key
        url = jira_server + '/rest/api/2/search?jql=project%20%3D%20' + project + '%20AND%20issuetype%20%3D%20Test%20AND%20labels%20%3D%20' + label
        resp2 = requests.get(url + '&maxResults=-1', auth=self.auth)
        keys = json.loads(resp2.text)['issues']
        for key in keys:
            testcaseKeys.append(key['key'])
        return (testcaseKeys)

    def get_project_by_key(self, project_key=None):
        if project_key is not None:
            p_key = project_key
        else:
            p_key = self.project_key
        url = self.jira_url + '/rest/api/2/project/' + p_key
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

        url = self.jira_url + '/rest/zapi/latest/util/versionBoard-list?projectId=' + p_id
        headers = {'accept': 'application/json'}
        project = requests.get(url, headers=headers, auth=self.auth)
        for version in project.json()['unreleasedVersions']:
            if version['label'] == v_name:
                return version['value']

    def createTestCycle(self, cycleName, startdate, endDate, description=None):
        jira_server = self.jira_url
        url = jira_server + '/rest/zapi/latest/cycle'
        versionId = self.version_id
        projectId = self.project_id
        # versionId = self.get_version_id()
        # projectId = self.get_project_id_from_project_key()

        headers = {'content-type': 'application/json'}
        newCycleValues = json.dumps({
            "clonedCycleId": "",
            "name": cycleName,
            "build": "",
            "environment": "",
            "description": description,
            "startDate": startdate,
            "endDate": endDate,
            "projectId": projectId,
            "versionId": versionId
        })
        resp = requests.post(url, data=newCycleValues, headers=headers, auth=self.auth)
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

        url = self.jira_url + '/rest/zapi/latest/cycle?projectId=' + p_id + '&versionId=' + v_id
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

    def get_folder_id(self, cycle_name=None, project_id=None, version_id=None, folder_name=None):
        if cycle_name is not None:
            c_id = self.get_cycle_id(cycle_name)
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

        if folder_name:
            f_name = folder_name
        else:
            f_name = self.folder_name

        url = self.jira_url + '/rest/zapi/latest/cycle/' + c_id + '/folders?projectId=' + p_id + '&versionId=' + v_id
        resp = requests.get(url, auth=self.auth)
        for folder in resp.json():
            if folder['folderName'] == f_name:
                return folder['folderId']

    def AddTestCasesToCycle(self, testcaseLabel, cyclename=None, folderName=None):
        if cyclename:
            cycle_id = self.get_cycle_id(cyclename)
            cyclename = cyclename
        else:
            cycle_id = self.get_cycle_id(self.cycle_name)
            cyclename = self.cycle_name
        # print ("Cycle ID : " + str(cycle_id))
        projectId = self.project_id
        folderId = ''
        if folderName:
            folderId = self.get_folder_id(cyclename, folderName)
        versionId = self.version_id
        testsToAdd = self.get_testcases(testcaseLabel)
        # import pdb;pdb.set_trace()
        jira_server = self.jira_url
        url = jira_server + '/rest/zapi/latest/execution/addTestsToCycle/'
        addTestValues = json.dumps({
            "issues": testsToAdd,
            "versionId": versionId,
            "cycleId": cycle_id,
            "projectId": projectId,
            "method": "1",
            "folderId": folderId
        })
        headers = {'content-type': 'application/json'}
        # import pdb;pdb.set_trace()
        resp = requests.post(url, data=addTestValues, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            print('Tests Added Succesfully')
        else:
            raise Exception("Tests could not be added..{}".format(resp.content))

    def bulkUpdateCompleteFolder(self, status):
        issues = self._generate_issue_ids()
        # print (issues)
        issueListString = ''
        for issueKey, issueId in issues.items():
            issueListString = issueListString + '"' + str(issueId) + '",'
        status_number = self._get_status_number(status)
        bulk_data = '{"executions":[' + issueListString[:-1] + '], "status": "' + str(status_number) + '"}'
        url = self.jira_url + self.bulkUpdateUri
        headers = {'content-type': 'application/json'}
        # import pdb;pdb.set_trace()
        try:
            resp = requests.put(url, headers=headers, data=bulk_data, auth=self.auth)
            if resp.status_code != 200:
                raise Exception(resp.content)
        except Exception as exp:
            raise Exception(str(exp))

    def Create_Folder_under_cycle(self, cyclename, folderName):
        if cyclename.lower() != self.cycle_name.lower():
            cycle_id = self.get_cycle_id(cyclename)
        else:
            cycle_id = self.get_cycle_id(self.cycle_name)
        projectId = self.project_id
        versionId = self.version_id
        jira_server = self.jira_url
        url = jira_server + '/rest/zapi/latest/folder/create'
        addTestValues = json.dumps({
            "versionId": versionId,
            "cycleId": cycle_id,
            "projectId": projectId,
            "name": folderName,
            "description": "created test folder for this cycle",
            "clonedFolderId": 1
        })
        headers = {'content-type': 'application/json'}
        resp = requests.post(url, data=addTestValues, headers=headers, auth=self.auth)
        if resp.status_code == 200:
            return (self.get_folder_id(cyclename, folderName))
        else:
            raise Exception('Unable to create Folder {}'.format(resp.content))

    def get_color(self, status):
        if status.lower() == 'pass':
            color = 'green'
        elif status.lower() == 'fail':
            color = 'red'
        elif status.lower() == 'wip':
            color = 'orange'
        elif status.lower() == 'blocked':
            color = 'lightskyblue'
        elif status.lower() == 'deferred':
            color = 'mediumpurple'
        elif status.lower() == 'out of scope':
            color = 'gold'
        else:
            color = 'darkgray'
        return color

    def GetExecutionStatus(self):
        projectId = self.project_id
        cycle_id = self.get_cycle_id(self.cycle_name)
        versionId = self.version_id
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        jira_server = self.jira_url
        url = jira_server + '/rest/zapi/latest/execution/executionsStatusCountByCycle?projectId=' + str(
            projectId) + '&versionId=' + str(versionId) + '&cycles=' + str(cycle_id)
        if self.folder_name:
            folder_id = self.get_folder_id(self.cycle_name, self.folder_name)
            url = url + '&folders=' + str(folder_id)
        resp = requests.get(url, headers=headers, auth=self.auth)
        execution_status = {}
        for status in resp.json():
            execution_status[status['statusName']] = status['statusCount']
        # print(execution_status)
        return (execution_status)

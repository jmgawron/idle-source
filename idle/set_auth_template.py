from settings.dnac_settings import BASE_URI
from idle import idle_utilities
import json


GET_FABRIC = {'uri': BASE_URI + '/v2/data/customer-facing-service/ConnectivityDomain?name=',
              'method': 'GET'}
GET_AUTH_IDS = {'uri': BASE_URI + '/v1/siteprofile?namespace=authentication',
                'method': 'GET'}
POST_FABRIC = {'uri': BASE_URI + '/v2/data/customer-facing-service/ConnectivityDomain',
              'method': 'PUT'}


def update_set_auth_template_task(task, populate_template, connector):
    get_auth_id(task, connector)
    get_fabric(task, connector)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=POST_FABRIC['uri'],
                       method=POST_FABRIC['method'])
    #task.print_jinja()


def get_auth_id(task, connector):
    response = connector.get_request(GET_AUTH_IDS['uri'])
    response_json = json.loads(response.content)
    for auth in response_json['response']:
        if task.template['authenticationTemplate'] in auth['name']:
            task.template['authenticationProfileId'] = auth['siteProfileUuid']


def get_fabric(task, connector):
    response = connector.get_request(GET_FABRIC['uri'] + task.template['fabricName'])
    response_json = json.loads(response.content)
    task.print_task()
    task.template['fabric'] = response_json['response']
    task.template['fabric'][0]['virtualNetwork'] = json.dumps(task.template['fabric'][0]['virtualNetwork'])
    task.template['fabric'][0]['isDefault'] = idle_utilities.lowercase_bool(task.template['fabric'][0]['isDefault'])
    task.template['fabric'][0]['enableMonitoring'] = idle_utilities.lowercase_bool(task.template['fabric'][0]['enableMonitoring'])
    task.template['fabric'][0]['wirelessMulticastFeature'] = idle_utilities.lowercase_bool(task.template['fabric'][0]['wirelessMulticastFeature'])


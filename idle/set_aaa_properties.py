from settings.dnac_settings import BASE_URI
from idle import idle_utilities
import json


SET_AAA_PROPERTIES = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
                      'method': 'POST'}

GET_SERVER_UUID = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
                   'method': 'GET'}


def update_set_aaa_properties_task(task, populate_template, connector):
    task.template['value'] = format_values(task)
    response = get_server_uuid(task, connector)
    response_json = json.loads(response.content)
    key_list = [task.template['endpointKey'], task.template['serverKey']]
    for i in range(0, len(key_list)):
        for server in response_json['response']:
            if key_list[i] in server['key']:
                task.template['instanceUuid'+str(i)] = server['instanceUuid']

    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=SET_AAA_PROPERTIES['uri'],
                       method=SET_AAA_PROPERTIES['method'])
    #task.print_jinja()


def get_server_uuid(task, connector):
    response = connector.get_request(GET_SERVER_UUID['uri'])
    return response


def format_values(task):
    value = {'ipAddress': task.template['ipAddress'],
             'sharedSecret': idle_utilities.check_for_null(task.template['updateSharedSecret']),
             'protocol': task.template['protocol']}
    return json.dumps(value)

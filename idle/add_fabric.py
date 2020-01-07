from settings.dnac_settings import BASE_URI
from idle import idle_utilities
import json


ADD_FABRIC = {'uri': BASE_URI + '/v2/data/customer-facing-service/ConnectivityDomain',
              'method': 'POST'}
GET_VN_CONTEXTID = {'uri': BASE_URI + '/v2/data/customer-facing-service/VirtualNetwork',
                    'method': 'GET'}


def update_add_fabric_task(task, populate_template, connector):
    get_vn_data(task, connector)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=ADD_FABRIC['uri'],
                       method=ADD_FABRIC['method'])
    #task.print_jinja()


def get_vn_data(task, connector):
    response = connector.get_request(GET_VN_CONTEXTID['uri'])
    response_json = json.loads(response.content)
    task.template['virtualNetwork'] = build_vn_template(response_json, task)


def build_vn_template(vn_data, task):
    result = []
    for vn in vn_data['response']:
        if vn['id'] in vn['namespace']:
            result.append({"name": vn['name'] + "-" + task.template['name'],
                           "isDefault": idle_utilities.lowercase_bool(vn['isDefault']),
                           "isInfra": idle_utilities.lowercase_bool(vn['isInfra']),
                           "virtualNetworkContextId": vn['virtualNetworkContextId'],
                           "type": vn['type']})
    return json.dumps(result)

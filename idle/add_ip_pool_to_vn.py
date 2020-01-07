from settings.dnac_settings import BASE_URI
from idle import idle_utilities
import json


GET_VN_DATA = {'uri': BASE_URI + '/v2/data/customer-facing-service/VirtualNetwork?name=',
               'method': 'GET'}
GET_IP_POOL_ID = {'uri': BASE_URI + '/v2/ippool/?ipPoolName=',
                  'method': 'GET'}
ADD_IP_POOL_TO_VN = {'uri': BASE_URI + '/v2/data/customer-facing-service/VirtualNetwork',
                     'method': 'PUT'}
GET_SEGMENT_DATA = {'uri': BASE_URI + '/v2/data/customer-facing-service/Segment?id=',
                    'method': 'PUT'}


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


def update_add_ip_pool_to_vn_task(task, populate_template, connector):
    try:
        get_vn_data(task, connector)
        get_segment_data(task, connector)
        get_ip_pool_id(task, connector)
        task.set_attribute(jinja=populate_template(task.task[3], task.vn_template),
                           uri=ADD_IP_POOL_TO_VN['uri'],
                           method=ADD_IP_POOL_TO_VN['method'])
    except IndexError as e:
        print("Debug:", e)
    #task.print_all()
    #task.print_jinja()


def get_vn_data(task, connector):
    response = connector.get_request(GET_VN_DATA['uri'] + task.template['virtualNetworkName'] + '-' +
                                     task.template['fabricName'])
    response_json = json.loads(response.content)
    task.set_attribute(vn_template=build_vn_template(response_json['response'][0]))


def build_vn_template(content):
    template = {'fabricOverride': [],
                'segment': content['segment'],
                'id': content['id'],
                'name': content['name'],
                'type': content['type'],
                'isDefault': idle_utilities.lowercase_bool(content['isDefault']),
                'isInfra': idle_utilities.lowercase_bool(content['isInfra']),
                'l3Instance': content['l3Instance'],
                'namespace': content['namespace'],
                'instanceId': content['instanceId'],
                'authEntityId': content['authEntityId'],
                'displayName': content['displayName'],
                'authEntityClass': content['authEntityClass'],
                'deployPending': content['deployPending'],
                'instanceVersion': content['instanceVersion'],
                'deployed': idle_utilities.lowercase_bool(content['deployed']),
                'isStale': idle_utilities.lowercase_bool(content['isStale']),
                'provisioningState': content['provisioningState'],
                'cfsChangeInfo': content['cfsChangeInfo'],
                'virtualNetworkContextId': content['virtualNetworkContextId'],
                'resourceVersion': content['resourceVersion']}
    return template


def get_segment_data(task, connector):
    for i in range(0, len(task.vn_template['segment'])):
        print(task.vn_template['segment'][i]['idRef'])
        response = connector.get_request(GET_SEGMENT_DATA['uri'] + task.vn_template['segment'][i]['idRef'])
        response_json = json.loads(response.content)['response'][0]
        seg_template = build_existing_segment_template(response_json)
        task.vn_template['segment'].append(seg_template)
    for i in range(0, int(len(task.vn_template['segment'])/2)):
        task.vn_template['segment'].pop(0)


def build_existing_segment_template(response_json):
    seg_template = {'id': response_json['id'],
                        'type': response_json['type'],
                        'name': response_json['name'],
                        'trafficType': response_json['trafficType'],
                        'ipPoolId': response_json['ipPoolId'],
                        'isFloodAndLearn': idle_utilities.lowercase_bool(response_json['isFloodAndLearn']),
                        'isApProvisioning': idle_utilities.lowercase_bool(response_json['isApProvisioning']),
                        'isDefaultEnterprise': idle_utilities.lowercase_bool(response_json['isDefaultEnterprise']),
                        'wlan': response_json['wlan'],
                        'connectivityDomain': response_json['connectivityDomain']['idRef'],
                        'vlanId': response_json['vlanId'],
                        'instanceId': response_json['instanceId'],
                        'l2Instance': response_json['l2Instance']}
    return seg_template


def get_ip_pool_id(task, connector):
    response = connector.get_request(GET_IP_POOL_ID['uri'] + task.template['ipPoolName'])
    response_json = json.loads(response.content)
    task.vn_template['segment'].append(create_segment_template(task, response_json['response'][0]))


def create_segment_template(task, response_json):
    new_segment = {'type': 'Segment',
                   'name': response_json['ipPoolCidr'].split('/')[0] + '-' + task.template['virtualNetworkName'],
                   'trafficType': task.template['trafficType'].upper(),
                   'ipPoolId': response_json['id'],
                   'isFloodAndLearn': idle_utilities.lowercase_bool(task.template['l2Extension']),
                   'isApProvisioning': idle_utilities.lowercase_bool(task.template['isApProvisioning']),
                   'isDefaultEnterprise': 'false',
                   'connectivityDomain': task.vn_template['namespace']
                   }
    return new_segment


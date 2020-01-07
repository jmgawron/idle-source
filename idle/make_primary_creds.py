from settings.dnac_settings import BASE_URI
import json

PRIMARY_CREDS = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
                 'method': 'POST'}

GET_REF_UUID = {'uri': BASE_URI + '/v1/commonsetting/global/-1?key=',
                'method': 'GET'}

GET_CRED_ID = {'uri': BASE_URI + '/v1/global-credential?credentialSubType=',
               'method': 'GET'}

SUBTYPE = {'credential_cli': 'CLI',
           'credential_snmp_v2_read': 'SNMPV2_READ_COMMUNITY',
           'credential_snmp_v2_write': 'SNMPV2_WRITE_COMMUNITY',
           'credential_snmp_v3': 'SNMPV3'}


def update_make_primary_creds_task(task, populate_template, connector):
    #get_reference_uuid(task, connector)
    task.print_all()
    get_credential_id(task, connector)
    task.set_attribute(jinja=populate_template(task.task[1], task.template),
                       uri=PRIMARY_CREDS['uri'],
                       method=PRIMARY_CREDS['method'])



def get_reference_uuid(task, connector):
    response = connector.get_request(GET_REF_UUID['uri'] + task.template['key'])
    json_response = json.loads(response.content)
    task.template['instanceUuid'] = json_response['response'][0]['instanceUuid']


def get_credential_id(task, connector):
    response = connector.get_request(GET_CRED_ID['uri'] + SUBTYPE[task.template['value'][0]['type']])
    json_response = json.loads(response.content)
    for i in range(len(json_response['response'])):
        print(json_response['response'])
        if json_response['response'][i]['description'] in task.template['profileName']:
            task.template['id'] = json_response['response'][i]['id']


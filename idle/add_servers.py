from settings.dnac_settings import BASE_URI
import json


ADD_SERVERS = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
               'method': 'POST'}


GET_SERVER_UUID = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
                   'method': 'GET'}

# TODO need to test this functionality
# TODO move AAA add to another tab to take care of need for new jinja template
def update_add_servers(task, populate_template, connector):
    response = get_server_uuid(task, connector)
    response_json = json.loads(response.content)
    for server in response_json['response']:
        if task.template['type'] in server['key']:
            task.template['instanceUuid'] = server['instanceUuid']
    task.template['value'] = new_format_value(task)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=ADD_SERVERS['uri'],
                       method=ADD_SERVERS['method'])
    #task.print_jinja()


def get_server_uuid(task, connector):
    response = connector.get_request(GET_SERVER_UUID['uri'])
    return response


def new_format_value(task):
    if task.template['type'] in ['dhcp.server', 'syslog.server', 'snmp.trap.receiver', 'ntp.server']:
        #print(task.template['instanceType'])
        # Needs to be formatted "172.17.100.13","172.17.100.11"
        split_value = task.template['ipAddress'].split(',')
        for i in range(0, len(split_value)):
            split_value[i] = split_value[i].strip()
            split_value[i] = json.dumps(split_value[i])
        return ', '.join(split_value)
    elif task.template['type'] in ['dns.server']:
        # Needs to be formatted like {"domainName":"asdna.cisco.com","primaryIpAddress":"172.17.100.13"}
        #print(task.template['instanceType'])
        if task.template['ipAddress'] is not None:
            split_value = task.template['ipAddress'].split(',')
            for i in range(0, len(split_value)):
                split_value[i] = split_value[i].strip()
            new_dns_value = {'domainName': task.template['dnsDomainName_or_neflowPort'],
                             'primaryIpAddress': split_value[0],
                             'secondaryIpAddress': split_value[1]}
            result = json.dumps(new_dns_value)
        return result
    else:
        return json.dumps(task.template['ipAddress'])


def format_value(task):
    if task.template['instanceType'] in ['ip']:
        #print(task.template['instanceType'])
        # Needs to be formatted "172.17.100.13","172.17.100.11"
        split_value = task.template['value'].split(',')
        for i in range(0, len(split_value)):
            split_value[i] = split_value[i].strip()
            split_value[i] = json.dumps(split_value[i])
        return ', '.join(split_value)
    elif task.template['instanceType'] in ['aaa']:
        # Needs to be formatted like "ipAddress":"","sharedSecret":"","protocol":""
        #print(task.template['instanceType'])
        if task.template['value'] is not None:
            split_value = task.template['value'].split(',')
            for i in range(0, len(split_value)):
                split_value[i] = split_value[i].split(':', 1)[-1]
                split_value[i] = split_value[i].strip()
            new_aaa_value = {'ipAddress': split_value[0], 'sharedSecret': split_value[1], 'protocol': split_value[2]}
            result = json.dumps(new_aaa_value)
        else:
            new_aaa_value = {'ipAddress': '', 'sharedSecret': '', 'protocol': ''}
            result = json.dumps(new_aaa_value)
        return result
    elif task.template['instanceType'] in ['netflow']:
        # Needs to be formatted link "ipAddress":"","port":""
        #print(task.template['instanceType'])
        if task.template['value'] is not None:
            split_value = task.template['value'].split(',')
            for i in range(0, len(split_value)):
                split_value[i] = split_value[i].split(':', 1)[-1]
                split_value[i] = split_value[i].strip()
            new_netflow_value = {'ipAddress': split_value[0], 'port': split_value[1]}
            result = json.dumps(new_netflow_value)
        else:
            new_netflow_value = {'ipAddress': '', 'port': ''}
            result = json.dumps(new_netflow_value)
        return result
    elif task.template['instanceType'] in ['dns']:
        # Needs to be formatted like {"domainName":"asdna.cisco.com","primaryIpAddress":"172.17.100.13"}
        #print(task.template['instanceType'])
        if task.template['value'] is not None:
            split_value = task.template['value'].split(',')
            for i in range(0, len(split_value)):
                split_value[i] = split_value[i].split(':', 1)[-1]
                split_value[i] = split_value[i].strip()
            new_dns_value = {'domainName': split_value[0], 'primaryIpAddress': split_value[1]}
            result = json.dumps(new_dns_value)
        else:
            new_dns_value = {'domainName': '', 'primaryIpAddress': ''}
            result = json.dumps(new_dns_value)
        return result
    else:
        return json.dumps(task.template['value'])

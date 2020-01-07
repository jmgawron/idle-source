from settings.dnac_settings import BASE_URI
import json


IP_POOL = {'uri': BASE_URI + '/v2/ippool/',
           'method': 'POST'
           }


def update_ip_pool_task(task, populate_template):
    formatted_task = format_ip_lists(task)
    task.set_attribute(jinja=populate_template(formatted_task.task[3], formatted_task.template),
                       uri=IP_POOL['uri'],
                       method=IP_POOL['method'])
    #task.print_all()


def format_ip_lists(task):
    split_dhcp_value = task.template['dhcpServerIps'].split(',')
    for i in range(0, len(split_dhcp_value)):
        split_dhcp_value[i] = split_dhcp_value[i].strip()
        split_dhcp_value[i] = json.dumps(split_dhcp_value[i])
    task.template['formattedDhcpIps'] = ', '.join(split_dhcp_value)
    split_dns_value = task.template['dnsServerIps'].split(',')
    for i in range(0, len(split_dhcp_value)):
        split_dns_value[i] = split_dns_value[i].strip()
        split_dns_value[i] = json.dumps(split_dns_value[i])
    task.template['formattedDnsIps'] = ', '.join(split_dns_value)
    return task

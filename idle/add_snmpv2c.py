from settings.dnac_settings import BASE_URI
from idle import idle_core

READ_SNMP = {'uri': BASE_URI + '/v1/global-credential/snmpv2-read-community',
       'method': 'POST'}

WRITE_SNMP = {'uri': BASE_URI + '/v1/global-credential/snmpv2-write-community',
       'method': 'POST'}


def update_add_snmpv2c_task(task, populate_template, inputQueue):
    check_make_primary(task, inputQueue)
    if 'read' in task.template['communityType']:
        task.set_attribute(jinja=populate_template(task.task[3], task.template),
                           uri=READ_SNMP['uri'],
                           method=READ_SNMP['method'])
    else:
        task.set_attribute(jinja=populate_template(task.task[3], task.template),
                           uri=WRITE_SNMP['uri'],
                           method=WRITE_SNMP['method'])
    #task.print_all()


def check_make_primary(task, inputQueue):
    if task.template['makePrimary']:
        if 'read' in task.template['communityType']:
            template = {'profileName': task.template['profileName'],
                        'instanceUuid': '',
                        'key': 'credential.snmp_v2_read',
                        'value': [{'objReferences': [], 'type': 'credential_snmp_v2_read', 'url': ''}],
                        'id': ''}
            reference_task = ('make_primary_creds', 'make_primary_creds.j2')
        else:
            template = {'profileName': task.template['profileName'],
                        'instanceUuid': '',
                        'key': 'credential.snmp_v2_write',
                        'value': [{'objReferences': [], 'type': 'credential_snmp_v2_write', 'url': ''}],
                        'id': ''}
            reference_task = ('make_primary_creds', 'make_primary_creds.j2')
        inputQueue.append(idle_core.DNACBuildTask(template=template, task=reference_task))

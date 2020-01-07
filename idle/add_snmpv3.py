from settings.dnac_settings import BASE_URI
from idle import idle_core

SNMPV3 = {'uri': BASE_URI + '/v1/global-credential/snmpv3',
       'method': 'POST'}


def update_add_snmpv3_task(task, populate_template, inputQueue):
    check_make_primary(task, inputQueue)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=SNMPV3['uri'],
                       method=SNMPV3['method'])
    #task.print_all()


def check_make_primary(task, inputQueue):
    if task.template['makePrimary']:
        template = {'profileName': task.template['profileName'],
                    'instanceUuid': '',
                    'key': 'credential.snmp_v3',
                    'value': [{'objReferences': [], 'type': 'credential_snmp_v3', 'url': ''}],
                    'id': ''}
        reference_task = ('make_primary_creds', 'make_primary_creds.j2')
        inputQueue.append(idle_core.DNACBuildTask(template=template, task=reference_task))

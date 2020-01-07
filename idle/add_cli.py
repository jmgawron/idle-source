from settings.dnac_settings import BASE_URI
from idle import idle_core

CLI = {'uri': BASE_URI + '/v1/global-credential/cli',
       'method': 'POST'}


def update_add_cli_task(task, populate_template, connector, inputQueue):
    check_make_primary(task, inputQueue)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=CLI['uri'],
                       method=CLI['method'])
    #task.print_all()


def check_make_primary(task, inputQueue):
    if task.template['makePrimary']:
        template = {'profileName': task.template['profileName'],
                    'instanceUuid': '',
                    'key': 'credential.cli',
                    'value': [{'objReferences': [], 'type': 'credential_cli', 'url': ''}],
                    'id': ''}
        reference_task = ('make_primary_creds', 'make_primary_creds.j2')
        inputQueue.append(idle_core.DNACBuildTask(template=template, task=reference_task))

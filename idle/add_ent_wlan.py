from settings.dnac_settings import BASE_URI
from idle import idle_utilities
import json


WLAN = {'uri': BASE_URI + '/v1/commonsetting/wlan/-1',
        'method': 'POST'
        }


def update_add_ent_wlan_task(task, populate_template):
    task.template['fastlane'] = idle_utilities.lowercase_bool(task.template['fastlane'])
    task.template['macFiltering'] = idle_utilities.lowercase_bool(task.template['macFiltering'])
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=WLAN['uri'],
                       method=WLAN['method'])
    #task.print_jinja()

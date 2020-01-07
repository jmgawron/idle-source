from settings.dnac_settings import BASE_URI
from idle import idle_core
import json


WIRELESS_PROFILE = {'uri': BASE_URI + '/v1/siteprofile',
                    'method': 'POST'
                    }


# TODO add support for non-farbic mode
def update_add_wireless_profile_task(task, populate_template, inputQueue):
    check_sites_not_empty(task, inputQueue)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=WIRELESS_PROFILE['uri'],
                       method=WIRELESS_PROFILE['method'])
    #task.print_jinja()


def check_sites_not_empty(task, inputQueue):
    # TODO need to finish this part
    if task.template['sites']:
        template = {'profileName': task.template['']}
        reference_task = ('make_primary_creds', 'make_primary_creds.j2')
        inputQueue.append(idle_core.DNACBuildTask(template=template, task=reference_task))


# TODO add new task to send get to
# GET https://10.201.37.80/api/v1/siteprofile?name=api_test_profile
# GET https://10.201.37.80/api/v1/group and iterate over list to get id
# POST https://10.201.37.80/api/v1/siteprofile/36049cce-fac3-4b15-8da0-37ada329a8a8/site/730efd49-7720-466d-bb52-7d0afeda94c6
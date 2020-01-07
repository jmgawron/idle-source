from settings.dnac_settings import BASE_URI
import json


ADD_SERVERS = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
               'method': 'POST'}


GET_SERVER_UUID = {'uri': BASE_URI + '/v1/commonsetting/global/-1',
                   'method': 'GET'}


def update_add_network_settings_task(task, populate_template):
    print(task.template)
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=ADD_SERVERS['uri'],
                       method=ADD_SERVERS['method'])
    #task.print_jinja()

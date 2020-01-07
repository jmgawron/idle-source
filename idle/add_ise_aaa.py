from settings.dnac_settings import BASE_URI
import json


ADD_ISE_AAA = {'uri': BASE_URI + '/v1/aaa',
               'method': 'POST'}


def update_add_ise_aaa_task(task, populate_template):
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=ADD_ISE_AAA['uri'],
                       method=ADD_ISE_AAA['method'])
    #task.print_jinja()

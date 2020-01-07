from settings.dnac_settings import BASE_URI


ADD_VN = {'uri': BASE_URI + '/v2/data/customer-facing-service/virtualnetworkcontext/',
          'method': 'POST'}


def update_add_virtual_network_task(task, populate_template):
    task.set_attribute(jinja=populate_template(task.task[3], task.template),
                       uri=ADD_VN['uri'],
                       method=ADD_VN['method'])
    #task.print_task()

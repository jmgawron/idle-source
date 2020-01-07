from settings.dnac_settings import BASE_URI
import json


GET_PARENT_ID = {'uri': BASE_URI + '/v1/group/?groupName=',
                 'method': 'GET'}
ADD_SITE_GROUP = {'uri': BASE_URI + '/v1/group/',
                  'method': 'POST'}


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


def update_add_sg_to_vn_task(task, populate_template, connector):
    try:
        parentId = get_parent_id(task, connector)[0]['id']
    except IndexError as e:
        print("Debug:", e)
        parentId = 'null'
    else:
        task.template['parentId'] = parentId
        task.set_attribute(jinja=populate_template(task.task[3], task.template),
                           uri=ADD_SITE_GROUP['uri'],
                           method=ADD_SITE_GROUP['method'])
        #task.print_all()


def get_parent_id(task, connector):
    response = connector.get_request(GET_PARENT_ID['uri'] + task.template['*parentName'])
    response_json = json.loads(response.content)
    return response_json['response']


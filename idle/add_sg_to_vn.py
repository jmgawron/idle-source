from settings.dnac_settings import BASE_URI
import json


ADD_SG_TO_VN = {'uri': BASE_URI + '/v2/data/customer-facing-service/virtualnetworkcontext/',
                'method': 'PUT'}
GET_VN_ID = {'uri': BASE_URI + '/v2/data/customer-facing-service/virtualnetworkcontext?name=',
             'method': 'GET'}
GET_SG_ID = {'uri': BASE_URI + '/v2/data/customer-facing-service/scalablegroup?scalableGroupType=USER_DEVICE&attributes=id,name,scalableGroupType&name=',
             'method': "GET"}


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


def update_add_sg_to_vn_task(task, populate_template, connector):
    template = get_vn_id(task, connector)
    #print (template)
    template[0]['scalableGroup'] = []
    #print(template)
    idRef = get_sg_id(task, connector)
    idref_list = []
    for id in idRef:
        idref_list.append(json.dumps({'idRef': id}))
    idref_list_with_comma = ", ".join(idref_list)
    #print (idref_list_with_comma)
    try:
        template[0]['scalableGroup'].append(idref_list_with_comma)
    except IndexError as e:
        print("Debug:", e)
        template.append(idref_list_with_comma)
    #print ("idRef list empty: ", template[0]['scalableGroup'])
    task.set_attribute(jinja=populate_template(task.task[3], template[0]),
                       uri=ADD_SG_TO_VN['uri'],
                       method=ADD_SG_TO_VN['method'])
    task.print_task()


def get_vn_id(task, connector):
    response = connector.get_request(GET_VN_ID['uri'] + task.template['virtualNetworkName'])
    response_json = json.loads(response.content)
    return response_json['response']


def get_sg_id(task, connector):
    result = []
    sg_name_list = task.template['scalableGroupNames'].split(',')
    print ("SG name list: ", sg_name_list)
    for name in sg_name_list:
        response = connector.get_request(GET_SG_ID['uri'] + name.lstrip(' '))
        response_json = json.loads(response.content)
        try:
            result.append(response_json['response'][0]['id'])
        except IndexError as e:
            print("Debug:", e)
            result.append('null')
    #print (result)
    return result

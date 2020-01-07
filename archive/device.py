import yaml, os, sys
import ruamel.yaml


def loadYaml(fileName):
    cwd, filename = os.path.split(os.path.abspath(__file__))
    settings = os.sep + 'settings/'
    handle = open(os.path.join(cwd + settings, fileName))
    result = yaml.load(handle)
    return result


class Device(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def setAttribute(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Link(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


device_settings = loadYaml('devices.yaml')

devices = []

for k, v in device_settings.items():
    links = []
    for key, value in v.items():
        if 'link' in key:
            links.append(Link(interface=value['interface']))
    devices.append(Device(hostname=v['hostname'],
                          mgmt_ip=v['mgmt-ip'],
                          mgmt_mask=v['mgmt-mask'],
                          mgmt_gateway=v['mgmt-gateway'],
                          mgmt_intf=v['mgmt-intf'],
                          mgmt_vrf=v['mgmt-vrf'],
                          fusion_template=v['fusion-template'],
                          template=v['template'],
                          link=links))
    if 'border' in k:
        devices[-1].setAttribute(border=v['border'])
    if 'fusion' in k:
        devices[-1].setAttribute(default_originate=v['default-originate'])


for k, v in device_settings.items():
    links = []
    for key, value in v.items():
        if 'link' in key:
            links.append(Link(interface=value['interface']))


for device in devices:
    print(device.__dict__)



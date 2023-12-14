# -*- coding: utf-8 -*-
"""
Задание 1.6

Написать тест(ы), который проверяет находятся ли все интерфейсы, которые указаны
в файле net_interfaces_up.yaml в состоянии up (например, столбец Protocol в выводе sh ip int br).

Для проверки надо подключиться к каждому маршрутизатору, который указан
в файле net_interfaces_up.yaml с помощью scrapli/netmiko и проверить статус
интерфейсов. Можно использовать параметры из devices_reachable.yaml.

Тест(ы) должен проходить, если все интерфейсы из файла net_interfaces_up.yaml в состоянии up.
Тест может быть один или несколько. Файл net_interfaces_up.yaml можно менять - писать другие
интерфейсы или IP-адреса, главное чтобы формат оставался таким же.

Тест(ы) написать в файле задания.

Для заданий этого раздела нет тестов для проверки тестов :)
"""

import pytest
from scrapli import Scrapli
import yaml

with open('devices_reachable.yaml') as f:
    devices = yaml.safe_load(f)
    ip_list = [dev['host'] for dev in devices]

with open('net_interfaces_up.yaml') as f:
    interfaces = yaml.safe_load(f)


@pytest.fixture(params=devices, ids=ip_list)
def ssh_con(request):
    with Scrapli(**request.param) as ssh:
        yield ssh


def test_interfaces(ssh_con):
    reply = ssh_con.send_command('sh ip int br')
    result = reply.textfsm_parse_output()
    print(result)
    for intf in result:
        intf_list = interfaces.get(intf['ip_address'])
        if intf_list:
            break
    else:
        assert intf_list, 'No record for device'
    for intf in result:
        if intf['interface'] in intf_list:
            intf_list.remove(intf['interface'])
            assert intf['proto'] == 'up', f'Interface {intf["interface"]} is down'

    assert len(intf_list) == 0, f'Not in config {intf_list}'

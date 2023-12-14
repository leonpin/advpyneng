import pytest
from task_1_1 import get_int_vlan_map


@pytest.fixture
def cfg_ex():
    with open("config_sw1.txt") as f:
        cfg = f.read()
    return cfg


def test_return_type(cfg_ex):
    ac_dict, tr_dict = get_int_vlan_map(cfg_ex)
    assert isinstance(ac_dict, dict) and isinstance(tr_dict, dict), 'Result is not dict'


def test_result(cfg_ex):
    ac_dict, tr_dict = get_int_vlan_map(cfg_ex)
    correct_ac_dict, correct_tr_dict = ({'FastEthernet0/0': 10,
                                         'FastEthernet0/2': 20,
                                         'FastEthernet1/0': 20,
                                         'FastEthernet1/1': 30,
                                         'FastEthernet1/3': 1},
                                        {'FastEthernet0/1': [100, 200],
                                         'FastEthernet0/3': [100, 300, 400, 500, 600],
                                         'FastEthernet1/2': [400, 500, 600]})
    assert (ac_dict, tr_dict) == (correct_ac_dict, correct_tr_dict), 'Wrong result'

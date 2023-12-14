from task_1_2 import Network
import pytest

net1 = Network('10.1.0.0/30')


def test_network_attr():
    #    net1 = Network('10.1.0.0/30')
    assert getattr(net1, 'network')
    assert net1.network == '10.1.0.0/30'
    assert net1.addresses == ('10.1.0.1', '10.1.0.2')


def test_network_iter():
    assert getattr(net1, '__iter__')
    iterator = iter(net1)
    assert iterator
    assert next(iterator) == '10.1.0.1'
    assert next(iterator) == '10.1.0.2'


def test_network_len():
    assert len(net1) == 2


def test_network_getitem():
    assert net1[1] == '10.1.0.2'
    assert net1[-1] == '10.1.0.2'


def test_network_getitem_raises():
    with pytest.raises(IndexError):
        assert net1[-10]

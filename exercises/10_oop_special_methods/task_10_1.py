# -*- coding: utf-8 -*-
'''
Задание 10.1

Скопировать класс IPv4Network из задания 9.1 и добавить ему все методы,
которые необходимы для реализации протокола последовательности (sequence):
* __getitem__, __len__, __contains__, __iter__
* index, count - должны работать аналогично методам в списках и кортежах

И оба метода, которые отвечают за строковое представление экземпляров
класса IPv4Network.

Существующие методы и атрибуты (из задания 9.1) можно менять, при необходимости.

Пример создания экземпляра класса:

In [2]: net1 = IPv4Network('8.8.4.0/29')

Проверка методов:

In [3]: for ip in net1:
   ...:     print(ip)
   ...:
8.8.4.1
8.8.4.2
8.8.4.3
8.8.4.4
8.8.4.5
8.8.4.6

In [4]: net1[2]
Out[4]: '8.8.4.3'

In [5]: net1[-1]
Out[5]: '8.8.4.6'

In [6]: net1[1:4]
Out[6]: ('8.8.4.2', '8.8.4.3', '8.8.4.4')

In [7]: '8.8.4.4' in net1
Out[7]: True

In [8]: net1.index('8.8.4.4')
Out[8]: 3

In [9]: net1.count('8.8.4.4')
Out[9]: 1

In [10]: len(net1)
Out[10]: 6

Строковое представление:

In [13]: net1
Out[13]: IPv4Network(8.8.4.0/29)

In [14]: str(net1)
Out[14]: 'IPv4Network 8.8.4.0/29'

'''
import ipaddress


class IPv4Network:
    def __init__(self, network, gw=None):
        self.network = network
        self._subnet = ipaddress.ip_network(network)
        self.hosts = tuple([str(ip) for ip in self._subnet.hosts()])
        self.allocated = set()
        self.unassigned = set(self.hosts)
        self.broadcast = str(self._subnet.broadcast_address)
        if gw:
            self.gw = gw
            self.allocate_ip(self.gw)

    def allocate_ip(self, ip):
        if ip in self.hosts:
            if ip in self.unassigned:
                self.allocated.add(ip)
                self.unassigned.discard(ip)
            else:
                raise ValueError(f'IP-адрес уже выделен')
        else:
            raise ValueError(f'IP - адрес не входит в сеть {self.network}')

    def free_ip(self, ip):
        if ip in self.allocated:
            self.unassigned.add(ip)
            self.allocated.discard(ip)
        else:
            raise ValueError(f'IP-адрес свободен')

    def __getitem__(self, item):
        return self.hosts[item]

    def __len__(self):
        return len(self.hosts)

    def __iter__(self):
        return iter(self.hosts)

    def __str__(self):
        return f'IPv4Network: {self.network}'

    def __repr__(self):
        return f'IPv4Network("{self.network}")'

    def __contains__(self, item):
        return item in self.hosts

    def count(self, item):
        return self.hosts.count(item)

    def index(self, item):
        return self.hosts.index(item)


if __name__ == "__main__":
    # Примеры обращения к переменным и вызова методов
    net1 = IPv4Network("10.1.1.0/29")
    print(repr(net1))
    print(net1.index('10.1.1.6'))
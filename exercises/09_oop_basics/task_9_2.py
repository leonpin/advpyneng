# -*- coding: utf-8 -*-
"""
Задание 9.2

Создать класс PingNetwork. При создании экземпляра класса PingNetwork,
как аргумент передается экземпляр класса IPv4Network.

У класса PingNetwork должны быть методы _ping и scan

Метод _ping с параметром ip: должен пинговать один IP-адрес и возвращать
* True - если адрес пингуется
* False - если адрес не пингуется

Метод scan с таким параметрами:

* workers - значение по умолчанию 5
* include_unassigned - значение по умолчанию False

Метод scan:

* Пингует адреса из сети, которая передается как аргумент при создании экземпляра.
* Адреса должны пинговаться в разных потоках, для этого использовать concurrent.futures.
* По умолчанию, пингуются только адреса, которые находятся в атрибуте allocated.
  Если параметр include_unassigned равен True, должны пинговаться и адреса unassigned.
* Метод должен возвращать кортеж с двумя списками: список доступных IP-адресов и список недоступных IP-адресов


Пример работы с классом PingNetwork. Сначала создаем сеть:
In [3]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [4]: net1.allocate_ip('8.8.4.2')
   ...: net1.allocate_ip('8.8.4.4')
   ...: net1.allocate_ip('8.8.4.6')
   ...:

In [5]: net1.allocated
Out[5]: {'8.8.4.6', '8.8.4.2', '8.8.4.4'}

In [6]: net1.unassigned
Out[6]: {'8.8.4.5', '8.8.4.3', '8.8.4.1'}

Затем создается экземпляр класса PingNetwork, а сеть передается как аргумент:

In [8]: ping_net = PingNetwork(net1)

Пример работы метода scan:
In [9]: ping_net.scan()
Out[9]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [10]: ping_net.scan(include_unassigned=True)
Out[10]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

"""
from task_9_1 import IPv4Network
import subprocess
from concurrent.futures import ThreadPoolExecutor


class PingNetwork:
    def __init__(self, network):
        self.network = network

    # @staticmethod
    def _ping(self, ip):
        reply = subprocess.run(['ping', '-c', '2', '-n', ip], stdout=subprocess.PIPE, encoding='utf-8')
        result = ' 0% packet loss' in reply.stdout
        return result

    def scan(self, workers=5, include_unassigned=False):
        av = []
        unav = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            if include_unassigned:
                addrlist = self.network.hosts
            else:
                addrlist = self.network.allocated
            result = executor.map(self._ping, addrlist)
            for ip, reply in zip(addrlist, result):
                if reply:
                    av.append(ip)
                else:
                    unav.append(ip)
        return av, unav


if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    net1.allocate_ip('8.8.4.2')
    net1.allocate_ip('8.8.4.1')
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")
    ping_net = PingNetwork(net1)
    print(ping_net.scan(include_unassigned=True))

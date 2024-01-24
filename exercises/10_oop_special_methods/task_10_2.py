# -*- coding: utf-8 -*-
'''
Задание 10.2

Скопировать класс PingNetwork из задания 9.2 и изменить его таким образом,
чтобы адреса пинговались не при вызове метода scan, а при вызове экземпляра.

Вся функциональность метода scan должна быть перенесена в метод, который отвечает
за вызов экземпляра.

Пример работы с классом PingNetwork. Сначала создаем сеть:
In [2]: net1 = IPv4Network('8.8.4.0/29')

И выделяем несколько адресов:
In [3]: net1.allocate('8.8.4.2')
   ...: net1.allocate('8.8.4.4')
   ...: net1.allocate('8.8.4.6')
   ...:

Затем создается экземпляр класса PingNetwork, сеть передается как аргумент:
In [6]: ping_net = PingNetwork(net1)

После этого экземпляр должен быть вызываемым объектом (callable):

In [7]: ping_net()
Out[7]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6'])

In [8]: ping_net(include_unassigned=True)
Out[8]: (['8.8.4.4'], ['8.8.4.2', '8.8.4.6', '8.8.4.1', '8.8.4.3', '8.8.4.5'])

'''

from task_10_1 import IPv4Network
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

    def __call__(self, *args, **kwargs):
        return self.scan(*args, **kwargs)


if __name__ == "__main__":
    net1 = IPv4Network('8.8.4.0/29')
    net1.allocate_ip('8.8.4.2')
    net1.allocate_ip('8.8.4.1')
    print(f"{net1.allocated=}")
    print(f"{net1.unassigned=}")
    ping_net = PingNetwork(net1)
    print(ping_net(include_unassigned=True))

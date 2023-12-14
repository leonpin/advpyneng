# -*- coding: utf-8 -*-
"""
Задание 2.3

Написать аннотацию для всех методов класса Topology:
аннотация должна описывать параметры и возвращаемое значение.

Проверить код с помощью mypy, если возникли какие-то ошибки, исправить их.
"""
from typing import Dict, Tuple

dict_tuple = Dict[Tuple[str, str], Tuple[str, str]]
tuple_two_str = Tuple[str, str]


class Topology:
    def __init__(self, topology_dict: dict_tuple) -> None:
        self.topology = self._normalize(topology_dict)

    @staticmethod
    def _normalize(topology_dict: dict_tuple) -> dict_tuple:
        normalized_topology = {}
        for box, neighbor in topology_dict.items():
            if neighbor not in normalized_topology:
                normalized_topology[box] = neighbor
        return normalized_topology

    def delete_link(self, from_port: tuple_two_str, to_port: tuple_two_str) -> None:
        if self.topology.get(from_port) == to_port:
            del self.topology[from_port]
        elif self.topology.get(to_port) == from_port:
            del self.topology[to_port]
        else:
            print("Такого соединения нет")


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

if __name__ == "__main__":
    t1 = Topology(topology_example)
    print(t1.topology)

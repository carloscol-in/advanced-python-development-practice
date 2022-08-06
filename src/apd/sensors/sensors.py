
import socket
import sys
from typing import Generic, List, Optional, TypeVar

import psutil


T_value = TypeVar('T_value')


class Sensor(Generic[T_value]):

    def value(self) -> T_value:
        raise NotImplementedError

    @classmethod
    def format(self, value: T_value) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.format(self.value())


class Temperature(Sensor[Optional[float]]):
    title = 'Ambient Temperature'

    def value(self):
        try:
            from adafruit_dht import DHT22
            from board import D4
        except (ImportError, NotImplementedError):
            return None

        try:
            return DHT22(D4).temperature
        except RuntimeError:
            return None

    @staticmethod
    def celsius_to_fahrenheit(value: float) -> float:
        return value * 9 / 5 + 32

    @classmethod
    def format(cls, value: Optional[float]) -> str:
        if value is None:
            return 'Unknown'
        else:
            return '{:.1f}C ({:.1f}F)'.format(
                value,
                cls.celsius_to_fahrenheit(value=value)
            )


class PythonVersion(Sensor[Optional[str]]):
    
    title = 'Python Version'
    
    def value(self):
        return sys.version_info

    @classmethod
    def format(cls, value: str) -> str:
        return f'Python Version: {value.major}.{value.minor}'


class IpAddresses(Sensor[Optional[List[str]]]):

    title = 'IP Addresses'

    def value(self) -> List[str]:
        hostname = socket.gethostname()
        addresses = socket.getaddrinfo(hostname, None)

        address_info = [(address[0].name, address[4][0]) for address in addresses]

        return address_info

    @classmethod
    def format(cls, value: List[str]) -> str:
        return f'IP Addresses: {", ".join([f"{v[0]}: {v[1]}" for v in value])}'


class CpuLoad():

    title = 'CPU Load'

    def value(self) -> float:
        return psutil.cpu_percent(interval=0.1)

    @classmethod
    def format(cls, value: float) -> str:
        return f''
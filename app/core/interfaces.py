from __future__ import annotations

from dataclasses import dataclass

from likeinterface import Interface, Network

from core.settings import interface_settings


@dataclass
class Interfaces:
    auth_interface: Interface = Interface(network=Network(base=interface_settings.AUTH_BASE))


interfaces = Interfaces()

from __future__ import annotations

from likeinterface import Interface, Network

from core.settings import interface_settings

interface = Interface(network=Network(base=interface_settings.INTERFACE_BASE))

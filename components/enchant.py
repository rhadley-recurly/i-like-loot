from __future__ import annotations

from components.base_component import BaseComponent
from enchant_types import EnchantType

class Enchant(BaseComponent):
    parent: Equippable
    bonus: 0

    def __init__(
        self,
        enchant_type: EnchantType,
    ):
        self.enchant_type = enchant_type


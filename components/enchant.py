from __future__ import annotations

from components.base_component import BaseComponent
from enchant_types import EnchantType

class Enchant(BaseComponent):
    def __init__(
        self,
        enchant_type: EnchantType,
    ):
        self.enchant_type = enchant_type

class HPEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.HP)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass HP by {self.bonus}.\n"

        return description

class DamageEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.DAMAGE)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass Damage by {self.bonus}.\n"

        return description

class DefenseEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.DEFENSE)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass Defense by {self.bonus}.\n"

        return description

class LeechEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.LEECH)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"{self.bonus}% life leech.\n"

        return description

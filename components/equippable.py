from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from equipment_types import EquipmentType
from rarity_levels import RarityLevel

if TYPE_CHECKING:
    from entity import Item

class Equippable(BaseComponent):
    parent: Item
    rarity: RarityLevel

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus

    def get_color(self) -> Tuple[int, int, int]:
        match self.rarity:
            case RarityLevel.COMMON:
                return color.gray
            case RarityLevel.UNCOMMON:
                return color.white
            case RarityLevel.RARE:
                return color.blue
            case RarityLevel.LEGENDARY:
                return color.gold
            case RarityLevel.UNIQUE:
                return color.brown
            case RarityLevel.SET:
                return color.green

        return color.gray

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=4)

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)

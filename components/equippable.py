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
        ilvl: int = 0,
        defense_bonus: int = 0,
        min_damage: int = 0,
        max_damage: int = 0,
    ):
        self.equipment_type = equipment_type

        self.ilvl = ilvl
        self.defense_bonus = defense_bonus
        self.min_damage = min_damage
        self.max_damage = max_damage

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

    def get_multiplier(self) -> Float:
        multiplier = float(1)
        match self.rarity:
            case RarityLevel.COMMON:
                multiplier = float(1)
            case RarityLevel.UNCOMMON:
                multiplier = float(1.1)
            case RarityLevel.RARE:
                multiplier = float(1.2)
            case RarityLevel.LEGENDARY:
                multiplier = float(1.3)
            case RarityLevel.UNIQUE:
                multiplier = float(1.5)
            case RarityLevel.SET:
                multiplier = float(1.5)

        return float(multiplier)

    @property
    def min_dmg(self) -> int:
        return int((self.min_damage + self.ilvl) * self.get_multiplier())

    @property
    def max_dmg(self) -> int:
        return int((self.max_damage + self.ilvl) * self.get_multiplier())

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, min_damage=1, max_damage=4)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, min_damage=1, max_damage=8)

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=1)

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense_bonus=3)

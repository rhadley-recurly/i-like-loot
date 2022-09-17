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
        defense: int = 0,
        min_damage: int = 0,
        max_damage: int = 0,
    ):
        self.equipment_type = equipment_type

        self.ilvl = ilvl
        self.defense = defense
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

    def enchant(self) -> None:
        max_enchants = 0
        match self.rarity:
            case RarityLevel.UNCOMMON:
                max_enchants = 1
            case RarityLevel.RARE:
                max_enchants = 2
            case RarityLevel.LEGENDARY:
                max_enchants = 3
            case RarityLevel.UNIQUE:
                max_enchants = 4
            case RarityLevel.SET:
                max_enchants = 4

    @property
    def min_dmg(self) -> int:
        return int((self.min_damage + self.ilvl) * self.get_multiplier())

    @property
    def max_dmg(self) -> int:
        return int((self.max_damage + self.ilvl) * self.get_multiplier())

    @property
    def equipped_defense(self) -> int:
        if self.defense > 0:
            return int((self.defense + self.ilvl) * self.get_multiplier())
        else:
            return self.defense

    def is_equipped(self, equipment: Equipment, slot: str) -> bool:
        equipped_slot = getattr(equipment, slot)

        if equipped_slot:
            if equipped_slot.equippable == self:
                return True

        return False

    @property
    def description(self) -> str:
        rarity = ""
        match self.rarity:
            case RarityLevel.COMMON:
                rarity = "Common"
            case RarityLevel.UNCOMMON:
                rarity = "Uncommon"
            case RarityLevel.RARE:
                rarity = "Rare"
            case RarityLevel.LEGENDARY:
                rarity = "Legendary"
            case RarityLevel.UNIQUE:
                rarity = "Unique"
            case RarityLevel.SET:
                rarity = "Set"

        description = f"Item Level: {self.ilvl}\n"
        description += f"Rarity: {rarity}\n"

        if self.defense > 0:
            description += f"Defense: {self.equipped_defense}\n"

        if self.min_damage > 0:
            description += f"Damage: {self.min_dmg}-{self.max_dmg}\n"

        return description

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, min_damage=1, max_damage=4)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, min_damage=1, max_damage=8)

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense=3)

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defense=6)

class Helmet(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.HEAD, defense=2)

class Pants(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.PANTS, defense=2)

class Hands(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.HANDS, defense=2)

class Shoes(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.SHOES, defense=2)

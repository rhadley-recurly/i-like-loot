from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Actor, Item

class Equipment(BaseComponent):
    parent: Actor

    def __init__(self, weapon: Optional[Item] = None, armor: Optional[Item] = None):
        self.weapon = weapon
        self.armor = armor

    @property
    def min_damage(self) -> int:
        if self.weapon:
            return self.weapon.equippable.min_dmg

    @property
    def max_damage(self) -> int:
        if self.weapon:
            return self.weapon.equippable.max_dmg

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        else:
            slot = "armor"

        if equippable_item.equippable.is_equipped(self, slot):
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)

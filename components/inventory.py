from __future__ import annotations

from typing import List, TYPE_CHECKING

from entity import Item
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item

class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and restores it to the game map, at the player's current location.
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")

    def sort_items(self, item: Item) -> str:
        sort_by = item.name
        if item.equippable:
            if self.parent.equipment.item_is_equipped(item):
                """
                Make equipped items sort to top
                """
                sort_by = "__" + item.name

        return sort_by

    @property
    def sorted_stacked_items(self) -> List:
        sorted_items = self.items
        sorted_items.sort(reverse=True, key=self.sort_items)

        stacked_items = []
        previous_item = None
        item_count = 0

        for item in sorted_items:
            if item.stackable:
                if item_count == 0:
                    if previous_item is None:
                        previous_item = item

                if previous_item.name != item.name:
                    previous_item.count = item_count
                    item_count = 1
                    stacked_items.append(previous_item)
                    previous_item = item
                else:
                    item_count += 1
            else:
                stacked_items.append(item)

        if item_count > 0:
            previous_item.count = item_count
            stacked_items.append(previous_item)

        return stacked_items

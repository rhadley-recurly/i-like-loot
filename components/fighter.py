from __future__ import annotations

import os
from typing import TYPE_CHECKING

import color
import enchant_types
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor
    empowered: int

    def __init__(self, hp: int, mp: int, base_defense: int, min_damage: int, max_damage, strength: int, intelligence: int, dexterity: int, constitution: int):
        self._max_hp = hp
        self._max_mp = mp
        self.base_defense = base_defense
        self.min_damage = min_damage
        self.max_damage = max_damage
        self._strength = strength
        self._intelligence = intelligence
        self._dexterity = dexterity
        self._constitution = constitution
        self._mp = mp + intelligence
        self._hp = hp + constitution
        self.empowered = 0

    @property
    def strength(self) -> int:
        adjusted_strength = self._strength
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.STR:
                adjusted_strength += int(enchant.bonus)
                    
        return adjusted_strength

    @property
    def intelligence(self) -> int:
        adjusted_intelligence = self._intelligence
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.INT:
                adjusted_intelligence += int(enchant.bonus)
                    
        return adjusted_intelligence

    @property
    def dexterity(self) -> int:
        adjusted_dexterity = self._dexterity
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.DEX:
                adjusted_dexterity += int(enchant.bonus)
                    
        return adjusted_dexterity

    @property
    def constitution(self) -> int:
        adjusted_constitution = self._constitution
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.CON:
                adjusted_constitution += int(enchant.bonus)
                    
        return adjusted_constitution

    @property
    def max_hp(self) -> int:
        adjusted_hp = self._max_hp + self.constitution
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.HP:
                adjusted_hp += int(enchant.bonus)
                    
        return adjusted_hp

    @property
    def max_mp(self) -> int:
        adjusted_mp = self._max_mp + self.intelligence
        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.MP:
                adjusted_mp += int(enchant.bonus)
                    
        return adjusted_mp

    @property
    def hp(self) -> int:
        return round(self._hp)

    @property
    def mp(self) -> int:
        return round(self._mp)

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @mp.setter
    def mp(self, value: int) -> None:
        self._mp = max(0, min(value, self.max_mp))

    @property
    def defense(self) -> int:
        defense = self.base_defense
        if self.parent.equipment.weapon:
            defense += self.parent.equipment.weapon.equippable.equipped_defense
        if self.parent.equipment.head:
            defense += self.parent.equipment.head.equippable.equipped_defense
        if self.parent.equipment.armor:
            defense += self.parent.equipment.armor.equippable.equipped_defense
        if self.parent.equipment.hands:
            defense += self.parent.equipment.hands.equippable.equipped_defense
        if self.parent.equipment.pants:
            defense += self.parent.equipment.pants.equippable.equipped_defense
        if self.parent.equipment.shoes:
            defense += self.parent.equipment.shoes.equippable.equipped_defense

        for enchant in self.parent.equipment.enchants:
            if enchant.enchant_type == enchant_types.EnchantType.DEFENSE:
                defense += int(enchant.bonus)

        return defense

    @property
    def unarmed_min_damage(self) -> int:
        return self.min_damage

    @property
    def unarmed_max_damage(self) -> int:
        return self.max_damage

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
            if os.path.exists("savegame.sav"):
                os.remove("savegame.sav")  # Deletes the active save file.
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die
            if self.parent.name == "Dragon":
                self.engine.win = True

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def restore(self, amount: int) -> int:
        if self.mp == self.max_mp:
            return 0

        new_mp_value = self.mp + amount

        if new_mp_value > self.max_mp:
            new_mp_value = self.max_mp

        amount_recovered = new_mp_value - self.mp

        self.mp = new_mp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def use_mp(self, amount: int) -> None:
        self.mp -= amount

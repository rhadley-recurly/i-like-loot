from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class Level(BaseComponent):
    parent: Actor

    def __init__(
        self,
        current_level: int = 1,
        current_xp: int = 0,
        level_up_base: int = 0,
        level_up_factor: int = 150,
        xp_given: int = 0,
    ):
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor
        self.xp_given = xp_given

    @property
    def experience_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        return self.current_xp > self.experience_to_next_level

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.level_up_base == 0:
            return

        self.current_xp += xp

        self.engine.message_log.add_message(f"You gain {xp} experience points.")

        if self.requires_level_up:
            self.engine.message_log.add_message(
                f"You advance to level {self.current_level + 1}!"
            )

    def increase_level(self) -> None:
        self.current_xp -= self.experience_to_next_level

        self.current_level += 1

    def increase_max_hp(self, amount: int = 5) -> None:
        self.parent.fighter._max_hp += amount
        self.parent.fighter.hp += amount

        self.engine.message_log.add_message("Your health improves!")

        self.increase_level()

    def increase_str(self, amount: int = 1) -> None:
        self.parent.fighter._strength += amount
        self.engine.message_log.add_message("Your strength improves!")
        self.increase_level()

    def increase_int(self, amount: int = 1) -> None:
        self.parent.fighter._intelligence += amount
        self.engine.message_log.add_message("Your intelligence improves!")
        self.increase_level()

    def increase_dex(self, amount: int = 1) -> None:
        self.parent.fighter._dexterity += amount
        self.engine.message_log.add_message("Your dexterity improves!")
        self.increase_level()

    def increase_con(self, amount: int = 1) -> None:
        self.parent.fighter._constitution += amount
        self.engine.message_log.add_message("Your constitution improves!")
        self.increase_level()

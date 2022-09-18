from __future__ import annotations

import random

import color
import actions
from exceptions import Impossible
from components.base_component import BaseComponent
from enchant_types import EnchantType
from input_handlers import AreaMeleeAttackHandler, BeemRangedAttackHandler, SingleRangedAttackHandler

class Enchant(BaseComponent):
    parent: Item

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

class MPEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.MP)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass MP by {self.bonus}.\n"

        return description

class STREnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.STR)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass STR by {self.bonus}.\n"

        return description

class INTEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.INT)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass INT by {self.bonus}.\n"

        return description

class DEXEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.DEX)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass DEX by {self.bonus}.\n"

        return description

class CONEnchant(Enchant):
    def __init__(self, bonus: int) -> None:
        super().__init__(enchant_type=EnchantType.CON)
        self.bonus = bonus

    @property
    def description(self) -> str:
        description = f"Increass CON by {self.bonus}.\n"

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

class EnchantAbility(Enchant):
    def __init__(self, name: str, mana: int) -> None:
        super().__init__(enchant_type=EnchantType.ABILITY)
        self.level = 1
        self.name = name
        self.mana = mana

    def get_action(self, user: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this ability."""
        return actions.AbilityAction(user, self)

    def activate(self, action: actions.AbilityAction) -> None:
        user = action.entity

        if user.fighter.mp < self.mana:
            raise Impossible("Not enough MP.")
        else:
            user.fighter.use_mp(self.mana)

class Whirlwind(EnchantAbility):
    def __init__(self) -> None:
        super().__init__(
            name="Whirlwind",
            mana=2,
        )

    @property
    def description(self) -> str:
        description = f"(STR) Whirlwind (s)kill\n    Attack all enemies around you.\n"

        return description

    def get_action(self, user: Actor) -> AreaMeleeAttackHandler:
        self.radius = self.level
        if self.radius > 3:
            self.radius = 3
        self.engine.message_log.add_message(
            "Execute Whirlwind?", color.needs_target
        )
        return AreaMeleeAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.AbilityAction(user, self, xy),
        )

    def activate(self, action: actions.AbilityAction, area: Tuple[int, int]) -> None:
        super().activate(action=action)

        damage = 2 * self.engine.player.fighter.strength

        for xy in area:
            target = self.engine.game_map.get_actor_at_location(xy[0], xy[1])
            if target:
                self.engine.message_log.add_message(
                    f"The {target.name} is caught up in your whirlwind, taking {damage} damage!"
                )
                target.fighter.take_damage(damage)

class LightningBolt(EnchantAbility):
    def __init__(self) -> None:
        super().__init__(
            name="Lightning Bolt",
            mana=1,
        )

    @property
    def description(self) -> str:
        description = f"(INT) Lightning Bolt (s)kill\n    Attack multiple enemies in a line.\n"

        return description

    def get_action(self, user: Actor) -> BeemRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return BeemRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.AbilityAction(user, self, xy),
        )

    def activate(self, action: actions.AbilityAction, path: Tuple[int, int]) -> None:
        super().activate(action=action)

        damage = self.level * self.engine.player.fighter.intelligence
        for xy in path:
            target = self.engine.game_map.get_actor_at_location(xy[0], xy[1])
            if target:
                target.fighter.take_damage(damage)
                self.engine.message_log.add_message(
                    f"The lightning bolt zaps {target.name} for {damage} damage!"
                )

class ShadowStrike(EnchantAbility):
    def __init__(self) -> None:
        super().__init__(
            name="Shadow Strike",
            mana=2,
        )

    @property
    def description(self) -> str:
        description = f"(DEX) Shadow Strike (s)kill\n    Teleport and backstab a target.\n"

        return description

    def get_action(self, user: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.AbilityAction(user, self, xy),
        )

    def activate(self, action: actions.AbilityAction, target_xy: Tuple[int, int]) -> None:
        super().activate(action=action)

        damage = self.level * self.engine.player.fighter.dexterity
        target = self.engine.game_map.get_actor_at_location(target_xy[0], target_xy[1])
        if target:
            # Find empty spaces around target
            center_x = target_xy[0]
            center_y = target_xy[1]
            start_x = center_x - 1
            stop_x = center_x + 1
            start_y = center_y - 1
            stop_y = center_y + 1

            teleport_options = []
            for x in range(start_x, stop_x + 1):
                for y in range(start_y, stop_y + 1):
                    if self.engine.game_map.tiles["walkable"][x, y]:
                        if not self.engine.game_map.get_actor_at_location(x, y):
                            teleport_options.append([x, y])

            if not teleport_options:
                raise Impossible("No empty tile to teleport to.")

            teleport_to = random.choice(teleport_options)
            self.engine.player.x = teleport_to[0]
            self.engine.player.y = teleport_to[1]

            target.fighter.take_damage(damage)
            self.engine.message_log.add_message(
                f"You step through the shadows and stab {target.name} doing {damage} damage!"
            )
        else:
            raise Impossible("No one here to teleport to.")


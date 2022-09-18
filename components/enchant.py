from __future__ import annotations

import color
import actions
from exceptions import Impossible
from components.base_component import BaseComponent
from enchant_types import EnchantType
from input_handlers import AreaMeleeAttackHandler

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

    def activate(self, action: actions.AbilityAction, xy: Tuple[int, int]) -> None:
        super().activate(action=action)

        self.radius += 1
        damage = 2 * self.engine.player.fighter.strength

        for actor in self.engine.game_map.actors:
            if actor.distance(*xy) <= self.radius:
                if actor != self.engine.player:
                    self.engine.message_log.add_message(
                        f"The {actor.name} is caught up in your whirlwind, taking {damage} damage!"
                    )
                    actor.fighter.take_damage(damage)

class LightningBolt(EnchantAbility):
    def __init__(self) -> None:
        super().__init__(
            name="Lightning Bolt",
            mana=2,
        )

    @property
    def description(self) -> str:
        description = f"(INT) Lightning Bolt (s)kill\n    Attack multiple enemies in a line.\n"

        return description

    def get_action(self, user: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.AbilityAction(user, self, xy),
        )

    def activate(self, action: actions.AbilityAction, xy: Tuple[int, int]) -> None:
        super().activate(action=action)

        damage = self.level * self.engine.player.fighter.intelligence

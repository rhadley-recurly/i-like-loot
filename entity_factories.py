from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=2, min_damage=1, max_damage=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=8, base_defense=0, min_damage=1, max_damage=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=20),
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=12, base_defense=4, min_damage=4, max_damage=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=40),
)

ogre = Actor(
    char="O",
    color=(168, 52, 235),
    name="Ogre",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_defense=8, min_damage=15, max_damage=25),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=80),
)

dragon = Actor(
    char="D",
    color=(31, 112, 22),
    name="Dragon",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=40, base_defense=10, min_damage=20, max_damage=30),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=160),
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    stackable=True,
    consumable=consumable.HealingConsumable(amount=5),
)

taco = Item(
    char="!",
    color=(127, 0, 255),
    name="Taco",
    stackable=True,
    consumable=consumable.HealingConsumable(amount=5),
)

super_health_potion = Item(
    char="!",
    color=(163, 31, 31),
    name="Super Health Potion",
    stackable=True,
    consumable=consumable.HealingConsumable(amount=20),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    stackable=True,
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    stackable=True,
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    stackable=True,
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

blink_scroll = Item(
    char="~",
    color=(177, 196, 193),
    name="Blink Scroll",
    stackable=True,
    consumable=consumable.BlinkConsumable(),
)

dagger = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=equippable.Dagger(),
)

sword = Item(
    char="/",
    color = (255, 255, 255),
    name="Sword",
    equippable=equippable.Sword(),
)

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail()
)

helmet = Item(
    char="[",
    color=(139, 69, 19),
    name="Helmet",
    equippable=equippable.Helmet()
)

gloves = Item(
    char="[",
    color=(139, 69, 19),
    name="Gloves",
    equippable=equippable.Hands()
)

pants = Item(
    char="[",
    color=(139, 69, 19),
    name="Greeves",
    equippable=equippable.Pants()
)

flipflops = Item(
    char="[",
    color=(139, 69, 19),
    name="Flipflops",
    equippable=equippable.Shoes()
)

import random

list_avatar = [
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Abby",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Socks",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Chester",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Sadie",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Zoey",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Spooky",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Kiki",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Misty",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Princess",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Buster",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Mittens",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Whiskers",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Luna",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Harley",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Angel",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Maggie",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Loki",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Coco",
    "https://api.dicebear.com/7.x/adventurer/svg?seed=Patches",
]


def get_random_avatar_url():
    return random.choice(list_avatar)

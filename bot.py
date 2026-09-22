import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = "8705307598:AAFo_eacq-zD399ge_XNZd5BhWTqmM4wizo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

player = {"hp": 40, "max_hp": 40, "str": 10, "agi": 8}
enemy = {"hp": 30, "max_hp": 30, "str": 7, "agi": 6}

def attack(attacker, defender):
    hit_chance = 70 + (attacker["agi"] - defender["agi"]) * 2
    if random.randint(1, 100) > hit_chance:
        return "Промах!", 0

    dmg = attacker["str"] + random.randint(0, 3)

    if random.randint(1, 100) <= 10:
        dmg = int(dmg * 1.5)
        return f"Критический удар! Урон: {dmg}", dmg

    return f"Удар! Урон: {dmg}", dmg


@dp.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer("Ты вышел на район. На тебя нападает Гопник!\n\nНажми /fight чтобы начать бой.")


@dp.message(F.text == "/fight")
async def fight(msg: Message):
    text_p, dmg_p = attack(player, enemy)
    enemy["hp"] -= dmg_p

    if enemy["hp"] <= 0:
        enemy["hp"] = enemy["max_hp"]
        await msg.answer(f"{text_p}\n\nТы победил гопника!\nПолучено: +15 опыта, +20 рублей.")
        return

    text_e, dmg_e = attack(enemy, player)
    player["hp"] -= dmg_e

    if player["hp"] <= 0:
        player["hp"] = player["max_hp"]
        await msg.answer(f"{text_e}\n\nТебя отмудохали… Ты очнулся у подъезда.")
        return

    await msg.answer(
        f"{text_p}\nЗдоровье врага: {enemy['hp']}/{enemy['max_hp']}\n\n"
        f"{text_e}\nТвоё здоровье: {player['hp']}/{player['max_hp']}\n\n"
        f"Нажми /fight чтобы продолжить бой."
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

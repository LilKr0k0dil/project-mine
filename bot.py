from aiogram import Bot, Dispatcher, types, filters
from aiogram.filters import Filter
from config import TOKEN, admins
from database import Database
from backdoor import *
import asyncio


bot = Bot(token=TOKEN)
dp = Dispatcher()
db = Database("database.db")

class IsBanned(Filter):

    async def __call__(self, message: types.Message) -> bool:
        return db.is_banned(message.from_user.id)

class IsAdmin(Filter):
    
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in admins

@dp.message(filters.Command("start"))
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Приветствуем в боте сервера RAFMINE Для игры на сервере пропишите \n /add ВашНикнейм \n p.s. используйте только 1 аккаунт для игры на сервере\n\n Для смены аккаунта напишите: \n/change ВашНикнейм")
    
@dp.message(filters.Command("add"))
async def add_command(message: types.Message):
    if db.check_account(message.from_user.id) == True:
        nickname = message.text.split(' ')[1]
        db.add_account(message.from_user.id, nickname)
        add_to_whitelist(nickname)
        await message.reply("Похдравляем с доступом на сервер!")
        
    else:
        await message.reply("У вас уже есть аккаунт!!!")
        
@dp.message(filters.Command("change"), ~IsBanned())
async def change_command(message: types.Message):
    nickname = message.text.split(' ')[1]
    if db.check_account(message.from_user.id) == False:
        delete_from_whitelist(db.get_nickname(message.from_user.id))
        db.change_nickname(message.from_user.id, nickname)
        add_to_whitelist(nickname)
        await message.reply("Аккаунт успешно сменён")
    else:
        await message.reply("У вас не привязан аккаунт!!!")

@dp.message(filters.Command("ban"), IsAdmin())
async def ban_command(message: types.Message):
    db.ban(message.text.split(' ')[1])
    delete_from_whitelist(message.text.split(' ')[1])
    ban(message.text.split(' ')[1])
    await message.reply("Успешно забанен")
        

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from data_base.quotes_db import user_add
from pars.pars_quotes import add_quotes

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await user_add(message.from_user.id)


# Парсинг пословиц
@router.message(Command(commands=['pars']))
async def pars_quotes(message: Message):
    await add_quotes(message.from_user.id)

@router.message()
async def message(message: Message):
    await user_add(message.forward_from.id)
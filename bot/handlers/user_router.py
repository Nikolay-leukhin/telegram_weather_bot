from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from bot.lexicon import Lexicon as lx

router: Router = Router()

# Этот файл содержит базовые маршруты для Telegram-бота, включая приветственное сообщение
# и команду помощи. Маршруты обрабатывают команды /start и /help.


@router.message(CommandStart())
async def welcome_process(msg: Message):
    await msg.answer(text=lx.start)


@router.message(Command(commands='help'))
async def help_process(msg: Message):
    await msg.answer(text=lx.help)

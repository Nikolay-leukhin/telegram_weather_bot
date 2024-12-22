from aiogram.types import BotCommand


menu_commands: list[BotCommand] = [
    BotCommand(
        command="/start",
        description = "Начать пользоваться ботом"
    ),
    BotCommand(
        command="/help",
        description="Что может бот"
    ),
    BotCommand(
        command="/weather",
        description="Получить погоду"
    ),
]
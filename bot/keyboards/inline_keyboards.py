from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_factories import DaysCountCallbackData, NewValueOfAspectCallbackData


class InlineKeyboards:
    @staticmethod
    def create_days_keyboard():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="1 день", callback_data=DaysCountCallbackData(count=1).pack()),
                    InlineKeyboardButton(text="3 дня", callback_data=DaysCountCallbackData(count=3).pack()),
                    InlineKeyboardButton(text="5 дней", callback_data=DaysCountCallbackData(count=5).pack())
                ]
            ]
        )
        return keyboard


    @staticmethod
    def create_confirm_weather_keyboard():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Все вернер", callback_data='confirmed_weather'),
                    InlineKeyboardButton(text="Изменить", callback_data='change_weather'),
                ]
            ]
        )
        return keyboard

    @staticmethod
    def change_data_keyboard():
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="1", callback_data=NewValueOfAspectCallbackData(value='start').pack()),
                    InlineKeyboardButton(text="2", callback_data=NewValueOfAspectCallbackData(value='end').pack()),
                    InlineKeyboardButton(text="3", callback_data=NewValueOfAspectCallbackData(value='extra').pack()),
                    InlineKeyboardButton(text="4", callback_data=NewValueOfAspectCallbackData(value='days').pack())
                ]
            ]
        )
        return keyboard

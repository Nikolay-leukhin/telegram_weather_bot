from aiogram.filters.callback_data import CallbackData


class DaysCountCallbackData(CallbackData, prefix='days'):
    count: int


class NewValueOfAspectCallbackData(CallbackData, prefix='change'):
    value: str



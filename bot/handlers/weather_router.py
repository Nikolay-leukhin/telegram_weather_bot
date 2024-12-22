from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter

from bot.lexicon import Lexicon as lx
from bot.states import CordsWeatherFSM
from bot.keyboards import InlineKeyboards, DaysCountCallbackData, NewValueOfAspectCallbackData

from service.api import Api, WeatherModel

router: Router = Router()
api = Api()

# Этот файл реализует маршруты для взаимодействия с пользователем в Telegram-боте.
# Основная функциональность включает сбор данных от пользователя,
# передачу их в API сервиса погоды и отображение результатов.


@router.message(Command(commands='weather'))
async def get_weather_process(msg: Message, state: FSMContext):
    await msg.answer(lx.start_point)
    await state.set_state(CordsWeatherFSM.start_point)


@router.message(StateFilter(CordsWeatherFSM.start_point))
async def handle_first_point_process(msg: Message, state: FSMContext):
    city = msg.text.upper().strip()
    await state.update_data(start_point=city)
    await state.set_state(CordsWeatherFSM.end_point)
    await msg.answer(lx.end_point)


@router.message(StateFilter(CordsWeatherFSM.end_point))
async def handle_last_point_process(msg: Message, state: FSMContext):
    city = msg.text.upper().strip()
    await state.update_data(end_point=city)
    await state.set_state(CordsWeatherFSM.extra_points)
    await msg.answer(lx.extra_points)


@router.message(StateFilter(CordsWeatherFSM.extra_points))
async def handle_last_point_process(msg: Message, state: FSMContext):
    raw_data = msg.text.upper().strip()
    if raw_data == 'НЕТ':
        await state.update_data(extra_points=[])
    else:
        city_list = raw_data.split(', ')
        await state.update_data(extra_points=city_list)

    await state.set_state(CordsWeatherFSM.prediction_days)
    await msg.answer(lx.prediction_days, reply_markup=InlineKeyboards.create_days_keyboard())


@router.callback_query(DaysCountCallbackData.filter())
async def handle_prediction_days_process(cb: CallbackQuery, callback_data: DaysCountCallbackData, state: FSMContext):
    await state.update_data(days=callback_data.count)
    await cb.answer()
    await state.set_state(CordsWeatherFSM.show_data)
    await show_current_data(cb.message, state)


async def show_current_data(msg: Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer(lx.confirm_points(
        start_point=data['start_point'],
        end_point=data['end_point'],
        extra_points=data['extra_points'],
        days=data['days']
    ), reply_markup=InlineKeyboards.create_confirm_weather_keyboard())
    await state.set_state(CordsWeatherFSM.confirm_points)


@router.callback_query(StateFilter(CordsWeatherFSM.confirm_points))
async def confirm_weather_data_process(cb: CallbackQuery, state: FSMContext):
    data = cb.data
    await cb.message.delete()

    if data == "confirmed_weather":
        await cb.message.answer("ЗАЗАГРУЖАЕМ ДАНННЫЕЕЕЕЕ!!!!!!!!")
        try:
            state_data = await state.get_data()
            points = [state_data['start_point']] + state_data['extra_points'] + [state_data['end_point']]
            weather_data = api.get_weather(state_data['days'], points)
            line = WeatherModel.format_weather_data(weather_data)
            await cb.message.answer(line)
            await state.clear()
        except Exception as ex:
            await cb.message.answer(str(ex) + ' попробуй в дургой раз')
            await state.clear()

    elif data == "change_weather":
        await cb.message.answer(
            lx.aspects_to_change,
            reply_markup=InlineKeyboards.change_data_keyboard()
        )
        await state.set_state(CordsWeatherFSM.get_new_data)


@router.callback_query(NewValueOfAspectCallbackData.filter())
async def get_new_value_of_aspect(cb: CallbackQuery, callback_data: NewValueOfAspectCallbackData, state: FSMContext):
    value = callback_data.value
    await state.update_data(aspect_index=value)
    await cb.message.delete()
    await cb.message.answer('Введи новое значени:')
    await state.set_state(CordsWeatherFSM.change_data)


@router.message(StateFilter(CordsWeatherFSM.change_data))
async def change_value_of_aspect(msg: Message, state: FSMContext):
    state_data = await state.get_data()

    value = state_data['aspect_index']
    new_value = msg.text

    if value == 'start':
        await state.update_data(start_point=new_value)
    elif value == 'end':
        await state.update_data(end_point=new_value)
    elif value == 'extra':
        await state.update_data(extra_points=new_value)
    elif value == 'days':
        await state.update_data(days=new_value)

    await state.update_data(aspect_index=None)
    await state.set_state(CordsWeatherFSM.show_data)
    await show_current_data(msg, state)




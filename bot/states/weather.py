from aiogram.fsm.state import StatesGroup, State


class CordsWeatherFSM(StatesGroup):
    start_point = State()
    end_point = State()
    extra_points = State()
    prediction_days = State()
    confirm_points = State()
    show_data = State()
    change_data = State()
    get_new_data = State()
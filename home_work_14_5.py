from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from crud_function1 import *

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
# initiate_db()


api = "8047196713:AAGowFkavLw9VOBcT7_NZ6UMcY4Y71TR7_o"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация'), KeyboardButton(text='Купить')]],
    resize_keyboard=True)

inline_choices = InlineKeyboardMarkup(InlineKeyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
     [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]]],
    resize_keyboard=True)

kb_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardMarkup(text='Product1', callback_data='product_buying')],
        [InlineKeyboardMarkup(text='Product2', callback_data='product_buying')],
        [InlineKeyboardMarkup(text='Product3', callback_data='product_buying')],
        [InlineKeyboardMarkup(text='Product4', callback_data='product_buying')]],
    resize_keyboard=True)

kb_reg = ReplyKeyboardMarkup(keyboard=[KeyboardButton(text='Регистрация')],
                             resize_keyboard=True)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_reg)


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) == False:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await RegistrationState.age.set()
    await message.answer('Введите свой возраст:')


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    user_data = await state.get_data()
    add_user(user_data["username"], user_data["email"], user_data["age"])
    await message.answer('Регистрация прошла успешно', reply_markup=menu)
    await state.finish()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_choices)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    with open('1.jpeg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product1 | Описание: описание 1 | Цена: 100 ')
    with open('2.jpeg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product2 | Описание: описание 2 | Цена: 200 ')
    with open('3.jpeg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product3 | Описание: описание 3 | Цена: 300 ')
    with open('4.jpg', 'rb') as img:
        await message.answer_photo(img, f'Название: Product4 | Описание: описание 4 | Цена: 400 ')
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_product)


@dp.callback_query_handler(text="product_buying")
async def end_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('calories = 10 * weight + 6.25 * growth - 5 * age + 5')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост:')


@dp.message_handler(state=UserState.growth)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес:')


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привет! Я бот помогающий твоему здоровью, {message.from_user.username}', reply_markup=menu)


@dp.message_handler()
async def all_message(message):
    await message.answer('Ввeдите команду /start,что бы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

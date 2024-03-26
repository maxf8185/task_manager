import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.for_navigate import films_keyboard
from filters.type_of_chat import ChatTypeFilter

films_router = Router()
films_router.message.filter(ChatTypeFilter(['private']))


async def read_file():
    async with aiofiles.open('./films.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./films.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@films_router.message(Command('films'))
async def homeworks_cmd(message: types.Message):
    await message.answer('Яку дію виконати з фільмами?', reply_markup=films_keyboard)


@films_router.message(F.text == 'view all films')
async def all_homeworks_cmd(message: types.Message):
    films_list = await read_file()
    if len(films_list) > 0:
        for i in await read_file():
            text = as_marked_section(
                Underline(Bold('Фільми🎥')),
                as_key_value('Назва ', i['topic']),
                as_key_value('Жанр ', i['number']),
                as_key_value('Посилання ', i['content']),
                marker='📌 '
            )
            builder = InlineKeyboardBuilder()
            builder.add(
                types.InlineKeyboardButton(text='Видалити фільм', callback_data=f'deletefilm_{films_list.index(i)}')
            )

            await message.answer(text.as_html(), reply_markup=builder.as_markup())
            await asyncio.sleep(0.3)
    else:
        await message.answer('hane no films')


@films_router.callback_query(F.data.split('_')[0] == 'deletefilm')
async def del_film(callback: types.CallbackQuery):  # 'delete_1'
    film_id = callback.data.split('_')[-1]
    films_list = await read_file()  # []
    films_list.pop(int(film_id))
    await write_file(films_list)
    await callback.message.answer('Фільм видалено! Оновіть список😊')
    await callback.answer('Its ok, film has been deleted', show_alert=True)


class AddFilm(StatesGroup):
    topic = State()
    genre = State()
    studio = State()


@films_router.message(StateFilter(None), F.text == 'add new film')
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer('Введіть назву фільму: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddFilm.topic)


@films_router.message(Command("cancel"))
@films_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@films_router.message(AddFilm.topic, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer('Введіть жанр фільму: ')
    await state.set_state(AddFilm.genre)


@films_router.message(AddFilm.genre, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('Введіть посилання: ')
    await state.set_state(AddFilm.studio)


@films_router.message(AddFilm.studio, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer('Фільм додано! Приємного перегляду!', reply_markup=films_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
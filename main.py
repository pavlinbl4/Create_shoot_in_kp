import asyncio
import logging
import sys
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from create_shoot import create_shoot
from telegram_bot_tools import kp_keyboard
from data.categories import category_dict
from data.get_credentials import Credentials
from aiogram.types import Message

import subprocess

form_router = Router()


class Form(StatesGroup):
    name = State()
    confirm = State()
    caption = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    logging.info(f"User {message.from_user.full_name}  with id {message.from_user.id}")
    await state.set_state(Form.name)
    await message.answer("Для создания съемки\nвыберите категорию",
                         reply_markup=kp_keyboard.kp_keyboard.as_markup(
                             resize_keyboard=True,
                         ))



@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)

    await state.clear()
    await message.answer(
        "*Оформление съемки отменено*",
        reply_markup=ReplyKeyboardRemove(),
    )


# @form_router.message(Form.name)
@form_router.message(Form.name, F.from_user.full_name.in_({'Евгений Павленко', 'Александр Коряков'}))
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.confirm)
    await message.answer(
        f"_Выбрана категория_ \n*{message.text}*\nПодтвердите ваш выбор",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

@form_router.message(F.from_user.full_name.not_in({'Евгений Павленко', 'Александр Коряков'}))
async def handle_other_messages(message: Message):
    await message.answer("It's private bot, you are not an allowed user.")


@form_router.message(Form.confirm, F.text.casefold() == "no")
async def process_bad_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    logging.info(f"User pressed NO {data}")
    await state.clear()
    await message.answer(
        "Запустите бота заново командой\n**/start**",
        reply_markup=ReplyKeyboardRemove(),
    )
    await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.confirm, F.text.casefold() == "yes")
async def process_good_category(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.caption)
    data = await state.get_data()

    await message.reply(
        f"_Выбрана категория_: *{data['name']}*\nВведите описание съемки",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.caption)
async def process_caption(message: Message, state: FSMContext) -> None:
    data = await state.update_data(caption=message.text)
    await state.clear()
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["name"]
    caption = data.get("caption", "")
    if positive:
        text = f"Категория - *{name}*\n"
        text += f"_описание съемки_: *{caption}*\n"
        text += "*Заявка на съемку создается*"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        try:
            create_shoot(caption, category_dict[name], message.from_user.full_name)
            await message.answer("I hope all good")
        except Exception as e:
            await message.reply(f"Error: {e}")
    else:
        text = "_ошибки бывают у всех_"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())




async def main():
    bot = Bot(token=Credentials().kp_tools,
              default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())

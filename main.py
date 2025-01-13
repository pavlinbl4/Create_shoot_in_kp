import asyncio
import logging
import sys
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, types
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
from aiogram.utils.markdown import escape_md

from create_shoot import create_shoot
from telegram_bot_tools import kp_keyboard
from data.categories import category_dict
from data.get_credentials import Credentials

form_router = Router()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class Form(StatesGroup):
    name = State()
    confirm = State()
    caption = State()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        "Для создания съемки\nвыберите категорию",
        reply_markup=kp_keyboard.kp_keyboard.as_markup(
            resize_keyboard=True,
        ),
    )


@form_router.message(Command("cancel"))
@form_router.message(F.text.func(lambda text: text.lower() == "cancel"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "*Оформление съемки отменено*",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    # Проверяем, разрешен ли пользователь
    allowed_users = {187597961}  # Список разрешенных пользователей
    if user_id not in allowed_users:
        logging.warning(f"Unauthorized access attempt by user {user_id}")
        await message.reply("Извините, вы не авторизованы для работы с этим ботом.")
        return

    category_name = message.text.strip()

    # Проверяем, существует ли категория
    if category_name not in category_dict:
        logging.warning(f"Category '{category_name}' not found for user {user_id}")
        await message.reply("Указанная категория не существует. Попробуйте снова.")
        return

    await state.update_data(name=category_name)
    await state.set_state(Form.confirm)
    await message.answer(
        f"_Выбрана категория_ \n*{escape_md(category_name)}*\nПодтвердите ваш выбор",
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


@form_router.message(Form.confirm, F.text.func(lambda text: text.lower() == "no"))
async def process_bad_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()
    await message.answer(
        "Запустите бота заново командой\n**/start**",
        reply_markup=ReplyKeyboardRemove(),
    )
    await show_summary(message=message, data=data, positive=False)


@form_router.message(Form.confirm, F.text.func(lambda text: text.lower() == "yes"))
async def process_good_category(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.caption)
    data = await state.get_data()
    category_name = escape_md(data["name"])

    await message.reply(
        f"{escape_md(message.from_user.full_name)}\n_Выбрана категория_: *{category_name}*\nВведите описание съемки",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.caption)
async def process_caption(message: Message, state: FSMContext) -> None:
    data = await state.update_data(caption=message.text.strip())
    await state.clear()
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = escape_md(data["name"])
    caption = escape_md(data.get("caption", ""))

    if positive:
        text = f"Категория - *{name}*\n"
        text += f"_описание съемки_: *{caption}*\n"
        text += "*Заявка на съемку создается*"
    else:
        text = "_Ошибки бывают у всех_"

    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

    try:
        # Асинхронный запуск внешнего процесса
        category = category_dict.get(data["name"])
        if not category:
            raise KeyError(f"Категория {data['name']} отсутствует в category_dict")

        process = await asyncio.create_subprocess_exec(
            'python', '-c',
            f"import create_shoot; create_shoot.create_shoot({repr(caption)}, {repr(category)})",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            await message.reply("Ваше приложение успешно запущено.")
            logging.info(f"Process output: {stdout.decode().strip()}")
        else:
            await message.reply(f"Ошибка запуска приложения:\n{stderr.decode().strip()}")
            logging.error(f"Process error: {stderr.decode().strip()}")
    except Exception as e:
        await message.reply(f"Ошибка выполнения: {e}")
        logging.exception("Exception during subprocess execution")


async def main():
    try:
        token = Credentials().pavlinbl4_bot
        bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    except Exception as e:
        logging.error(f"Failed to initialize bot: {e}")
        sys.exit(1)

    dp = Dispatcher()
    dp.include_router(form_router)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error while polling: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
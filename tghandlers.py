from aiogram.types import Message
from aiogram.enums import ChatType
from aiogram import Router, F
from aiogram.filters import Command
from loader import bot
import asyncio
import os
from dotenv import load_dotenv
from pymax import Client, ClientRouter, Message
from aiogram.fsm.context import FSMContext
from data import RegMaxState
load_dotenv()
TgId = int(os.getenv("TgId"))

router = Router()

@router.message(Command("start"))
async def handler_start(sms: Message):
    if sms.chat.type not in {ChatType.PRIVATE}:
        await sms.answer("Бот не прендназначен для групп")
        return
    if sms.from_user.id == TgId and not Client.is_authorized:
        await sms.answer("Этот бот является мостом между Telegram и Max, для регистрации аккаунта Max напишите команду /reg, или /help.")


@router.message(Command("help"))
async def handler_help(sms: Message):
    if sms.from_user.id != TgId:
        return
    await sms.answer("...") #тут че то будет потом


@router.message(Command("reg"))
async def handler_reg(sms: Message, state: FSMContext):
    if sms.from_user.id != TgId:
        return
    elif not Client.is_authorized:
        await state.set_state(RegMaxState.Phone)
        await sms.answer("Напишите свой номер телефона аккаунта Max")


@router.message(RegMaxState.Phone)
async def phone_state(sms: Message, state: FSMContext):
    phone = (sms.text)
    await state.update_data(phone=phone)
    await Client.send_code(phone)
    await state.set_state(RegMaxState.Code)
    await sms.answer("Ввидите код из Max")


@router.message(RegMaxState.Code)
async def code_state(sms: Message, state: FSMContext):
    code = (sms.text)
    data = await state.get_data()
    phone = data.get("phone")
    async def inline_code():
        return code
    try:

        client = Client(
            phone=phone,
            work_dir="max_session",
            session_name=f"session_user",
            code_callback=inline_code
        )

        await client.start()
        await state.clear()
    except Exception:
        await sms.answer("Скорее всего вы ввели не верный пароль, попробуйте всю процедуру еще раз.")


@router.message(Command("CheckSms"))
async def handler_checksms(sms: Message):
    if sms.from_user.id != TgId:
        return
    pass #ну тут будет типа просмотр сообщений которые пришли, и типо диномической клавиатуры кому ответить


@router.message((Command("CheckHistori")))
async def handler_checksms(sms: Message):
    if sms.from_user.id != TgId:
        return
    pass # ну тут будет типа просмотр диалого а именно последнии 150 сообщений именно для обычных чатов 


c = ClientRouter()


@c.on_message()
async def on_message(message: Message, client: Client) -> None:
    if message.text == "/start":
        await message.answer("Готово")


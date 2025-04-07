import logging
import time

from aiogram import Router, types, filters

from src.application.uow.uow import IUnitOfWork
from src.application.use_cases.auth.telegram import TelegramAuthUseCase
from src.domain.messages.action_hello import reply_hello_message
from src.domain.messages.action_mailto import reply_mailto_message
from src.utils.telegram.parse_start_command_args import parse_start_command_args


router = Router()


@router.message(filters.CommandStart)
async def start_handler(message: types.Message):
    logging.info(f'Start: {message.from_user.id} {message.from_user.full_name} {time.asctime()}. Message: {message}')

    uow = IUnitOfWork(
        current_user=await TelegramAuthUseCase.authenticate_by_message(message),
        x_timezone='Asia/Tashkent',
    )
    async with uow:
        arg_action, arg_data = parse_start_command_args(message.text)
        if arg_action is None:
            await action_hello_user(uow, message)
        else:
            match arg_action:
                case 'mailto':
                    await action_mailto(uow, message, arg_data)
                case _:
                    await action_hello_user(uow, message)
        await uow.commit()


async def action_hello_user(uow: IUnitOfWork, message: types.Message):
    await reply_hello_message(message)


async def action_mailto(uow: IUnitOfWork, message: types.Message, data: str):
    try:
        mailto_user_id = int(data)
    except ValueError:
        await message.reply(f'Кажется вы перешли по недействительной ссылке :(')
        return
    user = await uow.users.get_user_info_by_id(mailto_user_id)
    if user is None:
        await message.reply(f'Пользователь с id {mailto_user_id} не найден :(')
        return
    await reply_mailto_message(message, mailto_user_id, user.get_full_name())

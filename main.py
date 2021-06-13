import logging
import asyncio

from telethon import TelegramClient, Button
from telethon import events
from telethon.tl.custom import Message
from telethon.events.callbackquery import CallbackQuery

from message_deleter import MessageDeleter
from button_maker import PageMaker
from states import States, StateChecker
from product_manager import ProductManager
from config import *
from settings import *

logging.basicConfig(level=logging.INFO)
bot = TelegramClient('calories_bot', api_id=API_ID, api_hash=API_HASH).start(bot_token=TOKEN)
state = StateChecker()
deleter = MessageDeleter(bot)
product_mng = ProductManager()


@bot.on(events.NewMessage(pattern='/start'))
async def start(event: Message):
    user_id = event.sender_id

    if not product_mng.registered(user_id):
        button_text = 'Створити щоденник калорійності'
    else:
        button_text = 'Щоденник'

    await event.respond(START_MESSAGE, buttons=Button.text(button_text, resize=True))
    raise events.StopPropagation


@bot.on(events.NewMessage(pattern=r'Щоденник'))
async def show_diary(event: Message):
    user_id = event.sender_id

    if not product_mng.registered(user_id):
        await event.respond('Схоже, ви ще не створили щоденник калорійності',
                            buttons=Button.text('Створити щоденник калорійності'))
    else:
        user_diary = product_mng.get_diary(user_id)
        await event.respond(user_diary.show_diary())


@bot.on(events.NewMessage(pattern=r'Створити щоденник калорійності'))
async def create_diary(event: Message):
    user = await event.get_sender()

    if product_mng.registered(user.id):
        await event.respond('Щоденник вже було створено! Ви можете очистити його в меню')
    else:
        await product_mng.register_new_user(user)

    await event.respond('Щоденник успішно створено! Натисніть на кнопку Щоденник',
                        buttons=Button.text('Щоденник', resize=True))


@bot.on(events.NewMessage())
@state.check_state(States.WAIT_SEARCH)
@deleter.delete_previous_messages
async def search_product(event: Message):
    user_id = event.sender_id
    search_request = event.text
    pages = await product_mng.get_products_pages(search_request)
    pager = PageMaker.create_pager(user_id, pages)

    if not pager:
        curr_search_message = await event.respond('Нічого не знайдено')
    else:
        buttons = pager.make_page()
        curr_search_message = await event.respond('Результати пошуку', buttons=buttons)

    deleter.add_messages_to_delete(user_id, event.id, curr_search_message.id)


@bot.on(events.NewMessage())
@state.check_state(States.WAIT_WEIGHT)
async def input_weight(event: Message):
    user_id = event.sender_id
    try:
        weight = float(event.raw_text)
        print(weight)
        state.set_state(user_id)
    except (ValueError, OverflowError) as e:
        logging.error(e)
        await event.respond('Вказана неправильна одиниця!')


@bot.on(events.CallbackQuery(pattern=r'\d+'))
async def get_product(call: CallbackQuery.Event):
    product_id = int(call.data)
    product_info = await product_mng.get_product_info(product_id)

    await call.respond(product_info, buttons=Button.inline('Додати', f'add_{product_id}'))
    raise events.StopPropagation


@bot.on(events.CallbackQuery(pattern=r'add_(\d+)'))
async def add_product(call: CallbackQuery.Event):
    user_id = call.sender_id
    product_id = call.pattern_match.group(1).decode()

    state.set_state(user_id, States.WAIT_WEIGHT)
    state.set_product(user_id, product_id)

    await call.respond('Вкажи грамаж страви')


@bot.on(events.CallbackQuery(pattern=r'(prev|next)'))
async def toggle_page(call: CallbackQuery.Event):
    user_id = call.sender_id
    direction = call.pattern_match.group(1).decode()
    pager = PageMaker.get_pager(user_id)

    if not pager:
        await call.answer('Error', alert=True)
        await call.delete()
    else:
        buttons = pager.make_page(direction)
        await call.edit(buttons=buttons)

    raise events.StopPropagation


async def main():
    await bot.run_until_disconnected()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

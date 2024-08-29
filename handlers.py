from aiogram import types, Router, F
import logging
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot import dp
from data.quiz_data import quiz_data
from utils import update_quiz_index, get_quiz_index, update_quiz_result, get_quiz_result, show_quiz_result

router = Router()

def generate_options_keyboard(answer_options):
    logging.info("Генерация клавиатуры с вариантами ответов...")
    builder = InlineKeyboardBuilder()
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option)
        )
    builder.adjust(1)
    return builder.as_markup()

@router.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    user_answer = callback.data  # Получаем текст ответа пользователя
    user_id = callback.from_user.id

    # Удаляем кнопки из сообщения
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,  # Используем chat.id вместо user_id
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Выводим ответ пользователя
    await callback.answer() 
    await callback.message.reply(f"Ваш ответ: {user_answer}")

    # Проверяем, является ли ответ правильным
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    correct_answer = quiz_data[current_question_index]['options'][correct_index]

    if user_answer == correct_answer:
        await callback.message.answer("Верно!")
        score = await get_quiz_result(user_id) + 1
        await update_quiz_result(user_id, score)
        logging.info(f'Текущий результат {score}')
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Обновляем индекс вопроса
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await show_quiz_result(callback.message, user_id)  # Показываем результат
        await update_quiz_result(user_id, 0)
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать заново"))
        await callback.message.answer("Начните новую игру!", reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logging.info(f"Пользователь {message.from_user.id} начал игру.")
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts)
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

@router.message(F.text == "Начать игру")
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

    
@router.message(F.text == "Начать заново")
async def cmd_restart(message: types.Message):
    await message.answer(f"Начинаем квиз заново!")
    await new_quiz(message)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)
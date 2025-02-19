import asyncio
import aiohttp
import time
import ast
import datetime
from urllib.parse import urlparse
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
from text_scripts import *
from sql_scripts import *
from async_markdownv2 import *


engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    user_id = message.chat.id
    username = message.from_user.username

    async with async_session() as session:
        _check_user = await check_user_exists(session, user_id)
    if not _check_user:
        try:
            current_time = int(time.time())
            await add_user_data(session, user_id, username, current_time)

            button_list0 = [
                types.InlineKeyboardButton("Да", callback_data="custom_quest_1_yes"),
                types.InlineKeyboardButton("Нет", callback_data="custom_quest_1_no"),
            ]
            quest_reply_markup = types.InlineKeyboardMarkup([button_list0])

            text = await escape(lang_dict['first_custom_question'], flag=0)
            await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=quest_reply_markup, parse_mode="MarkdownV2")

            async with async_session() as session:
                await update_user_status(session, user_id, start_status)

        except Exception as error:
            print(f"ERROR LOG:\n Adding user to db error: {username}\n{error}")
    else:
        async with async_session() as session:
            await update_username(session, user_id, username)

        button_list0 = [
            types.InlineKeyboardButton("Перейти в чат ➡️", callback_data="join_chat"),
        ]
        button_list1 = [
            types.InlineKeyboardButton("Мой UserID", callback_data="user_id"),
        ]
        reply_markup = types.InlineKeyboardMarkup(
            [button_list0, button_list1])

        text = await escape(lang_dict['start_msg'], flag=0)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")

        async with async_session() as session:
            await update_user_status(session, user_id, start_status)


@bot.message_handler(commands=['faq'])
async def faq_command(message):
    user_id = message.chat.id
    username = message.from_user.username

    async with async_session() as session:
        _check_user = await check_user_exists(session, user_id)
    if not _check_user:
        try:
            current_time = int(time.time())
            await add_user_data(session, user_id, username, current_time)
        except Exception as error:
            print(f"ERROR LOG:\n Adding user to db error: {username}\n{error}")
    else:
        async with async_session() as session:
            await update_username(session, user_id, username)


    faq_text = ("**Часто задаваемые вопросы (FAQ)**\n\n"
                '____________________________________________\n\n'
                "**Обучение и сообщество USAbyTemamila**\n"
                '____________________________________________\n\n'
                "**1) Как можно пройти обучение у Артема и Милы Ракаевых?**\n"
                '- Мы обучаем инвесторов стратегиям Creative Financing ("Subject to", "Seller Financing", аренда с правом выкупа). Для участия нужно быть частью сообщества, пройти отбор и ознакомиться с бесплатными материалами.\n\n'
                '**2) Какие форматы обучения у вас есть?**\n'
                '- Бесплатные открытые Zoom-встречи каждый вторник в 5:00 PM PT. Закрытые Zoom-встречи каждую пятницу в 5:00 PM PT (для участников сообщества). Индивидуальное наставничество и разбор сложных кейсов.oОнлайн-курсы и записи для самостоятельного изучения.\n\n'
                '**3) Как долго занимает процесс первой сделки и получения прибыли?**\n'
                '- Это индивидуально: кто-то делает сделки уже во время обучения, а кто-то откладывает процесс на месяцы. В среднем на первую сделку уходит около месяца: маркетинг, звонки, встречи, подписание бумаг, проверка сделки, клозинг, поиск финансирования и продажа недвижимости.\n\n'
                '**4) Как быть, если у меня нет капитала и банк не даст мне кредит?**\n'
                '- Креативные стратегии позволяют инвестировать без крупных вложений. Например, в "Subject to" или "Seller Financing" можно купить недвижимость с минимальными затратами. Для pre-foreclosure сделок могут потребоваться небольшие средства на маркетинг, но сам дом можно взять с минимальным платежом ($10-$100)\n\n'
                '**5) Я очень занят, у меня работа, семья. Как я смогу совмещать обучение и инвестиции?**\n'
                '- Наши занятия проходят онлайн и остаются в записи. Их можно изучать в любое удобное время, включая выходные. Мы также даем четкие алгоритмы, которые позволяют работать по 5-10 часов в неделю и уже делать первые сделки.\n\n'
                '**6) Как попасть в закрытый чат Telegram?**\n'
                '- Чат `usabytemamila_chat` доступен только для участников сообщества. Чтобы попасть в него, нужно пройти базовое обучение и показать активность в теме инвестирования\n\n'
                '**7) Можно ли инвестировать в недвижимость в США, если я нахожусь в другой стране?**\n'
                '- Да, это возможно. Мы обучаем, как организовать процесс удаленно: от поиска сделок до закрытия через агентские и нотариальные сервисы. Важно заранее подготовить финансовые и юридические вопросы (наличие счета, LLC, почтовый адрес и т. д.).\n\n'
                '**8) Мне нужна LLC для покупки недвижимости?**\n'
                '- Первые сделки можно делать на физическое лицо, но для масштабирования и налоговой оптимизации рекомендуется открыть LLC.\n\n'
                '**9) Мне нужна лицензия Real Estate Agent, чтобы инвестировать?**\n'
                '- Нет, лицензия агента не обязательна, но понимание рынка недвижимости важно. Мы даем список книг, которые стоит изучить, чтобы лучше разбираться в процессе\n\n')
    faq_text_2 = ('____________________________________________\n\n'
                '**Недвижимость в США и Creative Financing**\n'
                '____________________________________________\n\n'
                '**10) Что такое "Subject to" и почему это работает?**\n'
                '- "Subject to" – это покупка недвижимости с сохранением существующей ипотеки продавца. Это позволяет избежать новых кредитов и получить актив с минимальными вложениями.\n\n'
                '**11) Банки не против сделок "Subject to"? Разве это легально?**\n'
                '- Да, это легально. Если бы это было незаконно, титульные компании не проводили бы такие сделки. Банк продолжает получать платежи по ипотеке, а смена владельца не отменяет обязательства по кредиту. Хотя есть пункт "due on sale clause", на практике банки редко активируют его, если платежи поступают исправно.\n\n'
                '**12) Как инвестировать в недвижимость в США без кредитной истории и SSN?**\n'
                '- Креативные стратегии позволяют обходить необходимость банковского финансирования. "Subject to" и "Seller Financing" работают без участия банков, а LLC можно открыть и без SSN.\n\n'
                '**13) Какие преимущества у "Seller Financing"?**\n'
                '- Это когда продавец сам предоставляет финансирование, минуя банк. Гибкие условия, низкий первоначальный взнос и минимум бюрократии делают этот метод очень выгодным.\n\n'
                '**14) Как покупать недвижимость в США, если я не говорю по-английски?**\n'
                '- Можно нанять виртуального ассистента, который будет вести переговоры. Мы предоставляем готовые сценарии звонков и анкеты, чтобы ваш ассистент мог сразу приступить к работе.\n\n'
                '**15) Какие города США самые перспективные для инвестиций?**\n'
                '- Техас (Даллас, Хьюстон)\n- Флорида (Тампа, Орландо\n- Северная Каролина (Шарлотт)\n- Средний Запад (Огайо, Индиана)\n\n'
                '**16) Где искать мотивированных продавцов недвижимости?**\n'
                '- Мы не берем готовые списки с сайтов. Сделки создаются через маркетинг: рассылки, звонки, таргетированную рекламу. Это требует вложений, но окупается.\n\n')
    faq_text_3 = ('____________________________________________\n\n'
                '**Инвестиции и бизнес в недвижимости**\n'
                '____________________________________________\n\n'
                '**17) Как начать зарабатывать на недвижимости без крупных вложений?**\n'
                '- Сделки по "Subject to" и "Seller Financing".\n- Перепродажа опционов на недвижимость.\n- Партнерство с инвесторами.\n- Флиппинг недвижимости (ремонт + продажа).\n\n'
                '**18) Какие налоги нужно платить с доходов от недвижимости?**\n'
                '- Налоги в США обязательны, но после их уплаты остается достаточно прибыли. Детали зависят от типа сделки и структуры бизнеса, поэтому лучше консультироваться с CPA.\n\n'
                '**19) Как найти первых инвесторов и партнеров?**\n'
                '- Вступайте в наше сообщество, посещайте мероприятия, участвуйте в Zoom-встречах и развивайте личный бренд.\n\n'
                '**20) Можно ли открыть бизнес в США, чтобы заниматься недвижимостью?**\n'
                '- Да, можно зарегистрировать LLC, вести сделки и платить налоги официально.\n\n'
                '**21) Стоит ли начинать обучение, если я переезжаю в США позже?**\n'
                '- Да! Если бы у нас был доступ к таким знаниям до переезда, то первые сделки можно было бы сделать уже в первый год. Гораздо лучше ехать в США с готовой стратегией, чем учиться на ошибках.\n\n'
                '**22) Как принять участие в ваших встречах и конференциях?**\n'
                '- Мы проводим живые мероприятия несколько раз в год в разных городах США. Следите за анонсами в нашем Telegram.')

    text = await escape(faq_text, flag=0)
    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")

    text = await escape(faq_text_2, flag=0)
    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")

    text = await escape(faq_text_3, flag=0)
    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['join_chat'])
async def join_chat_command(message):
    user_id = message.chat.id

    async with async_session() as session:
        user_menu_status = await select_menu_status(session, user_id)

    if user_menu_status >= completed_app_status:
        await bot.send_message(chat_id=user_id, text=await escape("Ваша заявка уже принята. Дождитесь вердикта.", flag=0), parse_mode="MarkdownV2")
    else:
        try:
            text = await escape(lang_dict['first_app_question_txt'], flag=0)
            await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
            async with async_session() as session:
                await update_user_status(session, user_id, first_app_qst_status)
                await update_main_questions_list(session, user_id, "[]")
        except:
            pass


@bot.message_handler(commands=['feedback'])
async def faq_command(message):
    user_id = message.chat.id
    username = message.from_user.username

    async with async_session() as session:
        _check_user = await check_user_exists(session, user_id)
    if not _check_user:
        try:
            current_time = int(time.time())
            await add_user_data(session, user_id, username, current_time)
        except Exception as error:
            print(f"ERROR LOG:\n Adding user to db error: {username}\n{error}")
    else:
        async with async_session() as session:
            await update_username(session, user_id, username)

    async with async_session() as session:
        await update_user_status(session, user_id, feed_back_input_status)

    text = await escape(lang_dict['feedback_txt'], flag=0)
    await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")


@bot.message_handler(commands=['broadcast'])
async def faq_command(message):
    user_id = message.chat.id
    username = message.from_user.username

    if user_id == admins_id:
        text = await escape(lang_dict['broadcast_admin_txt'], flag=0)
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")

        async with async_session() as session:
            await update_broadcast_status(session, broadcast_msg_status)


@bot.message_handler(commands=['send_zoom_invites'])
async def zoom_invites_command(message):
    user_id = message.chat.id
    username = message.from_user.username

    if user_id == admins_id:
        text = await escape(lang_dict['zoom_first_txt'], flag=0)
        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")

        async with async_session() as session:
            await update_zoom_status(session, zoom_date_status)
            await update_zoom_notif24(session, 0)
            await update_zoom_notif1(session, 0)


@bot.message_handler(commands=['add_to_group'])
async def add_to_group_command(message):
    user_id = message.chat.id

    if user_id == admins_id:
        args = message.text.split()
        if len(args) > 1:
            user_id_str = args[1]
            try:
                user_id = int(user_id_str)
            except ValueError:
                await bot.send_message(chat_id=user_id, text="UserID состоит только из чисел.")
                return

        generating_url = await bot.create_chat_invite_link(
            chat_id=group_id,
            name="Одноразовая ссылка",
            expire_date=None,
            member_limit=1,
            creates_join_request=False
        )
        url = generating_url.invite_link

        try:
            text = await escape(lang_dict['app_accepted'].format(url), flag=0)
            await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")

            async with async_session() as session:
                await update_user_status(session, user_id, finalized_app_status)
        except:
            pass


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    user_id = call.message.chat.id
    username = call.message.chat.username
    message_id = call.message.message_id

    if call.data == "back_to_main_menu":
        await bot.answer_callback_query(call.id)
        button_list0 = [
            types.InlineKeyboardButton("Перейти в чат ➡️", callback_data="join_chat"),
        ]
        button_list1 = [
            types.InlineKeyboardButton("Мой UserID", callback_data="user_id"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

        text = await escape(lang_dict['start_msg'], flag=0)

        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )
    elif call.data == "close_menu_window":
        await bot.answer_callback_query(call.id)
        await bot.delete_message(chat_id=user_id, message_id=message_id)

    elif call.data.startswith("custom_quest_1_"):
        await bot.answer_callback_query(call.id)

        data = call.data.split("_")[3]

        if data == "yes":
            async with async_session() as session:
                user_data = await get_all_user_data(session, user_id)

                custom_quest_list = ast.literal_eval(user_data['add_questions'])
                custom_quest_list.append("Да")

                await update_add_questions(session, user_id, str(custom_quest_list))
        elif data == "no":
            async with async_session() as session:
                user_data = await get_all_user_data(session, user_id)

                custom_quest_list = ast.literal_eval(user_data['add_questions'])
                custom_quest_list.append("Нет")

                await update_add_questions(session, user_id, str(custom_quest_list))

        button_list0 = [
            types.InlineKeyboardButton("Инвестирование", callback_data="custom_quest_2_invest"),
        ]
        button_list1 = [
            types.InlineKeyboardButton("Обучение", callback_data="custom_quest_2_learn"),
        ]
        button_list2 = [
            types.InlineKeyboardButton("Работа с нами", callback_data="custom_quest_2_work"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1, button_list2])

        text = await escape(lang_dict['second_custom_question'], flag=0)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )

    elif call.data.startswith("custom_quest_2_"):
        await bot.answer_callback_query(call.id)

        data = call.data.split("_")[3]

        if data == "invest":
            async with async_session() as session:
                user_data = await get_all_user_data(session, user_id)

                custom_quest_list = ast.literal_eval(user_data['add_questions'])
                custom_quest_list.append("Инвестирование")

                await update_add_questions(session, user_id, str(custom_quest_list))
        elif data == "learn":
            async with async_session() as session:
                user_data = await get_all_user_data(session, user_id)

                custom_quest_list = ast.literal_eval(user_data['add_questions'])
                custom_quest_list.append("Обучение")

                await update_add_questions(session, user_id, str(custom_quest_list))
        elif data == "work":
            async with async_session() as session:
                user_data = await get_all_user_data(session, user_id)

                custom_quest_list = ast.literal_eval(user_data['add_questions'])
                custom_quest_list.append("Работа с нами")

                await update_add_questions(session, user_id, str(custom_quest_list))

        button_list0 = [
            types.InlineKeyboardButton("Перейти в чат ➡️", callback_data="join_chat"),
        ]
        button_list1 = [
            types.InlineKeyboardButton("Мой UserID", callback_data="user_id"),
        ]
        reply_markup = types.InlineKeyboardMarkup(
            [button_list0, button_list1])

        text = await escape(lang_dict['start_msg'], flag=0)
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )

    elif call.data == "zoom_invites_send":
        await bot.answer_callback_query(call.id)

        async with async_session() as session:
            all_users_data = await get_all_users(session)
            zoom_data = await get_zoom_invite_data(session)

            date = zoom_data['date']
            time = zoom_data['time']
            url = zoom_data['url']
            topic = zoom_data['topic']

            zoom_msg = (f"**Тема:** {topic}\n"
                        f"**Дата:** `{date}` **|** `{time}` **(UTC-8)**\n"
                        f"**Ссылка:** {url}")


            for user_data in all_users_data:
                user_id = user_data['user_id']
                try:
                    button_list1 = [
                        types.InlineKeyboardButton("Закрыть окно ❌", callback_data="close_menu_window"),
                    ]
                    reply_markup = types.InlineKeyboardMarkup([button_list1])

                    text = await escape(lang_dict['user_warning_zoom_txt'].format(zoom_msg), flag=0)
                    await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                except:
                    pass

    elif call.data == "broadcast_send":
        await bot.answer_callback_query(call.id)

        async with async_session() as session:
            all_users_data = await get_all_users(session)
            broadcast_msg = await select_broadcast_msg(session)

            for user_data in all_users_data:
                user_id = user_data['user_id']

                try:
                    button_list1 = [
                        types.InlineKeyboardButton("Закрыть окно ❌", callback_data="close_menu_window"),
                    ]
                    reply_markup = types.InlineKeyboardMarkup([button_list1])

                    text = await escape(lang_dict['user_warning_broadcast_txt'].format(broadcast_msg), flag=0)
                    await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                except:
                    pass

    elif call.data.startswith("accept_app_"):
        await bot.answer_callback_query(call.id, text="Вы приняли заявку. Пользователю отправлена ссылка на вступление в чат.", show_alert=True)
        user_data = call.data.split("_")
        app_user_id = int(user_data[2])

        async with async_session() as session:
            await update_user_status(session, user_id, finalized_app_status)

        generating_url = await bot.create_chat_invite_link(
            chat_id=group_id,
            name="Одноразовая ссылка",
            expire_date=None,
            member_limit=1,
            creates_join_request=False
        )
        url = generating_url.invite_link

        try:
            button_list1 = [
                types.InlineKeyboardButton("Закрыть окно ❌", callback_data="close_menu_window"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])

            await bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=reply_markup,
            )

            text = await escape(lang_dict['app_accepted'].format(url), flag=0)
            await bot.send_message(chat_id=app_user_id, text=text, parse_mode="MarkdownV2")
        except:
            pass

    elif call.data.startswith("decline_app_"):
        await bot.answer_callback_query(call.id, text="Вы отклонили заявку. Пользователь уведомлен.", show_alert=True)
        user_data = call.data.split("_")
        app_user_id = user_data[2]

        async with async_session() as session:
            await update_user_status(session, user_id, start_status)

        try:
            button_list1 = [
                types.InlineKeyboardButton("Закрыть окно ❌", callback_data="close_menu_window"),
            ]
            reply_markup = types.InlineKeyboardMarkup([button_list1])

            await bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=reply_markup,
            )

            text = await escape(lang_dict['app_declined'], flag=0)
            await bot.send_message(chat_id=app_user_id, text=text, parse_mode="MarkdownV2")
        except:
            pass

    elif call.data == "join_chat":
        async with async_session() as session:
            user_menu_status = await select_menu_status(session, user_id)

        if user_menu_status >= completed_app_status:
            await bot.answer_callback_query(call.id, text="Ваша заявка уже принята. Дождитесь вердикта.", show_alert=True)
        else:
            await bot.answer_callback_query(call.id)
            text = await escape(lang_dict['first_app_question_txt'], flag=0)
            try:
                await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                async with async_session() as session:
                    await update_user_status(session, user_id, first_app_qst_status)
                    await update_main_questions_list(session, user_id, "[]")
            except:
                pass

    elif call.data == "user_id":
        await bot.answer_callback_query(call.id)
        button_list0 = [
            types.InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main_menu"),
        ]
        reply_markup = types.InlineKeyboardMarkup([button_list0])

        text = await escape(lang_dict['user_id_txt'].format(user_id), flag=0)

        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def handle_text(message):
    user_id = message.chat.id
    username = message.chat.username
    try:
        chat_type = message.chat.type

        if chat_type == 'private':

            async with async_session() as session:
                user_menu_status = await select_menu_status(session, user_id)
                broadcast_status = await select_broadcast_status(session)
                zoom_status = await select_zoom_status(session)

            # questions handler
            if user_menu_status == first_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['second_app_question_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, second_app_qst_status)
                except:
                    pass
            elif user_menu_status == second_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['third_app_question_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, third_app_qst_status)
                except:
                    pass
            elif user_menu_status == third_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['fourth_app_question_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, fourth_app_qst_status)
                except:
                    pass
            elif user_menu_status == fourth_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['fifth_app_question_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, fifth_app_qst_status)
                except:
                    pass
            elif user_menu_status == fifth_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['sixth_app_question_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, sixth_app_qst_status)
                except:
                    pass
            elif user_menu_status == sixth_app_qst_status:
                answer_msg = message.text

                text = await escape(lang_dict['completed_app_txt'], flag=0)
                try:
                    await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        user_data = await get_all_user_data(session, user_id)

                        main_questions = ast.literal_eval(user_data['main_questions'])
                        main_questions.append(answer_msg)

                        await update_main_questions_list(session, user_id, str(main_questions))
                        await update_user_status(session, user_id, completed_app_status)
                except:
                    pass
            # feedback handler
            elif user_menu_status == feed_back_input_status:
                feedback_msg = message.text

                text = await escape(lang_dict['feedback_admin_txt'].format(user_id, username, feedback_msg), flag=0)
                try:
                    await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        await update_user_status(session, user_id, start_status)
                except:
                    pass


            #  broadcast handler
            if user_id == admins_id and broadcast_status == broadcast_msg_status:
                broadcast_msg = message.text

                async with async_session() as session:
                    await update_broadcast_msg(session, broadcast_msg)

                button_list0 = [
                    types.InlineKeyboardButton("Отправить 📤", callback_data="broadcast_send"),
                ]
                button_list1 = [
                    types.InlineKeyboardButton("Отмена ❌", callback_data="close_menu_window"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

                text = await escape(lang_dict['broadcast_admin_txt_recheck'].format(broadcast_msg), flag=0)

                try:
                    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        await update_broadcast_status(session, broadcast_msg_zero_status)
                except:
                    pass

            # zoom_invites handler
            if user_id == admins_id and zoom_status == zoom_date_status:
                zoom_date_msg = message.text

                date_verdict = await is_valid_date(zoom_date_msg)

                if date_verdict == True:
                    async with async_session() as session:
                        await update_zoom_date(session, zoom_date_msg)
                        await update_zoom_status(session, zoom_time_status)

                    try:
                        text = await escape(lang_dict['zoom_second_txt'], flag=0)
                        await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                    except:
                        pass
                else:
                    try:
                        text = await escape("Неверно указанная дата.\nПопробуйте еще раз (Формат: dd.mm.yy) ⬇️", flag=0)
                        await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                        # async with async_session() as session:
                        #     await update_zoom_status(session, zoom_zero_status)
                    except:
                        pass
            elif user_id == admins_id and zoom_status == zoom_time_status:
                zoom_time_msg = message.text

                time_verdict = await is_valid_time(zoom_time_msg)

                if time_verdict == True:
                    async with async_session() as session:
                        await update_zoom_time(session, zoom_time_msg)
                        await update_zoom_status(session, zoom_url_status)

                    try:
                        text = await escape(lang_dict['zoom_third_txt'], flag=0)
                        await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                    except:
                        pass
                else:
                    try:
                        text = await escape("Неверно указано время.\nПопробуйте еще раз (Формат: 12:37, 22:15, 08:05) ⬇️", flag=0)
                        await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                        # async with async_session() as session:
                        #     await update_zoom_status(session, zoom_zero_status)
                    except:
                        pass
            elif user_id == admins_id and zoom_status == zoom_url_status:
                zoom_url_msg = message.text

                url_verdict = await is_valid_url(zoom_url_msg)

                if url_verdict == True:
                    async with async_session() as session:
                        await update_zoom_url(session, zoom_url_msg)
                        await update_zoom_status(session, zoom_topic_status)

                    try:
                        text = await escape(lang_dict['zoom_fourth_txt'], flag=0)
                        await bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")
                    except:
                        pass
                else:
                    try:
                        text = await escape("Это не url адрес.\nВведите еще раз ⬇️", flag=0)
                        await bot.send_message(chat_id=admins_id, text=text, parse_mode="MarkdownV2")
                        # async with async_session() as session:
                        #     await update_zoom_status(session, zoom_zero_status)
                    except:
                        pass
            elif user_id == admins_id and zoom_status == zoom_topic_status:
                zoom_topic_msg = message.text

                async with async_session() as session:
                    await update_zoom_topic(session, zoom_topic_msg)
                    await update_zoom_status(session, zoom_zero_status)
                    zoom_data = await get_zoom_invite_data(session)

                date = zoom_data['date']
                time = zoom_data['time']
                url = zoom_data['url']
                topic = zoom_data['topic']

                zoom_msg = (f"Тема: {topic}\n\n"
                            f"Дата: `{date}` | `{time}`\n"
                            f"Ссылка: {url}")

                button_list0 = [
                    types.InlineKeyboardButton("Отправить 📤", callback_data="zoom_invites_send"),
                ]
                button_list1 = [
                    types.InlineKeyboardButton("Отмена ❌", callback_data="close_menu_window"),
                ]
                reply_markup = types.InlineKeyboardMarkup([button_list0, button_list1])

                text = await escape(lang_dict['zoom_admin_txt_recheck'].format(zoom_msg), flag=0)

                try:
                    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                    async with async_session() as session:
                        await update_broadcast_status(session, broadcast_msg_zero_status)
                except:
                    pass
    except:
        pass


async def is_valid_url(url_str):
    try:
        result = urlparse(url_str)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


async def is_valid_date(date_str):
    try:
        x_date = datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except Exception as e:
        print(e)
        return False


async def is_valid_time(time_str):
    try:
        x_time = datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


async def time_registered_notif():
    while True:
        try:
            async with async_session() as session:
                all_users_data = await get_all_users(session)

                for user_data in all_users_data:
                    user_id = user_data['user_id']
                    app_status = int(user_data['app_status'])
                    time_register = int(user_data['time_register'])
                    notif24_status = user_data['notif24']
                    notif48_status = user_data['notif48']

                    current_server_time = int(time.time())

                    time_diff = current_server_time - time_register


                    if app_status < completed_app_status:
                        if notif24_status == 0 and time_diff >= 86400:
                            try:
                                text = await escape(lang_dict['user_repeat_notif'].format(admin_username), flag=0)
                                await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                            except:
                                pass
                            async with async_session() as session:
                                await update_notif24(session, user_id)

                        if notif24_status == 1 and notif48_status == 0 and time_diff >= 172800:
                            try:
                                text = await escape(lang_dict['user_repeat_notif'].format(admin_username), flag=0)
                                await bot.send_message(chat_id=user_id, text=text, parse_mode="MarkdownV2")
                            except:
                                pass
                            async with async_session() as session:
                                await update_notif48(session, user_id)

        except:
            pass
        await asyncio.sleep(3600)


async def zoom_invites_notif():
    while True:
        try:
            async with async_session() as session:
                all_users_data = await get_all_users(session)
                zoom_data = await get_zoom_invite_data(session)

                date = zoom_data['date']
                time = zoom_data['time']
                url = zoom_data['url']
                topic = zoom_data['topic']
                notify24 = zoom_data['notify24']
                notify1 = zoom_data['notify1']

            if len(date) > 0 and len(time) > 0 and len(url) > 0 and len(topic) > 0:
                zoom_msg = (f"**Тема:** {topic}\n"
                            f"**Дата:** `{date}` **|** `{time}` **(UTC-8)**\n"
                            f"**Ссылка:** {url}")

                text = await escape(lang_dict['user_warning_zoom_txt'].format(zoom_msg), flag=0)

                tz_utc_minus8 = datetime.timezone(timedelta(hours=-8))
                zoom_datetime = datetime.strptime(f"{date} {time}", "%d.%m.%Y %H:%M")
                zoom_datetime = zoom_datetime.replace(tzinfo=tz_utc_minus8)
                now = datetime.now(tz_utc_minus8)
                time_diff = zoom_datetime - now

                if notify24 == 0 and time_diff > timedelta(0) and time_diff <= timedelta(hours=24):
                    for user_data in all_users_data:
                        user_id = user_data['user_id']

                        button_list0 = [
                            types.InlineKeyboardButton("Закрыть ❌", callback_data="close_menu_window"),
                        ]
                        reply_markup = types.InlineKeyboardMarkup([button_list0])
                        try:
                            await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                        except:
                            pass
                    async with async_session() as session:
                        await update_zoom_notif24(session, 1)

                if notify1 == 0 and time_diff > timedelta(0) and time_diff <= timedelta(hours=1):
                    for user_data in all_users_data:
                        user_id = user_data['user_id']

                        button_list0 = [
                            types.InlineKeyboardButton("Закрыть ❌", callback_data="close_menu_window"),
                        ]
                        reply_markup = types.InlineKeyboardMarkup([button_list0])

                        try:
                            await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                        except:
                            pass
                    async with async_session() as session:
                        await update_zoom_notif1(session, 1)
        except:
            pass

        await asyncio.sleep(1800)


async def completed_apps_mailing():
    while True:
        try:
            async with async_session() as session:
                all_users_data = await get_all_users(session)


            for user_data in all_users_data:
                user_id = user_data['user_id']
                username = user_data['username']
                app_status = int(user_data['app_status'])
                main_questions = ast.literal_eval(user_data['main_questions'])
                custom_answers = ast.literal_eval(user_data['add_questions'])


                if app_status == completed_app_status:

                    quest_msg = ""
                    quest_counter = 1
                    for quest in main_questions:
                        quest_msg += f"{quest_counter}) {quest}\n"
                        quest_counter += 1

                    segment_txt = ""
                    segment_counter = 1
                    for custom_answer in custom_answers:
                        if segment_counter == 1:
                            segment_txt += f"Сегментирующие вопросы:\n{segment_counter}) Вы уже работаете с недвижимостью США?\n- {custom_answer}\n"
                        elif segment_counter == 2:
                            segment_txt += f"{segment_counter}) Какие аспекты для вас наиболее интересны?\n- {custom_answer}"
                        segment_counter += 1

                    button_list0 = [
                        types.InlineKeyboardButton("Принять 🟢", callback_data=f"accept_app_{user_id}"),
                        types.InlineKeyboardButton("Отклонить 🔴", callback_data=f"decline_app_{user_id}"),

                    ]

                    reply_markup = types.InlineKeyboardMarkup([button_list0])


                    pre_text = ("✅ **Новая пользовательская заявка** ✅\n\n"
                                f"User🆔: `{user_id}`\n"
                                f"Username: @{username}\n"
                                f"{quest_msg}\n\n"
                                f"{segment_txt}")
                    text = await escape(pre_text, flag=0)
                    try:
                        await bot.send_message(chat_id=admins_id, text=text, reply_markup=reply_markup, parse_mode="MarkdownV2")
                    except:
                        pass
                    async with async_session() as session:
                        await update_user_status(session, user_id, examination_app_status)
        except:
            pass
        await asyncio.sleep(1)


async def main():
    bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=120))
    register_monitoring = asyncio.create_task(time_registered_notif())
    app_examination = asyncio.create_task(completed_apps_mailing())
    zoom_invites = asyncio.create_task(zoom_invites_notif())
    await asyncio.gather(bot_task, register_monitoring, app_examination, zoom_invites)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

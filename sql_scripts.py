import logging
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, class_mapper
from sqlalchemy import Column, Integer, String, BigInteger, Float, insert, update, delete, Float
from sqlalchemy import select
from datetime import datetime, timedelta
from config import *


Base = declarative_base()


engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    main_questions = Column(String)
    add_questions = Column(String)
    app_status = Column(Integer)
    time_register = Column(Integer)
    notif24 = Column(Integer)
    notif48 = Column(Integer)



class Broadcast(Base):
    __tablename__ = 'broadcast_notify'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    status = Column(Integer)


class ZoomNotify(Base):
    __tablename__ = 'zoom_notify'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    time = Column(String)
    url = Column(String)
    topic = Column(String)
    status = Column(Integer)
    notify24 = Column(Integer)
    notify1 = Column(Integer)


async def add_user_data(session: AsyncSession, user_id, username, current_time):
    user_data = {
        "user_id": user_id,
        "username": username,
        "main_questions": "[]",
        "add_questions": "[]",
        "app_status": 0,
        "time_register": current_time,
        "notif24": 0,
        "notif48": 0,
    }

    new_user = User(**user_data)
    session.add(new_user)
    await session.commit()


async def select_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.user_id == user_id))
    return result.scalars().first()


async def check_user_exists(session: AsyncSession, user_id: int) -> bool:
    user = await select_user(session, user_id)
    return user is not None



async def update_username(session: AsyncSession, user_id: int, new_username: str):
    values = {"username": new_username}
    await session.execute(
        update(User).where(User.user_id == user_id).values(**values)
    )
    await session.commit()


async def update_add_questions(session: AsyncSession, user_id: int, quest_list):
    values = {"add_questions": quest_list}
    await session.execute(
        update(User).where(User.user_id == user_id).values(**values)
    )
    await session.commit()


async def update_zoom_date(session: AsyncSession, zoom_date):
    new_data = {f"date": zoom_date}
    await session.execute(
        update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data)
    )
    await session.commit()


async def update_zoom_time(session: AsyncSession, zoom_time):
    new_data = {f"time": zoom_time}
    await session.execute(
        update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data)
    )
    await session.commit()


async def update_zoom_url(session: AsyncSession, zoom_url):
    new_data = {f"url": zoom_url}
    await session.execute(
        update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data)
    )
    await session.commit()


async def update_zoom_topic(session: AsyncSession, zoom_topic):
    new_data = {f"topic": zoom_topic}
    await session.execute(
        update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data)
    )
    await session.commit()


async def update_zoom_status(session: AsyncSession, status):
    new_data = {f"status": status}
    await session.execute(
        update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data)
    )
    await session.commit()


async def update_broadcast_status(session: AsyncSession, status):
    new_data = {f"status": status}
    await session.execute(
        update(Broadcast).where(Broadcast.name == "broadcast_notification").values(**new_data)
    )
    await session.commit()


async def update_broadcast_msg(session: AsyncSession, msg_text):
    new_data = {f"text": msg_text}
    await session.execute(
        update(Broadcast).where(Broadcast.name == "broadcast_notification").values(**new_data)
    )
    await session.commit()


async def update_user_status(session: AsyncSession, user_id, status):
    new_data = {f"app_status": status}
    await session.execute(
        update(User).where(User.user_id == int(user_id)).values(**new_data)
    )
    await session.commit()


async def update_main_questions_list(session: AsyncSession, user_id, question_list):
    new_data = {f"main_questions": question_list}
    await session.execute(update(User).where(User.user_id == int(user_id)).values(**new_data))
    await session.commit()


async def update_notif24(session: AsyncSession, user_id):
    new_data = {f"notif24": 1}
    await session.execute(update(User).where(User.user_id == int(user_id)).values(**new_data))
    await session.commit()


async def update_notif48(session: AsyncSession, user_id):
    new_data = {f"notif48": 1}
    await session.execute(update(User).where(User.user_id == int(user_id)).values(**new_data))
    await session.commit()


async def update_zoom_notif24(session: AsyncSession, status):
    new_data = {f"notify24": status}
    await session.execute(update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data))
    await session.commit()


async def update_zoom_notif1(session: AsyncSession, status):
    new_data = {f"notify1": status}
    await session.execute(update(ZoomNotify).where(ZoomNotify.name == "zoom_notification").values(**new_data))
    await session.commit()


async def select_menu_status(session: AsyncSession, user_id: int) -> int:
    result = await session.execute(select(User.app_status).where(User.user_id == user_id))
    return result.scalars().first()


async def select_broadcast_status(session: AsyncSession):
    result = await session.execute(select(Broadcast.status).where(Broadcast.name == "broadcast_notification"))
    return result.scalars().first()


async def select_zoom_status(session: AsyncSession):
    result = await session.execute(select(ZoomNotify.status).where(ZoomNotify.name == "zoom_notification"))
    return result.scalars().first()


async def select_broadcast_msg(session: AsyncSession):
    result = await session.execute(select(Broadcast.text).where(Broadcast.name == "broadcast_notification"))
    return result.scalars().first()


async def get_all_user_data(session: AsyncSession, user_id):
    query = select(User).where(User.user_id == int(user_id))
    result = await session.execute(query)
    user_data = result.scalars().first()

    if user_data:
        return {column.key: getattr(user_data, column.key) for column in class_mapper(User).columns}
    else:
        return None


async def get_zoom_invite_data(session: AsyncSession):
    query = select(ZoomNotify).where(ZoomNotify.name == "zoom_notification")
    result = await session.execute(query)
    zoom_data = result.scalars().first()

    if zoom_data:
        return {column.key: getattr(zoom_data, column.key) for column in class_mapper(ZoomNotify).columns}
    else:
        return None


async def get_all_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    user_data = result.fetchall()

    if user_data:
        return [
            {column.key: getattr(row.User, column.key) for column in class_mapper(User).columns}
            for row in user_data
        ]
    else:
        return None

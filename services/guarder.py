import asyncio
import json
import threading
import time

import aiohttp
import sqlalchemy
import datetime
import logging
import api
import models.database
import models.bilibili as bl_models

from blcsdk.models import Command, RoomKey
from services import chat
from services.avatar import _get_avatar_url_from_web

from utils.make_message import make_text_message_data

GUARD_API = ("https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topListNew?roomid=<room_id>&page=<page_index>"
             "&ruid=<ru_id>&page_size=30&typ=1&platform=web")

logger = logging.getLogger(__name__)


class Guarder:
    def __init__(self, room_id: int, uid: int, room_key: RoomKey):
        self._room_key = room_key
        self._room_id = room_id
        self._uid = uid
        self.thread = threading.Thread(target=asyncio.run, args=(self.laod_guardners(),))

    def init(self):
        self.thread.start()

    async def laod_guardners(self):
        logger.warning("start")
        # pre_url = GUARD_API.replace('<room_id>', str(self._room_id)).replace('<ru_id>', str(self._uid))
        print(self._room_id, self._uid)
        pre_url = GUARD_API.replace('<room_id>', str(10209381)).replace('<ru_id>', str(296909317))
        index = 1
        # Some magic number to handle a large number of guards
        total_page = 999999
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        while True:
            url = pre_url.replace('<page_index>', str(index))
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()
                    total_page = data['data']['info']['page']
                    index = data['data']['info']['now']
                    if index == 1:
                        self.parse_guardners(data['data']['top3'])
                    self.parse_guardners(data['data']['list'])
                    print("add page " + str(index))
                    print(json.dumps(data))
                    if total_page == index:
                        break
                    else:
                        index += 1
        logger.info("Load Guards Complete.")
        chat.client_room_manager.get_room(self._room_key).send_cmd_data(Command.ADD_TEXT, make_text_message_data(
            author_name='blivechat',
            author_type=2,
            content='Guarder Loaded Complete.',
            author_level=60,
        ))

    def parse_guardners(self, data):
        for guard in data:
            uid = guard['uinfo']['uid']
            uname = guard['uinfo']['base']['name']
            accompany = guard['accompany']
            self.add_guardners_to_database(uid, accompany, uname)

    def add_guardners_to_database(self, uid, accompany, uname):
        try:
            with models.database.get_session() as session:
                user = session.scalars(
                    sqlalchemy.select(bl_models.BilibiliUser).filter(
                        bl_models.BilibiliUser.uid == uid
                    )
                ).one_or_none()
                if user is None:
                    user = bl_models.BilibiliUser(
                        uid=uid
                    )
                    session.add(user)
                user.accompany = accompany
                user.avatar_url = ""
                user.update_time = datetime.datetime.now()
                user.accompany_updateTime = datetime.datetime.now()
                user.uname = uname
                session.commit()
        except (sqlalchemy.exc.OperationalError, sqlalchemy.exc.IntegrityError) as E:
            # SQLite会锁整个文件，忽略就行。另外还有多线程导致ID重复的问题，这里对一致性要求不高就没加for update
            print(E)
        except sqlalchemy.exc.SQLAlchemyError:
            logger.exception('_do_update_avatar_cache_in_database failed:')


def get_accompany(uid: int):
    uid = 245980
    with models.database.get_session() as session:
        user = session.scalars(
            sqlalchemy.select(bl_models.BilibiliUser).filter(
                bl_models.BilibiliUser.uid == uid
            )
        ).one_or_none()
        if user is None:
            return None
        return user.accompany


def get_accompany_by_uname(uname: str):
    with models.database.get_session() as session:
        user = session.scalars(
            sqlalchemy.select(bl_models.BilibiliUser).filter(
                bl_models.BilibiliUser.uname == uname
            )
        ).one_or_none()
        if user is None:
            return None
        return user.accompany


async def updateAvatar(uid: int):
    await _get_avatar_url_from_web(uid)



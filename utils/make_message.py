import enum
import time
import uuid


class ContentType(enum.IntEnum):
    TEXT = 0
    EMOTICON = 1


DEFAULT_AVATAR_URL = '//static.hdslb.com/images/member/noface.gif'


def make_text_message_data(
        avatar_url: str = DEFAULT_AVATAR_URL,
        timestamp: int = None,
        author_name: str = '',
        author_type: int = 0,
        content: str = '',
        privilege_type: int = 0,
        is_gift_danmaku: bool = False,
        author_level: int = 1,
        is_newbie: bool = False,
        is_mobile_verified: bool = True,
        medal_level: int = 0,
        id_: str = None,
        translation: str = '',
        content_type: int = ContentType.TEXT,
        content_type_params: list = None,
        uid: str = '',
        medal_name: str = '',
        accompany: int = None
):
    # 为了节省带宽用list而不是dict
    return [
        # 0: avatarUrl
        avatar_url,
        # 1: timestamp
        timestamp if timestamp is not None else int(time.time()),
        # 2: authorName
        author_name,
        # 3: authorType
        author_type,
        # 4: content
        content,
        # 5: privilegeType
        privilege_type,
        # 6: isGiftDanmaku
        1 if is_gift_danmaku else 0,
        # 7: authorLevel
        author_level,
        # 8: isNewbie
        1 if is_newbie else 0,
        # 9: isMobileVerified
        1 if is_mobile_verified else 0,
        # 10: medalLevel
        medal_level,
        # 11: id
        id_ if id_ is not None else uuid.uuid4().hex,
        # 12: translation
        translation,
        # 13: contentType
        content_type,
        # 14: contentTypeParams
        content_type_params if content_type_params is not None else [],
        # 15: textEmoticons
        [],  # 已废弃，保留
        # 16: uid
        uid,
        # 17: medalName
        medal_name,
        # 18, accompany
        accompany
    ]

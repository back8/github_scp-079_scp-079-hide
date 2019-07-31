# SCP-079-HIDE - Hide the real watcher
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-HIDE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import Optional, Union

from pyrogram import Client, InlineKeyboardMarkup, Message
from pyrogram.errors import ChannelInvalid, ChannelPrivate, FloodWait, PeerIdInvalid

from .etc import wait_flood

# Enable logging
logger = logging.getLogger(__name__)


def send_message(client: Client, cid: int, text: str, mid: int = None,
                 markup: InlineKeyboardMarkup = None) -> Optional[Union[bool, Message]]:
    # Send a message to a chat
    result = None
    try:
        if text.strip():
            text_list = [text[i:i + 4096] for i in range(0, len(text), 4096)]
            for text_unit in text_list:
                flood_wait = True
                while flood_wait:
                    flood_wait = False
                    try:
                        result = client.send_message(
                            chat_id=cid,
                            text=text_unit,
                            parse_mode="html",
                            disable_web_page_preview=True,
                            reply_to_message_id=mid,
                            reply_markup=markup
                        )
                    except FloodWait as e:
                        flood_wait = True
                        wait_flood(e)
                    except (PeerIdInvalid, ChannelInvalid, ChannelPrivate):
                        return False
    except Exception as e:
        logger.warning(f"Send message to {cid} error: {e}", exc_info=True)

    return result

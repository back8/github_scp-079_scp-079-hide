# SCP-079-HIDE - Hide the real sender
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
import pickle
from json import loads
from typing import Any

from pyrogram import Client, Message

from .. import glovar
from .etc import bold, code, get_text, lang, thread, user_mention
from .file import crypt_file, delete_file, get_downloaded_path, get_new_path
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def receive_file_data(client: Client, message: Message, decrypt: bool = True) -> Any:
    # Receive file's data from exchange channel
    data = None
    try:
        if not message.document:
            return None

        file_id = message.document.file_id
        file_ref = message.document.file_ref
        path = get_downloaded_path(client, file_id, file_ref)

        if not path:
            return None

        if decrypt:
            # Decrypt the file, save to the tmp directory
            path_decrypted = get_new_path()
            crypt_file("decrypt", path, path_decrypted)
            path_final = path_decrypted
        else:
            # Read the file directly
            path_decrypted = ""
            path_final = path

        with open(path_final, "rb") as f:
            data = pickle.load(f)

        for f in {path, path_decrypted}:
            thread(delete_file, (f,))
    except Exception as e:
        logger.warning(f"Receive file error: {e}", exc_info=True)

    return data


def receive_help_send(client: Client, message: Message, data: int) -> bool:
    # Receive help send
    try:
        cid = data
        text = receive_file_data(client, message)
        if text:
            thread(send_message, (client, cid, text))
    except Exception as e:
        logger.warning(f"Receive help send error: {e}", exc_info=True)

    return False


def receive_text_data(message: Message) -> dict:
    # Receive text's data from exchange channel
    data = {}
    try:
        text = get_text(message)
        if text:
            data = loads(text)
    except Exception as e:
        logger.warning(f"Receive data error: {e}")

    return data


def receive_version_reply(client: Client, sender: str, data: dict) -> bool:
    # Receive version reply
    try:
        aid = data["admin_id"]
        mid = data["message_id"]
        version = data["version"]
        text = (f"{lang('admin')}{lang('colon')}{user_mention(aid)}\n\n"
                f"{lang('project')}{lang('colon')}{code(sender)}\n"
                f"{lang('version')}{lang('colon')}{bold(version)}\n")
        thread(send_message, (client, glovar.test_group_id, text, mid))

        return True
    except Exception as e:
        logger.warning(f"Receive version reply error: {e}", exc_info=True)

    return False

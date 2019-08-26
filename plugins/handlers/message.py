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

from pyrogram import Client, Filters, Message

from .. import glovar
from ..functions.channel import exchange_to_hide
from ..functions.etc import bold, code, thread, user_mention
from ..functions.filters import exchange_channel, hide_channel
from ..functions.receive import receive_text_data
from ..functions.telegram import forward_messages, send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.channel & hide_channel
                   & ~Filters.command(glovar.all_commands, glovar.prefix), group=-1)
def exchange_emergency(_: Client, message: Message):
    # Sent emergency channel transfer request
    try:
        # Read basic information
        data = receive_text_data(message)
        if data:
            sender = data["from"]
            receivers = data["to"]
            action = data["action"]
            action_type = data["type"]
            data = data["data"]
            if "EMERGENCY" in receivers:
                if action == "backup":
                    if action_type == "hide":
                        if data is True:
                            glovar.should_hide = data
                        elif data is False and sender == "MANAGE":
                            glovar.should_hide = data
    except Exception as e:
        logger.warning(f"Exchange emergency error: {e}", exc_info=True)


@Client.on_message(Filters.incoming & Filters.channel & exchange_channel
                   & ~Filters.command(glovar.all_commands, glovar.prefix))
def forward_others_data(client: Client, message: Message):
    # Forward message from other bots to WATCH
    try:
        if not glovar.should_hide:
            data = receive_text_data(message)
            if data:
                receivers = data["to"]
                if "WATCH" in receivers:
                    cid = glovar.hide_channel_id
                    fid = message.chat.id
                    mid = message.message_id
                    if forward_messages(client, cid, fid, [mid], True) is False:
                        exchange_to_hide(client)
    except Exception as e:
        logger.warning(f"Forward regex data error: {e}", exc_info=True)


@Client.on_message(Filters.incoming & Filters.channel & hide_channel
                   & ~Filters.command(glovar.all_commands, glovar.prefix))
def forward_watch_data(client: Client, message: Message):
    # Forward message from WATCH to other bots
    try:
        if not glovar.should_hide:
            data = receive_text_data(message)
            if data:
                sender = data["from"]
                receivers = data["to"]
                action = data["action"]
                action_type = data["type"]
                data = data["data"]
                if sender == "WATCH":
                    # Send version text to TEST group
                    if glovar.sender in receivers:
                        if action == "version":
                            if action_type == "reply":
                                admin_id = data["admin_id"]
                                message_id = data["message_id"]
                                version = data["version"]
                                text = (f"管理员：{user_mention(admin_id)}\n\n"
                                        f"发送者：{code('WATCH')}\n"
                                        f"版本：{bold(version)}\n")
                                thread(send_message, (client, glovar.test_group_id, text, message_id))
                    # Forward regular exchange text
                    else:
                        cid = glovar.exchange_channel_id
                        fid = message.chat.id
                        mid = message.message_id
                        if forward_messages(client, cid, fid, [mid], True) is False:
                            exchange_to_hide(client)
    except Exception as e:
        logger.warning(f"Forward watch data error: {e}", exc_info=True)

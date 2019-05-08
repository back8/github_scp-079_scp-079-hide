# SCP-079-WATCH-HIDE - Hide the real watcher
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-WATCH-HIDE.
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

from pyrogram import Filters, Message

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def is_exchange_channel(_, message: Message) -> bool:
    # Check if this message is sent from exchange channel
    cid = message.chat.id
    if cid == glovar.exchange_channel_id:
        return True

    return False


def is_hide_channel(_, message: Message) -> bool:
    # Check if this message is sent from hide channel
    cid = message.chat.id
    if cid == glovar.hide_channel_id:
        return True

    return False


def is_test_group(_, message: Message) -> bool:
    # Check if this message is sent from test group
    cid = message.chat.id
    if cid == glovar.test_group_id:
        return True

    return False


exchange_channel = Filters.create(
    name="Exchange Channel",
    func=is_exchange_channel
)


hide_channel = Filters.create(
    name="Hide Channel",
    func=is_hide_channel
)

test_group = Filters.create(
    name="Test Group",
    func=is_test_group
)

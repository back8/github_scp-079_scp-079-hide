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
from time import sleep

from pyrogram import Client, Filters
from pyrogram.errors import FloodWait

from .. import glovar
from ..functions.filters import hide_channel

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.channel & hide_channel
                   & ~Filters.command(glovar.all_commands, glovar.prefix))
def forward_data(_, message):
    try:
        flood_wait = True
        while flood_wait:
            flood_wait = False
            try:
                message.forward(
                    chat_id=glovar.exchange_channel_id,
                    as_copy=True
                )
            except FloodWait as e:
                flood_wait = True
                sleep(e.x + 1)
    except Exception as e:
        logger.warning(f"Forward data error: {e}", exc_info=True)

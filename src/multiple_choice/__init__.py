# Multiple Choice for Anki
#
# Copyright (C) 2018-2020  zjosua <https://github.com/zjosua>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from aqt import gui_hooks, mw

from .main import *
from .sc_template import initializeSCModels

def delayedInit():
    initializeSCModels()

gui_hooks.profile_did_open.append(delayedInit)
gui_hooks.webview_did_receive_js_message.append(on_js_message)
gui_hooks.card_will_show.append(prepare_answer)
mw._multiple_choice = MultipleChoice()

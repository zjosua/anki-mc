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

import re

from aqt import mw
from aqt.reviewer import Reviewer


class MultipleChoice:

    def __init__(self):
        self.qtable = ""
        self.solution = ""
        self.user_sel = ""

# Responding to JS messages
def on_js_message(handled, msg, context):
    if not isinstance(context, Reviewer):
        return handled

    if msg.startswith("mc_user_sel:"):
        # Get the question table
        qtable_pattern = re.compile(r"qtable:(.*?);;",
                                    re.MULTILINE | re.DOTALL)
        mo = qtable_pattern.search(msg)
        mw._multiple_choice.qtable = mo.group(1)

        # Get the user's answer
        ans_pattern = re.compile(r"mc_user_sel:(.*?);")
        mo = ans_pattern.search(msg)
        mw._multiple_choice.user_sel = mo.group(1)

        # Get the correct solution
        s_pattern = re.compile(r"mc_soultions:(.*?);")
        mo = s_pattern.search(msg)
        mw._multiple_choice.solution = mo.group(1)

        return True, None

    return handled

# Insert user selection and solutions on the back
def prepare_answer(a, c, kind):
    if c.model()["name"] not in ["Single Choice", "Multiple Choice", "Kprim"]:
        return a
    if kind != "reviewAnswer":
        return a

    # Insert question table
    qtable_pattern = re.compile(r"qtable_here")
    a = qtable_pattern.sub(mw._multiple_choice.qtable, a)

    # Insert user answers
    ans_pattern = re.compile(r"user_answers_here")
    a = ans_pattern.sub(mw._multiple_choice.user_sel, a)

    # Insert solutions
    s_pattern = re.compile(r"solutions_here")
    a = s_pattern.sub(mw._multiple_choice.solution, a)
    return a

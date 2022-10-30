# Multiple Choice for Anki
#
# Copyright (C) 2018-2022  zjosua <https://github.com/zjosua>
#
# This file is based on template.py from Glutanimate's
# Cloze Overlapper Add-on for Anki
#
# Copyright (C)  2016-2019 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Manages note type and templates
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import re

from anki.consts import MODEL_STD
from aqt import (mw, Collection)

aio_model = "AllInOne (kprim, mc, sc)"
aio_card = "AllInOne (kprim, mc, sc)"
aio_fields = {
    "question": "Question",
    "title": "Title",
    "qtype": "QType (0=kprim,1=mc,2=sc)",
    "q1": "Q_1",
    "q2": "Q_2",
    "q3": "Q_3",
    "q4": "Q_4",
    "q5": "Q_5",
    "answers": "Answers",
    "sources": "Sources",
    "extra": "Extra 1"
}


def getOptionsJavaScriptFromConfig(user_config):
    return (
        "const OPTIONS = {\n"
        "    qtable: {\n"
        f"        visible: true,\n"
        f"        colorize: {user_config['colorQuestionTable']},\n"
        f"        colors: {user_config['answerColoring']}\n"
        "    },\n"
        "    atable: {\n"
        f"        visible: {'false' if user_config['hideAnswerTable'] == 'true' else 'true'},\n"
        f"        colorize: {user_config['colorAnswerTable']},\n"
        f"        colors: {user_config['answerColoring']}\n"
        "    }\n"
        "};\n"
    )


def fillTemplateAndModelFromFile(template, model, user_config={}):
    addonFolderName = mw.addonManager.addonFromModule(__name__)
    addonPath = mw.addonManager.addonsFolder() + '/' + addonFolderName + '/'

    if user_config:
        options_java_script = getOptionsJavaScriptFromConfig(user_config)

    with open(addonPath + 'card/front.html', encoding="utf-8") as f:
        template['qfmt'] = f.read()
    with open(addonPath + 'card/back.html', encoding="utf-8") as f:
        back_template = f.read()
        if user_config:
            back_template = re.sub(
                r'const OPTIONS.*?;', options_java_script, back_template, 1, re.DOTALL)
        template['afmt'] = back_template
    with open(addonPath + 'card/css.css', encoding="utf-8") as f:
        model['css'] = f.read()


def addModel(col: Collection):
    """Add add-on note type to collection"""
    models = col.models
    model = models.new(aio_model)
    model['type'] = MODEL_STD
    # Add fields:
    for i in aio_fields.keys():
        fld = models.new_field(aio_fields[i])
        models.add_field(model, fld)
    # Add template
    template = models.new_template(aio_card)

    fillTemplateAndModelFromFile(template, model)

    model['sortf'] = 0  # set sortfield to question
    models.add_template(model, template)
    models.add(model)
    return model


def updateTemplate(col: Collection, user_config={}):
    """Update add-on note templates"""
    print(f"Updating {aio_model} note template")
    model = col.models.by_name(aio_model)
    template = model['tmpls'][0]

    fillTemplateAndModelFromFile(template, model, user_config)

    col.models.save(model)
    return model

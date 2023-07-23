# Multiple Choice for Anki
#
# Copyright (C) 2018-2023  3ter <https://github.com/3ter>
#                          zjosua <https://github.com/zjosua>
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
Manages note type and card templates
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import re
from enum import Enum
from functools import cache
from typing import Any

from anki.consts import MODEL_STD
from aqt import Collection, fields, mw

from .config import *
from .packaging import version

aio_model_name = "AllInOne (kprim, mc, sc)"
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
    "extra": "Extra 1",
}

QUESTION_ID_PATTERN = r"^Q_(\d+)$"
DEFAULT_NUMBER_OF_QUESTIONS = 5


class Template_side(Enum):
    FRONT = 1
    BACK = 2


def get_addon_name() -> str:
    return mw.addonManager.addonFromModule(__name__)


def get_addon_path() -> str:
    return mw.addonManager.addonsFolder() + "/" + get_addon_name() + "/"


def getOptionsJavaScriptFromConfig(user_config, side: Template_side):
    """Get OPTIONS string to write into JavaScript on card template.

    Boolean values differ in Python ('True') VS JavaScript ('true') so they
    need to be converted.
    """

    user_config_front_options_javascript = (
        "\n".join(
            [
                "const OPTIONS = {",
                f"    maxQuestionsToShow: {user_config['maxQuestionsToShow']}",
                "};",
            ]
        )
        + "\n"
    )
    user_config_back_options_javascript = (
        "const OPTIONS = {\n"
        "    qtable: {\n"
        f"        visible: true,\n"
        f"        colorize: {'true' if user_config['colorQuestionTable'] else 'false'},\n"
        f"        colors: {user_config['answerColoring']}\n"
        "    },\n"
        "    atable: {\n"
        f"        visible: {'false' if user_config['hideAnswerTable'] else 'true'},\n"
        f"        colorize: {'true' if user_config['colorAnswerTable'] else 'false'},\n"
        f"        colors: {user_config['answerColoring']}\n"
        "    }\n"
        "};\n"
    )
    return (
        user_config_front_options_javascript
        if side == Template_side.FRONT
        else user_config_back_options_javascript
    )


def fillTemplateAndModelFromFile(model, user_config={}):
    """Modify the referenced `model` by a user config or using the defaults instead."""

    if user_config:
        front_options_java_script = getOptionsJavaScriptFromConfig(
            user_config, Template_side.FRONT
        )
        back_options_java_script = getOptionsJavaScriptFromConfig(
            user_config, Template_side.BACK
        )

    front_template = get_default_front_template_text()
    if user_config:
        front_template = re.sub(
            r"const OPTIONS.*?;",
            front_options_java_script,
            front_template,
            1,
            re.DOTALL,
        )
    set_front_template(model, front_template)

    back_template = get_default_back_template_text()
    if user_config:
        back_template = re.sub(
            r"const OPTIONS.*?;",
            back_options_java_script,
            back_template,
            1,
            re.DOTALL,
        )
    set_back_template(model, back_template)

    model["css"] = get_default_css_template_text()


def adjust_number_of_question_fields(model) -> None:
    """When updating the note type this modifies the model in place to have the
    template match the model's number of question fields."""

    model_manager = mw.col.models
    field_names = model_manager.field_names(model)
    number_of_question_fields = len(
        [name for name in field_names if re.match(QUESTION_ID_PATTERN, name)]
    )

    add_missing_fields(model, field_names)

    if number_of_question_fields > DEFAULT_NUMBER_OF_QUESTIONS:
        for i in range(DEFAULT_NUMBER_OF_QUESTIONS + 1, number_of_question_fields + 1):
            set_front_template(
                model,
                get_front_template_with_added_field(
                    {"name": f"Q_{i}"}, get_model_front_template_text(model)
                ),
            )
    elif number_of_question_fields < DEFAULT_NUMBER_OF_QUESTIONS:
        for i in range(number_of_question_fields + 1, DEFAULT_NUMBER_OF_QUESTIONS + 1):
            set_front_template(
                model,
                get_front_template_with_removed_field(
                    {"name": f"Q_{i}"}, get_model_front_template_text(model)
                ),
            )


def addModel(col: Collection) -> dict[str, Any]:
    """Add add-on note type to collection"""
    models = col.models
    model = models.new(aio_model_name)
    model["type"] = MODEL_STD

    add_fields(models, model)

    # Add template
    template = models.new_template(aio_card)

    fillTemplateAndModelFromFile(model)

    model["sortf"] = 0  # set sortfield to question
    models.add_template(model, template)
    models.add(model)
    return model


def add_fields(models, model):
    for i in aio_fields.keys():
        fld = models.new_field(aio_fields[i])
        models.add_field(model, fld)


def add_missing_fields(model, current_field_names: list[str]):
    models = mw.col.models

    for default_field_name in filter(
        lambda n: not re.match(QUESTION_ID_PATTERN, n), aio_fields.values()
    ):
        if default_field_name not in current_field_names:
            fld = models.new_field(default_field_name)
            models.add_field(model, fld)


def updateTemplate(col: Collection, user_config={}):
    """Update add-on note templates"""
    print(f"Updating {aio_model_name} note template")
    model = col.models.by_name(aio_model_name)

    fillTemplateAndModelFromFile(model, user_config)
    adjust_number_of_question_fields(model)

    col.models.save(model)
    return model


def AddOrUpdateModel():
    model = mw.col.models.by_name(aio_model_name)
    model_version = mw.col.get_config("mc_conf")["version"]

    if not model:
        addModel(mw.col)
    elif version.parse(model_version) < version.parse(default_conf_syncd["version"]):
        updateTemplate(mw.col)


def get_model() -> dict[str, Any]:
    return mw.col.models.by_name(aio_model_name)


def manage_multiple_choice_note_type():
    """Setup add-on config and templates, update if necessary"""
    getSyncedConfig()
    getLocalConfig()
    AddOrUpdateModel()
    if version.parse(mw.col.get_config("mc_conf")["version"]) < version.parse(
        default_conf_syncd["version"]
    ):
        updateSyncedConfig()
    if version.parse(mw.pm.profile["mc_conf"].get("version", 0)) < version.parse(
        default_conf_syncd["version"]
    ):
        updateLocalConfig()


def update_multiple_choice_note_type_from_config(user_config: str, addon_name: str):
    """Set options according to saved user's meta.json in the addon's folder"""

    user_config_dict = json.loads(user_config)
    # Updating other add-ons' config also runs the hook calling this method.
    if addon_name == get_addon_name():
        updateTemplate(mw.col, user_config_dict)
    return user_config


def remove_deleted_field_from_template(
    dialog: fields.FieldDialog, field: dict[str, Any]
):
    """As this is called while using the addon this doesn't overwrite the
    potentially user-modified template with the default"""
    model = dialog.model

    if model.get("name") == aio_model_name and re.search(
        QUESTION_ID_PATTERN, field.get("name")
    ):
        set_front_template(
            model,
            get_front_template_with_removed_field(
                field, get_model_front_template_text()
            ),
        )
        update_model(model)


def add_added_field_to_template(dialog: fields.FieldDialog, field: dict[str, Any]):
    """As this is called while using the addon this doesn't overwrite the
    potentially user-modified template with the default"""
    model = dialog.model

    if model.get("name") == aio_model_name and re.search(
        QUESTION_ID_PATTERN, field.get("name")
    ):
        set_front_template(
            model,
            get_front_template_with_added_field(field, get_model_front_template_text()),
        )
        update_model(model)


def set_front_template(model, template_text):
    model["tmpls"][0]["qfmt"] = template_text


def set_back_template(model, template_text):
    model["tmpls"][0]["afmt"] = template_text


def update_model(model):
    mw.col.models.save(model)


def get_model_front_template_text(model: dict[str, Any] = None) -> str:
    if model is None:
        model = get_model()
    return model["tmpls"][0]["qfmt"]


@cache
def get_default_front_template_text() -> str:
    with open(get_addon_path() + "card/front.html", encoding="utf-8") as f:
        return f.read()


@cache
def get_default_back_template_text() -> str:
    with open(get_addon_path() + "card/back.html", encoding="utf-8") as f:
        return f.read()


@cache
def get_default_css_template_text() -> str:
    with open(get_addon_path() + "card/css.css", encoding="utf-8") as f:
        return f.read()


def get_front_template_with_removed_field(
    field: dict[str, Any], template_text: str
) -> str:
    question_div = (
        '<div class="hidden" id="question_id">{{question_id}}</div>\n'.replace(
            "question_id", field.get("name")
        )
    )

    return template_text.replace(question_div, "")


def get_front_template_with_added_field(
    field: dict[str, Any], template_text: str
) -> str:
    question_div = '<div class="hidden" id="question_id">{{question_id}}</div>'.replace(
        "question_id", field.get("name")
    )
    question_num = int(re.search(QUESTION_ID_PATTERN, field.get("name")).group(1))

    previous_question_text = (
        f'<div class="hidden" id="Q_{question_num-1}">{{{{Q_{question_num-1}}}}}</div>'
    )
    previous_question_index = template_text.find(previous_question_text)

    if previous_question_index > 0:
        return (
            template_text[: previous_question_index + len(previous_question_text)]
            + "\n"
            + question_div
            + template_text[previous_question_index + len(previous_question_text) :]
        )
    else:
        return question_div + "\n" + template_text

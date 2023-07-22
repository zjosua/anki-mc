# Multiple Choice for Anki

# Copyright (C) 2023  3ter and zjosua

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from multiple_choice.template import (
    add_added_field_to_template,
    adjust_number_of_question_fields,
    aio_model_name,
    get_default_front_template_text,
    get_front_template_with_added_field,
    get_front_template_with_removed_field,
    manage_multiple_choice_note_type,
    remove_deleted_field_from_template,
    set_front_template,
)

MODEL_QFMT = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_WITHOUT_Q5 = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_WITHOUT_Q5_Q2 = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_WITH_ADDED_Q6 = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>
<div class="hidden" id="Q_6">{{Q_6}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_WITH_ADDED_Q9 = """<div class="hidden" id="Q_9">{{Q_9}}</div>
# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_Q1_TO_Q3 = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_Q1_TO_Q7 = """# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>
<div class="hidden" id="Q_6">{{Q_6}}</div>
<div class="hidden" id="Q_7">{{Q_7}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""

MODEL_QFMT_PARTIAL_Q1_TO_Q3 = """# Start of the template front
<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4"></div>
<div class="hidden" id="Q_5"></div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
"""


def get_default_model(qfmt=MODEL_QFMT) -> dict[str, Any]:
    return {"name": aio_model_name, "tmpls": [{"qfmt": qfmt}]}


class TestTemplateMethods(unittest.TestCase):
    @patch("multiple_choice.template.mw", autospec=True)
    @patch("multiple_choice.config.mw", autospec=True)
    @patch("multiple_choice.template.get_addon_path")
    def test_given_new_addon_version_when_manage_multiple_choice_note_type_is_called_then_addon_loads_without_exceptions(
        self, get_addon_path: MagicMock, mw_from_config, mw_from_template
    ):
        """As we have no `main window` (mw), everything needs to be mocked."""
        model_manager = MagicMock()
        model_manager.field_names.return_value = [
            "Question",
            "Title",
            "Q_1",
            "Q_2",
            "Q_3",
            "Q_4",
            "Q_5",
            "Q_6",
            "Q_7",
            "Extra 1",
        ]
        model = get_default_model()
        old_version = {"version": "1.0.0"}

        for mw in [mw_from_template, mw_from_config]:
            mw.col.models = model_manager
            mw.col.models.by_name.return_value = model
            mw.col.get_config.return_value = old_version
            mw.pm.profile = {"mc_conf": old_version}

        get_addon_path.return_value = "src/multiple_choice/"

        manage_multiple_choice_note_type()

    @patch("multiple_choice.template.update_model")
    @patch("multiple_choice.template.get_front_template_with_removed_field")
    @patch("multiple_choice.template.get_model_front_template_text")
    @patch("multiple_choice.template.fields.FieldDialog")
    def test_when_remove_deleted_field_from_template_is_called_then_calls_correct_methods(
        self,
        field_dialog,
        get_model_front_template_text: MagicMock,
        get_front_template_with_removed_field: MagicMock,
        update_model: MagicMock,
    ):
        field_dialog.model = get_default_model()
        get_model_front_template_text.return_value = MODEL_QFMT

        field: dict[str, Any] = {"name": "Q_5"}

        remove_deleted_field_from_template(field_dialog, field)

        get_model_front_template_text.assert_called_once()
        get_front_template_with_removed_field.assert_called_once_with(field, MODEL_QFMT)
        update_model.assert_called_once()

    def test_when_get_front_template_with_removed_field_is_called_then_removes_correctly(
        self,
    ):
        field: dict[str, Any] = {"name": "Q_5"}

        self.assertEqual(
            get_front_template_with_removed_field(field, MODEL_QFMT),
            MODEL_QFMT_WITHOUT_Q5,
        )

    def test_when_get_front_template_with_removed_field_is_called_multiple_times_then_removes_correctly(
        self,
    ):
        field: dict[str, Any] = {"name": "Q_5"}

        self.assertEqual(
            get_front_template_with_removed_field(field, MODEL_QFMT),
            MODEL_QFMT_WITHOUT_Q5,
        )

        field: dict[str, Any] = {"name": "Q_2"}

        self.assertEqual(
            get_front_template_with_removed_field(field, MODEL_QFMT_WITHOUT_Q5),
            MODEL_QFMT_WITHOUT_Q5_Q2,
        )

    @patch("multiple_choice.template.fields.FieldDialog")
    def test_when_set_front_template_is_called_then_correct_attribute_is_used(
        self, field_dialog
    ):
        field_dialog.model = get_default_model()

        self.assertEqual(field_dialog.model["tmpls"][0]["qfmt"], MODEL_QFMT)

        set_front_template(field_dialog.model, "foobar3000")

        self.assertEqual(field_dialog.model["tmpls"][0]["qfmt"], "foobar3000")

    @patch("multiple_choice.template.update_model")
    @patch("multiple_choice.template.get_front_template_with_added_field")
    @patch("multiple_choice.template.get_model_front_template_text")
    @patch("multiple_choice.template.fields.FieldDialog")
    def test_when_add_added_field_to_template_is_called_then_calls_correct_methods(
        self,
        field_dialog,
        get_model_front_template_text: MagicMock,
        get_front_template_with_added_field: MagicMock,
        update_model: MagicMock,
    ):
        field_dialog.model = get_default_model()
        get_model_front_template_text.return_value = MODEL_QFMT

        field: dict[str, Any] = {"name": "Q_6"}

        add_added_field_to_template(field_dialog, field)

        get_model_front_template_text.assert_called_once()
        get_front_template_with_added_field.assert_called_once_with(field, MODEL_QFMT)
        update_model.assert_called_once()

    def test_when_get_front_template_with_added_field_is_called_then_adds_correctly(
        self,
    ):
        field: dict[str, Any] = {"name": "Q_6"}

        self.assertEqual(
            get_front_template_with_added_field(field, MODEL_QFMT),
            MODEL_QFMT_WITH_ADDED_Q6,
        )

        field: dict[str, Any] = {"name": "Q_9"}

        self.assertEqual(
            get_front_template_with_added_field(field, MODEL_QFMT),
            MODEL_QFMT_WITH_ADDED_Q9,
        )

    @patch("multiple_choice.template.mw", autospec=True)
    @patch("multiple_choice.template.get_default_front_template_text")
    def test_given_default_question_fields_when_adjust_number_of_question_fields_is_called_then_do_nothing(
        self, get_default_front_template_text: MagicMock, mw
    ):
        self.maxDiff = None

        model_manager = MagicMock()
        model_manager.field_names.return_value = [
            "Question",
            "Title",
            "Q_1",
            "Q_2",
            "Q_3",
            "Q_4",
            "Q_5",
            "Extra 1",
        ]

        get_default_front_template_text.return_value = MODEL_QFMT

        model = get_default_model()

        mw.col.models = model_manager
        mw.col.models.by_name.return_value = model
        mw.col.get_config.return_value = {"version": "9.9.9"}

        adjust_number_of_question_fields(model)

        self.assertEqual(model, get_default_model())

    @patch("multiple_choice.template.mw", autospec=True)
    @patch("multiple_choice.template.get_default_front_template_text")
    def test_given_too_few_question_fields_when_adjust_number_of_question_fields_is_called_then_add_divs(
        self, get_default_front_template_text: MagicMock, mw
    ):
        self.maxDiff = None

        model_manager = MagicMock()
        model_manager.field_names.return_value = [
            "Question",
            "Title",
            "Q_1",
            "Q_2",
            "Q_3",
            "Extra 1",
        ]

        get_default_front_template_text.return_value = MODEL_QFMT

        model = get_default_model()

        mw.col.models = model_manager
        mw.col.models.by_name.return_value = model
        mw.col.get_config.return_value = {"version": "9.9.9"}

        adjust_number_of_question_fields(model)

        self.assertEqual(model["tmpls"][0]["qfmt"], MODEL_QFMT_Q1_TO_Q3)

    @patch("multiple_choice.template.mw", autospec=True)
    @patch("multiple_choice.template.get_default_front_template_text")
    def test_given_too_many_question_fields_when_adjust_number_of_question_fields_is_called_then_add_divs(
        self, get_default_front_template_text: MagicMock, mw
    ):
        self.maxDiff = None

        model_manager = MagicMock()
        model_manager.field_names.return_value = [
            "Question",
            "Title",
            "Q_1",
            "Q_2",
            "Q_3",
            "Q_4",
            "Q_5",
            "Q_6",
            "Q_7",
            "Extra 1",
        ]

        get_default_front_template_text.return_value = MODEL_QFMT

        model = get_default_model()

        mw.col.models = model_manager
        mw.col.models.by_name.return_value = model
        mw.col.get_config.return_value = {"version": "9.9.9"}

        adjust_number_of_question_fields(model)

        self.assertEqual(model["tmpls"][0]["qfmt"], MODEL_QFMT_Q1_TO_Q7)


if __name__ == "__main__":
    unittest.main()

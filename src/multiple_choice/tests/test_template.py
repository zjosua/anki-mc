import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from multiple_choice.template import (add_added_field_to_template,
                                      aio_model_name,
                                      get_front_template_with_added_field,
                                      get_front_template_with_removed_field,
                                      remove_deleted_field_from_template,
                                      set_front_template)

MODEL_QFMT = '''# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
'''

MODEL_QFMT_WITHOUT_Q5 = '''# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
'''

MODEL_QFMT_WITHOUT_Q5_Q2 = '''# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
'''

MODEL_QFMT_WITH_ADDED_Q6 = '''# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>
<div class="hidden" id="Q_6">{{Q_6}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
'''

MODEL_QFMT_WITH_ADDED_Q9 = '''<div class="hidden" id="Q_9">{{Q_9}}</div>
# Start of the template front

<div class="hidden" id="Q_1">{{Q_1}}</div>
<div class="hidden" id="Q_2">{{Q_2}}</div>
<div class="hidden" id="Q_3">{{Q_3}}</div>
<div class="hidden" id="Q_4">{{Q_4}}</div>
<div class="hidden" id="Q_5">{{Q_5}}</div>

# Rest of the template front with some fake matches: Q_4 Q_5 <div>
'''


class TestTemplateMethods(unittest.TestCase):

    @patch('multiple_choice.template.update_model')
    @patch('multiple_choice.template.get_front_template_with_removed_field')
    @patch('multiple_choice.template.get_front_template_text')
    @patch('multiple_choice.template.fields.FieldDialog')
    def test_when_remove_deleted_field_from_template_is_called_then_calls_correct_methods(self,
                                                                                          field_dialog,
                                                                                          get_front_template_text: MagicMock,
                                                                                          get_front_template_with_removed_field: MagicMock,
                                                                                          update_model: MagicMock):
        field_dialog.model = {
            'name': aio_model_name, 'tmpls': [{'qfmt': MODEL_QFMT}]}
        get_front_template_text.return_value = MODEL_QFMT

        field: dict[str, Any] = {'name': 'Q_5'}

        remove_deleted_field_from_template(field_dialog, field)

        get_front_template_text.assert_called_once()
        get_front_template_with_removed_field.assert_called_once_with(
            field, MODEL_QFMT)
        update_model.assert_called_once()

    def test_when_get_front_template_with_removed_field_is_called_then_removes_correctly(self):
        field: dict[str, Any] = {'name': 'Q_5'}

        self.assertEqual(get_front_template_with_removed_field(
            field, MODEL_QFMT), MODEL_QFMT_WITHOUT_Q5)

    def test_when_get_front_template_with_removed_field_is_called_multiple_times_then_removes_correctly(self):
        field: dict[str, Any] = {'name': 'Q_5'}

        self.assertEqual(get_front_template_with_removed_field(
            field, MODEL_QFMT), MODEL_QFMT_WITHOUT_Q5)

        field: dict[str, Any] = {'name': 'Q_2'}

        self.assertEqual(get_front_template_with_removed_field(
            field, MODEL_QFMT_WITHOUT_Q5), MODEL_QFMT_WITHOUT_Q5_Q2)

    @patch('multiple_choice.template.fields.FieldDialog')
    def test_when_set_front_template_is_called_then_correct_attribute_is_used(self, field_dialog):
        field_dialog.model = {
            'name': aio_model_name, 'tmpls': [{'qfmt': MODEL_QFMT}]}

        self.assertEqual(field_dialog.model['tmpls'][0]['qfmt'], MODEL_QFMT)

        set_front_template(field_dialog.model, 'foobar3000')

        self.assertEqual(field_dialog.model['tmpls'][0]['qfmt'], 'foobar3000')

    @patch('multiple_choice.template.update_model')
    @patch('multiple_choice.template.get_front_template_with_added_field')
    @patch('multiple_choice.template.get_front_template_text')
    @patch('multiple_choice.template.fields.FieldDialog')
    def test_when_add_added_field_to_template_is_called_then_calls_correct_methods(self,
                                                                                   field_dialog,
                                                                                   get_front_template_text: MagicMock,
                                                                                   get_front_template_with_added_field: MagicMock,
                                                                                   update_model: MagicMock):
        field_dialog.model = {
            'name': aio_model_name, 'tmpls': [{'qfmt': MODEL_QFMT}]}
        get_front_template_text.return_value = MODEL_QFMT

        field: dict[str, Any] = {'name': 'Q_6'}

        add_added_field_to_template(field_dialog, field)

        get_front_template_text.assert_called_once()
        get_front_template_with_added_field.assert_called_once_with(
            field, MODEL_QFMT)
        update_model.assert_called_once()

    def test_when_get_front_template_with_added_field_is_called_then_adds_correctly(self):
        field: dict[str, Any] = {'name': 'Q_6'}

        self.assertEqual(get_front_template_with_added_field(
            field, MODEL_QFMT), MODEL_QFMT_WITH_ADDED_Q6)

        field: dict[str, Any] = {'name': 'Q_9'}

        self.assertEqual(get_front_template_with_added_field(
            field, MODEL_QFMT), MODEL_QFMT_WITH_ADDED_Q9)


if __name__ == '__main__':
    unittest.main()

# Multiple Choice for Anki
#
# Copyright (C) 2018-2023  3ter <https://github.com/3ter>
#                          zjosua <https://github.com/zjosua>
#
# This file is based on __init__.py from Glutanimate's
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

from anki.utils import pointVersion
from aqt.gui_hooks import addon_config_editor_will_update_json, profile_did_open

from .template import (
    add_added_field_to_template,
    manage_multiple_choice_note_type,
    remove_deleted_field_from_template,
    update_multiple_choice_note_type_from_config,
)

field_deletion_hook_anki_version = 36
field_addition_hook_anki_version = 66

# Only execute addon after profile and collection are fully initialized
profile_did_open.append(manage_multiple_choice_note_type)

addon_config_editor_will_update_json.append(
    update_multiple_choice_note_type_from_config
)


if pointVersion() >= field_deletion_hook_anki_version:
    from aqt.gui_hooks import fields_did_delete_field

    fields_did_delete_field.append(remove_deleted_field_from_template)
if pointVersion() >= field_addition_hook_anki_version:
    from aqt.gui_hooks import fields_did_add_field

    fields_did_add_field.append(add_added_field_to_template)

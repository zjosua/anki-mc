# Multiple Choice for Anki
#
# Copyright (C) 2018-2021  zjosua <https://github.com/zjosua>
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

from aqt import gui_hooks, mw

from .config import *
from .packaging import version
from .template import *

def getOrCreateModel():
    model = mw.col.models.byName(aio_model)
    if not model:
        # create model
        model = addModel(mw.col)
        return model
    model_version = mw.col.get_config('mc_conf')['version']
    if version.parse(model_version) < version.parse(default_conf_syncd['version']):
        return updateTemplate(mw.col)
    return model

def delayedInit():
    """Setup add-on config and templates, update if necessary"""
    getSyncedConfig()
    getLocalConfig()
    getOrCreateModel()
    if version.parse(mw.col.get_config("mc_conf")['version']) < version.parse(default_conf_syncd['version']):
        updateSyncedConfig()
    if version.parse(mw.pm.profile['mc_conf'].get('version', 0)) < version.parse(default_conf_syncd['version']):
        updateLocalConfig()

gui_hooks.profile_did_open.append(delayedInit)


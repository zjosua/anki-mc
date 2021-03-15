# Multiple Choice for Anki
#
# Copyright (C) 2018-2021  zjosua <https://github.com/zjosua>
#
# This file is based on config.py from Glutanimate's
# Image Occlusion Enhanced Add-on for Anki
#
# Copyright (C) 2016-2020  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2012-2015  Tiago Barroso <tmbb@campus.ul.pt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
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
Sets up configuration
"""

# Compare semantic version: https://stackoverflow.com/a/11887885
from distutils.version import LooseVersion

from aqt import mw

# default configurations
# TODO: update version number before release
default_conf_local = {'version': "2.4.0"}
default_conf_syncd = {'version': "2.4.0"}


def getSyncedConfig():
    # Synced preferences
    if mw.col.get_config("mc_conf") is None:
        # create initial configuration
        mw.col.set_config("mc_conf", default_conf_syncd)
        mw.col.setMod()

    elif LooseVersion(mw.col.get_config("mc_conf")['version']) < LooseVersion(default_conf_syncd['version']):
        print("Updating config DB from earlier IO release")
        tmp_conf = mw.col.get_config("mc_conf")
        for key in list(default_conf_syncd.keys()):
            if key not in mw.col.get_config("mc_conf"):
                tmp_conf[key] = default_conf_syncd[key]
        tmp_conf['version'] = default_conf_syncd['version']
        mw.col.set_config("mc_conf", tmp_conf)
        mw.col.setMod()

    return mw.col.get_config("mc_conf")


def getLocalConfig():
    # Local preferences
    if 'mc_conf' not in mw.pm.profile:
        mw.pm.profile["mc_conf"] = default_conf_local
    elif LooseVersion(mw.pm.profile['mc_conf'].get('version', 0)) < LooseVersion(default_conf_syncd['version']):
        for key in list(default_conf_local.keys()):
            if key not in mw.col.get_config("mc_conf"):
                mw.pm.profile["mc_conf"][key] = default_conf_local[key]
        mw.pm.profile['mc_conf']['version'] = default_conf_local['version']

    return mw.pm.profile["mc_conf"]

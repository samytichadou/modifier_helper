'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Modifier Helper",
    "description": "Manage several modifiers quickly",
    "author": "Samy Tichadou (tonton)",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "",
    "wiki_url": "https://github.com/samytichadou/particle_helper/blob/master/README.md",
    "tracker_url": "https://github.com/samytichadou/particle_helper/issues/new",
    "category": "Modifier" }

# IMPORT SPECIFICS
##################################

from . import   (toggle_modifiers_operator,
                )


# register
##################################

def register():
    toggle_modifiers_operator.register()

def unregister():
    toggle_modifiers_operator.unregister()
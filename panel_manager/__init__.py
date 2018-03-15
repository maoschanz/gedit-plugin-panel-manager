# panel_manager/__init__.py
#
# Copyright (C) 2018 Romain F. T. (except for icons i stole from gnome-builder)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, Gedit

IN_HEADERBAR = False
BASE_PATH = os.path.dirname(os.path.realpath(__file__))

class PanelManagerGeditPlugin(GObject.Object, Gedit.WindowActivatable):
	__gtype_name__ = "panel_manager"
	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)
		self.button_side = Gtk.ToggleButton()
		imageL = Gtk.Image()
		imageL.set_from_file(BASE_PATH + "/builder-view-left-pane-symbolic.symbolic.png")
		self.button_side.add(imageL)
		self.button_bottom = Gtk.ToggleButton()
		imageI = Gtk.Image()
		imageI.set_from_file(BASE_PATH + "/builder-view-bottom-pane-symbolic.symbolic.png")
		self.button_bottom.add(imageI)
		self.btnBox = Gtk.Box()
		self.btn_align = Gtk.Alignment(
			xalign=0.0, yalign=0.5, xscale=0.0, yscale=0.0)

	def do_activate(self):
		if IN_HEADERBAR:
			self._bar = self.window.get_titlebar().get_children()[-1]
			self._bar.pack_end(self.btn_align)
		else:
			self._bar = self.window.get_statusbar()
			self._bar.pack_end(self.btn_align, expand=False, fill=False, padding=5)
		self.btnBox.add(self.button_side)
		self.btnBox.add(self.button_bottom)
		self.btn_align.add(self.btnBox)
		self.btn_align.show_all()
		self.set_states()
		self.button_side.connect("toggled", self.on_side_click)
		self.button_bottom.connect("toggled", self.on_bottom_click)

	def do_deactivate(self):
		Gtk.Container.remove(self._bar, self.button_side)
		Gtk.Container.remove(self._bar, self.button_bottom)
		del self.button_side
		del self.button_bottom

	def on_side_click(self, button):
		self.window.get_side_panel().set_property("visible", self.button_side.get_active())

	def on_bottom_click(self, button):
		self.window.get_bottom_panel().set_property("visible", self.button_bottom.get_active())
			
	def set_states(self):
		self.window.get_side_panel().connect("notify::visible", self.on_side_changed)
		self.window.get_bottom_panel().connect("notify::visible", self.on_bottom_changed)
		
	def on_side_changed(self, a, b):
		self.button_side.set_active(self.window.get_side_panel().get_property("visible"))
		
	def on_bottom_changed(self, a, b):
		self.button_bottom.set_active(self.window.get_bottom_panel().get_property("visible"))



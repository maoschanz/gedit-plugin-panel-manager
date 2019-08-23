# panel_manager.py
#
# Copyright (C) 2018 Romain F. T.
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
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gio, Gtk, Gedit, PeasGtk

class PanelManagerPosition():
	TOP_LEFT = 0
	TOP_RIGHT = 1
	BOTTOM = 2

class PanelManagerGeditPlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
	__gtype_name__ = "PanelManagerGeditPlugin"
	window = GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

	def build_UI(self):
		self.button_side = Gtk.ToggleButton()
		image = Gtk.Image().new_from_icon_name('go-first-symbolic', \
		                                             Gtk.IconSize.SMALL_TOOLBAR)
		self.button_side.set_image(image)
		self.button_bottom = Gtk.ToggleButton()
		image = Gtk.Image().new_from_icon_name('go-bottom-symbolic', \
		                                             Gtk.IconSize.SMALL_TOOLBAR)
		self.button_bottom.set_image(image)
		
		self.btnBox = Gtk.Box()
		self.btnBox.add(self.button_side)
		self.btnBox.add(self.button_bottom)
		
		if self.get_position_id() == PanelManagerPosition.BOTTOM:
			self.button_side.set_relief(Gtk.ReliefStyle.NONE)
			self.button_bottom.set_relief(Gtk.ReliefStyle.NONE)
		else:
			self.btnBox.get_style_context().add_class('linked')
		
		self.window.get_side_panel().connect('notify::visible', self.on_side_changed)
		self.window.get_bottom_panel().connect('notify::visible', self.on_bottom_changed)
		self.button_side.connect('toggled', self.on_side_click)
		self.button_bottom.connect('toggled', self.on_bottom_click)

	def destroy_UI(self): # FIXME
#		Gtk.Container.remove(self._bar, self.btnBox)
#		del self.button_side
#		del self.button_bottom
		self.btnBox.set_visible(False)

	def do_activate(self):
		self.build_UI()
		position = self.get_position_id()
		if position == PanelManagerPosition.TOP_LEFT:
			self._bar = self.window.get_titlebar().get_children()[-1]
			self._bar.pack_start(self.btnBox)
		elif position == PanelManagerPosition.TOP_RIGHT:
			self._bar = self.window.get_titlebar().get_children()[-1]
			self._bar.pack_end(self.btnBox)
		else:
			self._bar = self.window.get_statusbar()
			self._bar.pack_end(self.btnBox, expand=False, fill=False, padding=5)
		self.btnBox.show_all()

	def do_deactivate(self):
		self.destroy_UI()

	def on_side_click(self, button):
		self.window.get_side_panel().set_property('visible', button.get_active())

	def on_bottom_click(self, button):
		self.window.get_bottom_panel().set_property('visible', button.get_active())

	def on_side_changed(self, *args):
		panel_is_visible = self.window.get_side_panel().get_property('visible')
		self.button_side.set_active(panel_is_visible)

	def on_bottom_changed(self, *args):
		panel_is_visible = self.window.get_bottom_panel().get_property('visible')
		self.button_bottom.set_active(panel_is_visible)

	############################################################################

	def do_create_configure_widget(self):
		# PeasGtk will automatically pack this widget into a dialog and show it.
		widget = Gtk.Box(margin=16, spacing=12, orientation=Gtk.Orientation.VERTICAL)
		widget.set_size_request(250, 0)
		label = Gtk.Label(label="Position:")
		widget.add(label)
		btn0 = Gtk.RadioButton(label="Top left")
		btn1 = Gtk.RadioButton(label="Top right", group=btn0)
		btn2 = Gtk.RadioButton(label="Bottom", group=btn0)
		btn0.connect('toggled', self.on_param_changed, 0)
		btn1.connect('toggled', self.on_param_changed, 1)
		btn2.connect('toggled', self.on_param_changed, 2)
		widget.add(btn0)
		widget.add(btn1)
		widget.add(btn2)
		position_id = self.get_position_id()
		if position_id == 0:
			btn0.set_active(True)
		elif position_id == 1:
			btn1.set_active(True)
		else:
			btn2.set_active(True)
		widget.show_all()
		return widget

	def on_param_changed(self, button, position_id):
		if button.get_active():
			settings = Gio.Settings.new('org.gnome.gedit.plugins.panel_manager')
			settings.set_int('position', position_id)

	def get_position_id(self):
		settings = Gio.Settings.new('org.gnome.gedit.plugins.panel_manager')
		return settings.get_int('position')

	############################################################################
################################################################################


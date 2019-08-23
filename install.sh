#!/bin/bash

if (( $EUID == 0 )); then
	INSTALL_DIR="/usr/lib/x86_64-linux-gnu/gedit/plugins"
	SCHEMA_DIR="/usr/share/glib-2.0/schemas"
else
	INSTALL_DIR="$HOME/.local/share/gedit/plugins"
	SCHEMA_DIR="$HOME/.local/share/glib-2.0/schemas"
fi
mkdir -p $INSTALL_DIR
mkdir -p $SCHEMA_DIR

echo "Installing $INSTALL_DIR/panel_manager.plugin"
cp panel_manager.plugin $INSTALL_DIR/panel_manager.plugin
echo "Installing $INSTALL_DIR/panel_manager.py"
cp -r panel_manager.py $INSTALL_DIR/panel_manager.py

echo "Compiling gsettings schemas in $SCHEMA_DIR"
cp org.gnome.gedit.plugins.panel_manager.gschema.xml $SCHEMA_DIR
glib-compile-schemas $SCHEMA_DIR

echo "Done."
exit 0


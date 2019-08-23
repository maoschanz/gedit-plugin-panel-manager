#!/bin/bash

if (( $EUID == 0 )); then
	INSTALL_DIR="/usr/lib/x86_64-linux-gnu/gedit/plugins"
else
	INSTALL_DIR="$HOME/.local/share/gedit/plugins"
fi
mkdir -p $INSTALL_DIR

echo "Installing $INSTALL_DIR/panel_manager.plugin"
cp panel_manager.plugin $INSTALL_DIR/panel_manager.plugin
echo "Installing $INSTALL_DIR/panel_manager.py"
cp -r panel_manager.py $INSTALL_DIR/panel_manager.py

echo "Done."
exit 0


#!/bin/bash

if [ ! -d "$HOME/.local/share/gedit" ]; then
	mkdir ~/.local/share/gedit
fi
if [ ! -d "$HOME/.local/share/gedit/plugins" ]; then
	mkdir ~/.local/share/gedit/plugins
fi

cp panel_manager.plugin ~/.local/share/gedit/plugins/panel_manager.plugin
cp -r panel_manager ~/.local/share/gedit/plugins/

#sudo cp markdown_preview.py /usr/lib/x86_64-linux-gnu/gedit/plugins/markdown_preview.py
#sudo cp markdown_preview.plugin /usr/lib/x86_64-linux-gnu/gedit/plugins/markdown_preview.plugin


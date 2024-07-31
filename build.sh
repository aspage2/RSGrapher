#!/bin/sh

poetry run pyinstaller \
	--hidden-import PIL._tkinter_finder \
	--hidden-import matplotlib.backends.backend_pdf \
	--add-data res/logo.png:res \
	--workpath workdir \
	--onefile \
	--name RSGrapher \
	run.py

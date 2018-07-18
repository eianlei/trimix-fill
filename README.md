# trimix-fill
trimix-fill was a quick project for learning to code Python and to learn and compare different Python GUI frameworks: TkInter and PyQt5.

I eventually decided that I like PyQt5 much more and decided not to continue with TkInter. This repo is no longer developed, and I have moved on to a new project [pydplan@github](https://github.com/eianlei/pydplan), see also [PYDPLAN github pages for documentation](https://eianlei.github.io/pydplan/)

In this repo there are various technical scuba diving calculation modules and applications coded in Python3. 
The GUI applications are coded for tkinter and PyQt5 frameworks.
Also a command line variant was made to see how that works vs GUI.
Read the wiki pages for more details.

This repo contains:

## Trimix blending tools:
- tmx_gui-pyqt5.py, GUI app for doing trimix gas blending calculations, uses PyQt5

- tmx_calc.py, modules for trimix gas blending calculations, no user interfaces, which are in other modules
- tmx_gui.py, GUI/tkinter module for trimix gas blending, uses  tmx_calc.py
- tmx_c.py, command line interface for tmx_calc.py, uses argparse
- trimix-fill-3.py, tkinter GUI app for doing trimix gas blending calculations all in one, and contains some functional bugs, uses tkinter, no longer developed 

## MOD calculation tools: 
- mod_gui_tk.py, GUI module for MOD calculation, uses tkinter
- mod_gui_pyqt5.py, GUI module for MOD calculation, uses PyQt5 instead of tkinter
- mod_gui_sb.py, GUI module for MOD calculation, uses PyQt5 and SpinBox widgets
- mod_gui_sb_sliders.py, GUI module for MOD calculation, uses PyQt5, SpinBox & slider widgets

The idea behind the MOD application is that it is simple enough to be coded quickly for many different frameworks with many different styles to see how they compare. 

## background
The project started from a single file module trimix-fill-3.py
Then it it was refactored so that the raw calculations are in functions inside the tmx_calc.py
and there is a TkInter based GUI in file tmx_gui.py and cmd line version in tmx_c.py.
This allows doing unit tests on the calculation modules, and to support both a GUI and command line version, or to reuse the calculation module in some other applications.
Then I continued to test other GUI frameworks, and concluded that PyQt5 is the best way to go.

You can find documentation about usage, requirements etc from the GitHub Wiki pages.



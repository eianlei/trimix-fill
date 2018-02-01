# trimix-fill
trimix-fill is a Python3 based GUI app for doing trimix gas blending calculations. 
It is coded in Python-3 using tkinter GUI framework.

Originally it was just a single file module trimix-fill-3.py
Then it it was refactored so that the raw calculations are in functions inside the tmx_calc.py
and there is a GUI in file tmx_gui.py.
This allows doing unit tests on the calculation modules, and to make a command line version, or to reuse the calculation module in some other applications.

You can find documentation about usage, requirements etc from the GitHub Wiki pages.

There is a "roadmap" of todo features in the GitHub Project page.

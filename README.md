# trimix-fill
trimix-fill is a Python3 based GUI & commnad line app for doing trimix gas blending calculations. 
It is coded in Python-3, and the GUI using tkinter framework, the cmd line version using argparse.

Originally it was just a single file module trimix-fill-3.py
Then it it was refactored so that the raw calculations are in functions inside the tmx_calc.py
and there is a GUI in file tmx_gui.py and cmd line version in tmx_c.py.
This allows doing unit tests on the calculation modules, and to support both a GUI and command line version, or to reuse the calculation module in some other applications.

You can find documentation about usage, requirements etc from the GitHub Wiki pages.

There is a "roadmap" of todo features in the GitHub Project page.

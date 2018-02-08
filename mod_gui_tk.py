#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# mod_gui_tk.py
# github project https://github.com/eianlei/trimix-fill/
#  this GUI uses function mod_calc() from tmx_calc.py
# use at your own risk, no guarantees, no liability!
#
# GUI to calculate MOD using tkinter

gui_version = "0.1"

from tkinter import *
from tkinter import ttk

# function that does the actual calculation
from tmx_calc import mod_calc

root = Tk()
root.title("MOD_GUIv{} MOD calculator".format(gui_version))

# create the main GUI frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# define all strings for input and output, set default values
o2pct = StringVar(root, value="21")
ppo2 = StringVar(root, value="1.4")
mod_out = StringVar(root)

############### define the input widgets on top
# top label
ttk.Label(mainframe, text="Input values for calculating MOD").grid(
    column=1, row=1, columnspan=2)
# input current tank pressure
ttk.Label(mainframe, text="Oxygen %").grid(column=1, row=2, sticky=W)
o2pct_entry = ttk.Entry(mainframe, width=7, textvariable=o2pct)
o2pct_entry.grid(column=2, row=2, sticky=(W, E))
#  input current tank O2
ttk.Label(mainframe, text="ppO2 in bar/ATA").grid(column=1, row=3, sticky=W)
ppo2_entry = ttk.Entry(mainframe, width=7, textvariable=ppo2)
ppo2_entry.grid(column=2, row=3, sticky=(W, E))


# calculation callback
def calc_cmd():
    '''callback for calculate button '''
    try:
        # get data from GUI objects, then convert input strings to floats
        o2pct_in = float(o2pct_entry.get())
        ppo2_in = float(ppo2_entry.get())

        mod_m = mod_calc(ppo2_in, o2pct_in)
        mod_out.set("MOD= {:.1f} meters".format(mod_m))
        print("mod_gui: o2pct= ", o2pct_in, " ppo2= ", ppo2_in, "=> MOD= ", mod_m)

    except ValueError:
        result_msg.set("enter all values as numbers!")
    pass


# the button to invoke calculation
ttk.Button(mainframe, text="Calculate", command=calc_cmd).grid(column=1, row=4, sticky=W)

# to insert text to these, we change the contents of what is pointed by textvariable
result_msg = ttk.Label(mainframe, textvariable=mod_out).grid(
    column=1, row=5, columnspan=2)

## padding around all widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=2, pady=2)
mainframe.pack()

# focus to the first entry field
o2pct_entry.focus()
# pressing return same as click calcualte button
root.bind('<Return>', calc_cmd())
# main window loop starts now
root.mainloop()

# done

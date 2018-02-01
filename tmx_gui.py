#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# tmx_gui.py
# github project https://github.com/eianlei/trimix-fill/
# Python-3 GUI using tkinter 8 for trimix blending calculator
#  this GUI uses function tmx_calc
# use at your own risk, no guarantees, no liability!
#
tmx_gui_version = "1.3"

from tkinter import *
from tkinter import ttk
import time
# function that does the actual calculation
from tmx_calc import *

root = Tk()
root.title("TMXGUIv{} Trimix fill calculator, 3 selectable methods".format(tmx_gui_version))

# create the main GUI frame
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

print("tmx_gui v. {}: starting".format(tmx_gui_version))




## callback function that is called when CALCULATE pressed
def calculate(*args) :
    """gets all entry data from GUI widgets and calls tmx_calc"""
    try:
        calc_method = method.get()

        print("tmx_gui: calculate")
        # get data from GUI objects, then convert input strings to floats
        tbar_1 = float(start_bar.get())
        endbar = float(end_bar.get())
        start_o2 = float(start_o2_pct.get())
        start_he = float(start_he_pct.get())
        end_o2 = float(end_o2_pct.get())
        end_he = float(end_he_pct.get())
        # cost calculation input
        liters = float(tank_lit.get())
        o2_cost_eur = float(o2_cost.get())
        he_cost_eur = float(he_cost.get())
        fill_cost_eur = float(fill_cost.get())
        he_ig = he_ignore.get()

        print("calculate with: ")
        print(calc_method, tbar_1, endbar, start_o2, start_he, end_o2, end_he, he_ig)
        #
        result = tmx_calc(calc_method, tbar_1, endbar, start_o2, start_he, end_o2, end_he, he_ig)
        result_pp.set(result['status_text'])
        add_o2 = result['add_o2']
        add_he = result['add_he']
        cost_result = tmx_cost_calc(liters, endbar, add_o2, add_he, o2_cost_eur,
                                    he_cost_eur, fill_cost_eur)
        total_cost_string = cost_result['result_txt']
        total_cost.set(total_cost_string)

        ## copy results to clipboard
        root.clipboard_clear()
        root.clipboard_append("Output result from Trimix fill calculator\n")
        root.clipboard_append("=========================================\n")
        root.clipboard_append(time.strftime("%Y-%method-%d %H:%M"))
        root.clipboard_append("\n- current tank {} bar, {} liters, mix {}/{}\n".format
                              (tbar_1, liters, start_o2, start_he))
        root.clipboard_append("- wanted mix {}/{}\n".format(end_o2, end_he))
        root.clipboard_append("\n{}\n\n{}\n".format(result['status_text'], total_cost_string))

    except ValueError:
        result_pp.set("enter all values as numbers!")
        pass
########################### end function calculate

def help_action(*args):
    print("HELP button pressed")
    pass

# define all strings for input and output, set default values
start_bar       = StringVar(root, value="0")
start_o2_pct    = StringVar(root, value="21")
start_he_pct    = StringVar(root, value="35")
end_bar         = StringVar(root, value="200")
end_o2_pct      = StringVar(root, value="21")
end_he_pct      = StringVar(root, value="35")
result_pp       = StringVar(root)
#
he_ignore       = IntVar(root, value=0)
#
tank_lit        = StringVar(root, value="24")
o2_cost         = StringVar(root, value="4.15")
he_cost         = StringVar(root, value="25")
fill_cost       = StringVar(root, value="5")
total_cost      = StringVar(root)

############### define the input widgets on top
# top label
ttk.Label(mainframe, text="Input values for calculating the fill", font="bold").grid(
    column=1, row=1, columnspan=2)
# input current tank pressure
ttk.Label(mainframe, text="current tank pressure (bar)").grid(column=1, row=2, sticky=W)
start_bar_entry = ttk.Entry(mainframe, width=7, textvariable=start_bar)
start_bar_entry.grid(column=2, row=2, sticky=(W, E))
#  input current tank O2
ttk.Label(mainframe, text="current tank Oxygen (%)").grid(column=1, row=3, sticky=W)
start_o2_pct_entry = ttk.Entry(mainframe, width=7, textvariable=start_o2_pct)
start_o2_pct_entry.grid(column=2, row=3, sticky=(W, E))
# input current tank He
ttk.Label(mainframe, text="current tank Helium (%)").grid(column=1, row=4, sticky=W)
start_he_pct_entry = ttk.Entry(mainframe, width=7, textvariable=start_he_pct)
start_he_pct_entry.grid(column=2, row=4, sticky=(W, E))
# wanted end pressure
ttk.Label(mainframe, text="wanted end pressure (bar)").grid(column=1, row=5, sticky=W)
end_bar_entry = ttk.Entry(mainframe, width=7, textvariable=end_bar)
end_bar_entry.grid(column=2, row=5, sticky=(W, E))
# wanted o2%
ttk.Label(mainframe, text="wanted Oxygen (%)").grid(column=1, row=6, sticky=W)
end_o2_pct_entry = ttk.Entry(mainframe, width=7, textvariable=end_o2_pct)
end_o2_pct_entry.grid(column=2, row=6, sticky=(W, E))
# wanted He %
end_he_label = ttk.Label(mainframe, text="wanted Helium (%)")
end_he_label.grid(column=1, row=7, sticky=W)
end_he_pct_entry = ttk.Entry(mainframe, width=7, textvariable=end_he_pct)
end_he_pct_entry.grid(column=2, row=7, sticky=(W, E))

## check button for not filling Helium and ignoring He target
style = ttk.Style()
style.configure("Grey.TLabel", foreground="grey")
style.configure("Black.TLabel", foreground="black")



# callback to handle
def he_ignore_change(*args):
    heg = he_ignore.get()
    print("He cb value {}".format(heg))
    if heg == 1:
        end_he_label.configure(style="Grey.TLabel")
        end_he_pct_entry.configure(state='disabled')
    else:
        end_he_label.configure(style="Black.TLabel")
        end_he_pct_entry.configure(state='enabled')


ttk.Checkbutton(mainframe, text="no He filled & ignore He target", variable=he_ignore,
                command=he_ignore_change).grid(column=3, row=7, sticky=W)

##############################################
# input fields for cost calculation
ttk.Label(mainframe, text="tank size (liters)").grid(column=3, row=2, sticky=W)
tank_lit_entry = ttk.Entry(mainframe, width=8, textvariable=tank_lit)
tank_lit_entry.grid(column=4, row=2, sticky=(W, E))

ttk.Label(mainframe, text="cost of Oxygen (€/m^3)").grid(column=3, row=3, sticky=W)
o2_cost_entry = ttk.Entry(mainframe, width=8, textvariable=o2_cost)
o2_cost_entry.grid(column=4, row=3, sticky=(W, E))

ttk.Label(mainframe, text="cost of Helium (€/m^3)").grid(column=3, row=4, sticky=W)
he_cost_entry = ttk.Entry(mainframe, width=8, textvariable=he_cost)
he_cost_entry.grid(column=4, row=4, sticky=(W, E))

ttk.Label(mainframe, text="cost of compressor fill (€)").grid(column=3, row=5, sticky=W)
fill_cost_entry = ttk.Entry(mainframe, width=8, textvariable=fill_cost)
fill_cost_entry.grid(column=4, row=5, sticky=(W, E))

# the radio buttons to select method, rows, 9-11
method = StringVar(root, value="tmx")
m_pp = ttk.Radiobutton(mainframe, text='1. Partial Pressure fill, 1st He, 2nd O2, 3rd air',
                       variable=method, value='pp').grid(column=1, row=9, sticky=W, columnspan=2)
m_cfm = ttk.Radiobutton(mainframe, text='2. Helium then Nitrox CFM',
                        variable=method, value='cfm').grid(column=1, row=10, sticky=W, columnspan=2)
m_tmx = ttk.Radiobutton(mainframe, text='3. Trimix CFM',
                        variable=method, value='tmx').grid(column=1, row=11, sticky=W, columnspan=2)

# the button to invoke calculation
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=1, row=12, sticky=W)

# button for copying result to clipcoard
ttk.Button(mainframe, text="HELP", command=help_action).grid(column=2, row=12, sticky=W)

# the bottom label to print results
ttk.Label(mainframe, text="result", font="bold", relief=RAISED) \
    .grid(column=1, row=13, sticky=(E, W), columnspan=2)
result_pp_label = ttk.Label(mainframe, textvariable=result_pp).grid(
    column=1, row=14, sticky=(E, W), columnspan=2)

result_pp_label = ttk.Label(mainframe, textvariable=total_cost).grid(
    column=3, row=14, sticky=(W, N), columnspan=2)

## padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=2, pady=2)

# focus to the first entry field
start_bar_entry.focus()
# pressing return same as click calcualte button
root.bind('<Return>', calculate)
# main window loop starts now
root.mainloop()

# done






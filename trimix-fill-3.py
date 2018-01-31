#!/usr/bin/python
# (c) 2017 Ian Leiman, ian.leiman@gmail.com
# trimix-fill-3.py
# github project https://github.com/eianlei/trimix-fill/
# Python-3 script using tkinter (v 8.5 or higher) as GUI
# calculates trimix blending for 3 different fill methods
# works also for Nitrox
# use at your own risk, no guarantees, no liability!
#
from tkinter import *
from tkinter import ttk
import time

root = Tk()
root.title("Trimix fill calculator, 3 selectable methods")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

pp_ok = "is possible without bleeding"
method = StringVar()

def calculate(*args):
    try:
        m = method.get()
#        print(m)

        # convert input strings to floats
        tbar_1   = float(start_bar.get())
        endbar   = float(end_bar.get())
        start_o2 = float(start_o2_pct.get()) 
        start_he = float(start_he_pct.get()) 
        end_o2   = float(end_o2_pct.get()) 
        end_he   = float(end_he_pct.get())
        # cost calculation input
        liters        = float(tank_lit.get())
        o2_cost_eur   = float(o2_cost.get())
        he_cost_eur   = float(he_cost.get())
        fill_cost_eur = float(fill_cost.get())

##        #print to console for debugging
##        print("tbar_1 = {}".format(tbar_1))
##        print("endbar = {}".format(endbar))
##        print("start_o2 = {}".format(start_o2))
##        print("start_he = {}".format(start_he))
##        print("end_o2 = {}".format(end_o2))
##        print("end_he = {}".format(end_he))
        
        # error checking for input values
        if tbar_1 <0 or endbar <0:
            result_pp.set("tank pressure cannot be <0")
            return 
        if tbar_1 > 300 or endbar >300:
            result_pp.set("tank pressure in Bar cannot be >300")
            return 
        if endbar <= tbar_1:
            result_pp.set("wanted tank pressure must be higher than current")
            return 
        if start_o2 <0 or start_he <0 or end_o2 <0 or end_he <0 or start_o2 >100 \
           or start_he >100 or end_o2 >100 or end_he >100:
            result_pp.set("enter oxygen/helium content in percentage from 0 to 100")
            return 
        if (start_o2 + start_he > 100) or (end_o2 + end_he > 100):
            result_pp.set("O2 + He percentage cannot exceed 100")
            return 
               
        # do the calculations
#        print("he_ignore.get = {}".format(he_ignore.get()))
        if he_ignore.get() == 1:
            add_he = 0
            end_o2_bar = endbar * end_o2 /100
            start_he_bar = tbar_1 * start_he /100 
            end_he_bar = start_he_bar
            end_he = 100* start_he_bar /endbar
            mix_he_pct = end_he
            tbar_2 = tbar_1 
            add_air = (endbar * (1 - end_he/100- end_o2/100)
                     - tbar_1 * (1 - start_o2/100 - start_he/100) ) / 0.79
            
            tbar_3 = endbar - add_air
            add_o2 = tbar_3 - tbar_2
            start_o2_bar = tbar_1 * start_o2 /100
            mix_o2_pct = 100* (start_o2_bar + add_o2 + add_air*0.21)/endbar
            mix_he_pct = 100* (start_he_bar + add_he)/endbar
            mix_n_pct = 100 - mix_he_pct - mix_o2_pct
            add_nitrox = endbar - tbar_2
            nitrox_pct = 100* ((end_o2_bar - start_o2_bar) / add_nitrox)
            add_tmx = endbar - tbar_1
            tmx_he_pct = 100* (end_he_bar - start_he_bar) / add_tmx
            tmx_o2_pct = 100* (end_o2_bar - start_o2_bar) / add_tmx
            tmx_preo2_pct = tmx_o2_pct * ((100 - tmx_he_pct)/100)
            print("==1 ")
             
        else :
            end_he_bar = endbar * end_he /100
            end_o2_bar = endbar * end_o2 /100
            start_he_bar = tbar_1 * start_he /100 
            add_he = end_he_bar - start_he_bar
            tbar_2 = tbar_1 + add_he
            add_air = (endbar * (1 - end_he/100- end_o2/100)
                     - tbar_1 * (1 - start_o2/100 - start_he/100) ) / 0.79
            
            tbar_3 = endbar - add_air
            add_o2 = tbar_3 - tbar_2
            start_o2_bar = tbar_1 * start_o2 /100
            mix_o2_pct = 100* (start_o2_bar + add_o2 + add_air*0.21)/endbar
            mix_he_pct = 100* (start_he_bar + add_he)/endbar
            mix_n_pct = 100 - mix_he_pct - mix_o2_pct
            add_nitrox = endbar - tbar_2
            nitrox_pct = 100* ((end_o2_bar - start_o2_bar) / add_nitrox)
            add_tmx = endbar - tbar_1
            tmx_he_pct = 100* (end_he_bar - start_he_bar) / add_tmx
            tmx_o2_pct = 100* (end_o2_bar - start_o2_bar) / add_tmx
            tmx_preo2_pct = tmx_o2_pct * ((100 - tmx_he_pct)/100)
            print("==0 ")
        # end else

##        #print to console for debugging
##        print("tbar_2 = {}".format(tbar_2))
##        print("tbar_3 = {}".format(tbar_3))
##        print("end_he_bar = {}".format(end_he_bar))
##        print("end_o2_bar  = {}".format( end_o2_bar))
##        print("start_he_bar  = {}".format(start_he_bar ))
##        print("start_o2_bar  = {}".format(start_o2_bar ))
##        print("add_he  = {}".format(add_he ))
##        print("add_o2  = {}".format(add_o2))
##        print("add_nitrox  = {}".format(add_nitrox ))
##        print("add_tmx  = {}".format(add_tmx ))
##        print("add_air = {}".format(add_air ))


        #error checking for results
        if add_he < 0 or add_o2 < -0.1 or add_air < 0:
            result_pp.set("blending this mix is not possible!")
            print("add_he {}, add_o2 {}, add_air {}".format(add_he, add_o2, add_air))
            return 
        if m == "cfm" and nitrox_pct < 21:
            result_pp.set("Nitrox CFM O2% <21% cannot be made!")
            return 
        if m == "cfm" and nitrox_pct > 36:
            result_pp.set("Nitrox CFM O2% >36% cannot be made!")
            return 
        if m == "tmx" and tmx_he_pct > 36:
            result_pp.set("Trimix CFM Helium % >36% cannot be made!")
            return 
        if m == "tmx" and tmx_o2_pct > 36:
            result_pp.set("Trimix CFM where Oxygen % >36% cannot be made!")
            return 
        if m == "tmx" and tmx_preo2_pct < 12:
            result_pp.set("Trimix CFM where Oxygen % <18% cannot be made!")
            return 

        # create result strings
        if add_he > 0 :
            he_fill =  "From {:.1f} bars add {:.1f} bar Helium,".format(tbar_1, add_he)
        else :
            he_fill = " - no helium added"
        if add_o2 > 0.1 :
            o2_fill =  "From {:.1f} bars add {:.1f} bar Oxygen,".format(tbar_2, add_o2)
        else :
            o2_fill = " - no oxygen added"
        if add_nitrox > 0 :
            nitrox_fill =  "From {:.1f} bars add {:.1f} bar {:.1f}% NITROX BY CFM,".format(tbar_2, add_nitrox, nitrox_pct)
        else :
            nitrox_fill = " - no Nitrox added"
        if add_tmx > 0 :
            tmx_fill =  "From {:.1f} bars add {:.1f} bar {:.1f}/{:.1f} TRIMIX BY CFM,".format(tbar_1, add_tmx, tmx_o2_pct, tmx_he_pct)
        else :
            tmx_fill = " - no Trimix added"

        result_mix = "Resulting mix will be {:.0f}/{:.0f}/{:.0f} (O2/He/N).".format(\
            mix_o2_pct, mix_he_pct, mix_n_pct )

        if m == "pp" :
            result = "PARTIAL PRESSURE BLENDING:\n"\
            "** {}.\n"\
            "{}\n"\
            "{}\n"\
            "From {:.1f} bars add {:.1f} bar air to {:.1f} bar.  \n"\
            "{}\n".format(\
             pp_ok, he_fill, o2_fill, tbar_3, add_air, endbar,\
             result_mix )
            
        elif m == "cfm" :
            result = "Pure Helium + Nitrox CFM blending:\n****\n"\
            "{}\n"\
            "{}\n"\
            "{}\n".format(\
             he_fill, nitrox_fill, result_mix )

        elif m == "tmx" :
            result = "TMX CFM blending:\n{}\n"\
                     "first open helium flow and adjust O2 to {:.1f}%\n"\
                     "then open oxygen flow and adjust O2 to {:.1f}%\n{}\n".format(\
                         tmx_fill, tmx_preo2_pct, tmx_o2_pct, result_mix)
        else :
            result = "no method selected"
            

        ### the output result printed to the bottom label widget
        result_pp.set( result )
        # cost calculation
        o2_lit = liters * endbar * (add_o2/endbar)
        he_lit = liters * endbar * (add_he/endbar)
        o2_eur = o2_lit * o2_cost_eur / 1000
        he_eur = he_lit * he_cost_eur / 1000
        total_cost_eur = fill_cost_eur + o2_eur + he_eur
        total_cost_string = "Total cost of the fill is:\n{:.2f} €\n"\
                            " # {:.0f} liters Oxygen costing {:.2f} €\n"\
                            " # {:.0f} liters Helium costing {:.2f} €\n".format(\
                            total_cost_eur, o2_lit, o2_eur, he_lit, he_eur )
        total_cost.set ( total_cost_string)
        ## copy results to clipboard
        root.clipboard_clear()
        root.clipboard_append("Output result from Trimix fill calculator\n")
        root.clipboard_append("=========================================\n")
        root.clipboard_append(time.strftime("%Y-%m-%d %H:%M"))
        root.clipboard_append("\n- current tank {} bar, {} liters, mix {}/{}\n".format
                              (tbar_1, liters, start_o2, start_he))
        root.clipboard_append("- wanted mix {}/{}\n".format(end_o2, end_he))
        root.clipboard_append("\n{}\n\n{}\n".format(result, total_cost_string))

    except ValueError:
        result_pp.set("enter all values as numbers!")
        pass
    
def help_action(*args):
        print("HELP button pressed")




# define all strings for input and output, set default values
start_bar = StringVar(root, value="0")
start_o2_pct = StringVar(root, value="21")
start_he_pct = StringVar(root, value="35")
end_bar = StringVar(root, value="200")
end_o2_pct = StringVar(root, value="21")
end_he_pct = StringVar(root, value="35")
result_pp = StringVar(root)

tank_lit = StringVar(root, value="24")
o2_cost = StringVar(root, value="4.15")
he_cost = StringVar(root, value="25")
fill_cost = StringVar(root, value="5")
total_cost = StringVar (root)

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

# grey out Helium input widgets
he_ignore = IntVar(root, value=0)
def he_ignore_change(*args):
    heg = he_ignore.get()
    print("He cb value {}".format( heg) )
    if heg == 1 :
            end_he_label.configure(style="Grey.TLabel")
            end_he_pct_entry.configure(state='disabled')
    else :
            end_he_label.configure(style="Black.TLabel")
            end_he_pct_entry.configure(state='enabled')

ttk.Checkbutton(mainframe, text="no He filled & ignore He target", variable= he_ignore,
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
m_pp =  ttk.Radiobutton(mainframe, text='1. Partial Pressure fill, 1st He, 2nd O2, 3rd air',\
                        variable=method, value='pp').grid(column=1, row=9, sticky=W, columnspan=2)
m_cfm = ttk.Radiobutton(mainframe, text='2. Helium then Nitrox CFM',\
                        variable=method, value='cfm').grid(column=1, row=10, sticky=W, columnspan=2)
m_tmx = ttk.Radiobutton(mainframe, text='3. Trimix CFM',\
                        variable=method, value='tmx').grid(column=1, row=11, sticky=W, columnspan=2)


# the button to invoke calculation
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=1, row=12, sticky=W)

# button for copying result to clipcoard
ttk.Button(mainframe, text="HELP", command=help_action).grid(column=2, row=12, sticky=W)

# the bottom label to print results
ttk.Label (mainframe, text="result", font="bold", relief=RAISED)\
          .grid(column=1, row=13, sticky=(E,W), columnspan=2)
result_pp_label = ttk.Label (mainframe, textvariable=result_pp).grid(
    column=1, row=14, sticky= (E,W), columnspan=2)

result_pp_label = ttk.Label (mainframe, textvariable= total_cost).grid(
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

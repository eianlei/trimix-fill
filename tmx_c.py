#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# tmx_c.py
# github project https://github.com/eianlei/trimix-fill/
# trimix blending calculator, command line version
#  this calls function tmx_calc
# use at your own risk, no guarantees, no liability!
#
import sys
import argparse
from tmx_calc import tmx_calc
from tmx_calc import tmx_cost_calc

# example tmx_c.py -m pp -sb 67 -eb 200 -so 20 -sh 34 -eo 21 -eh 35
# nota that argparse help strings may not contain % character, therefore pct
parser = argparse.ArgumentParser(
    description="calculates trimix blending for 3 different fill methods "
    "and optionally the cost of filling",
    epilog="use at your own risk!"
)

# define for argparse all input arguments
parser.add_argument('-m', action='store', dest='method',
                    help='fill method (default: %(default)s)',
                    choices=['pp', 'cfm', 'tmx'],default="tmx",)
parser.add_argument('-sb', type=int, action='store', dest='start_bar', help='start bar (default: %(default)d)', default=0)
parser.add_argument('-eb', type=int, action='store', dest='end_bar', help='end bar (default: %(default)d)', default=200)
parser.add_argument('-so', type=int, action='store', dest='start_o2', help='start O2 pct (default: %(default)d)', default=21)
parser.add_argument('-sh', type=int, action='store', dest='start_he', help='start He pct (default: %(default)d)', default=35)
parser.add_argument('-eo', type=int, action='store', dest='end_o2', help='end O2 pct (default: %(default)d)', default=21)
parser.add_argument('-eh', type=int, action='store', dest='end_he', help='end He pct (default: %(default)d)', default=35)
parser.add_argument('-i', action='store_true', default=False, dest='he_ignore',
                    help='ignore helium target and no He filled')
parser.add_argument('-c', action='store_true', default=False, dest='cost',
                    help='calculate also cost, use args l, co, ch, cf')
parser.add_argument('-l', type=int, action='store', dest='liters', help='tank volume in liters (default: %(default)d)', default=24)
parser.add_argument('-co', type=int, action='store', dest='o2_eur', help='oxygen cost eur/cu-m (default: %(default)d)', default=4.15)
parser.add_argument('-ch', type=int, action='store', dest='he_eur', help='helium cost eur/cu-m (default: %(default)d)', default=25)
parser.add_argument('-cf', type=int, action='store', dest='fill_eur', help='fill cost air in eur (default: %(default)d)', default=5)
parser.add_argument('-v', action='store_true', default=False, dest='verbose',
                    help='verbose output with all input/output data')

pargs = parser.parse_args()
# check if -h or --help is first arg, then quit, argparse has printed help message already
if len(sys.argv) > 1 :
    if sys.argv[1] == "-h" or sys.argv[1] == "--help" :
        sys.exit() # quit(0)

# if we get here, then either we have some arguments, or no args and are going with defaults
# get the arguments for tmx_calc(), we could skip this, but makes debugging nicer
filltype  = pargs.method
start_bar = pargs.start_bar
end_bar   = pargs.end_bar
start_o2  = pargs.start_o2
start_he  = pargs.start_he
end_o2    = pargs.end_o2
end_he    = pargs.end_he
he_ignore = pargs.he_ignore
## args for -c
cost      = pargs.cost
liters    = pargs.liters
o2_eur    = pargs.o2_eur
he_eur    = pargs.he_eur
fill_eur  = pargs.fill_eur
verbose   = pargs.verbose

# in verbose mode print the input args
if verbose :
    print ("tmx_c input arguments:")
    print ("method    = ", pargs.method)
    print ("start_bar = ", pargs.start_bar)
    print ("end_bar   = ", pargs.end_bar)
    print ("start_o2  = ", pargs.start_o2)
    print ("start_he  = ", pargs.start_he)
    print ("end_o2    = ", pargs.end_o2)
    print ("end_he    = ", pargs.end_he)
    print ("he_ignore = ", pargs.he_ignore)
    print ("cost      = ", pargs.cost)
    print ("liters    = ", pargs.liters)
    print ("o2_eur    = ", pargs.o2_eur)
    print ("he_eur    = ", pargs.he_eur)
    print ("fill_eur  = ", pargs.fill_eur)
    print ("***************** output:")

# now calculate the fill
result = tmx_calc(filltype, start_bar, end_bar, start_o2, start_he, end_o2, end_he,
                  he_ignore)

# print verbose results
if verbose :
    for i in result :
        print (i, "= ", result[i])
else :
    # print just plain text result
    print(result['status_text'])

# calculate also cost if -c
if cost :
    add_o2 = result['add_o2']
    add_he = result['add_he']
    cost_result = tmx_cost_calc(liters, end_bar, add_o2, add_he, o2_eur,
                                he_eur, fill_eur)
    total_cost_string = cost_result['result_txt']
    print("COST OF THE FILL:")
    print(total_cost_string)


    # input parameters to tmx_calc:
    #  filltype: {pp, cfm, tmx}
    #       pp = partial pressure,
    #       cfm= decant Helium + continuous flow Nitrox,
    #       tmx = tmx cfm
    #  start_bar: tank start pressure in bar, must be >=0 and <= 300
    #  end_bar: tank end pressure in bar, must be >=0 and <= 300
    #  start_o2: tank starting o2%, must be >=0 and <= 100
    #  start_he: tank starting he%, must be >=0 and <= 100
    #  end_o2: wanted 02%, must be >=0 and <= 100
    #  end_he: wanted he%, must be >=0 and <= 100
    #  he_ignore: boolean, true = ignore helium target, plain Nitrox fill

    # input parameters to tmx_cost_calc
    #      liters : size of your tank to be filled in liters (water colume)
    #      fill_bar : end pressure of the tank in bars
    #      add_o2 : bars of pure oxygen filled (not including what is in air fill)
    #      add_he : bars of pure helium filled by pp or cfm
    #          note that remaining part of gas to fill is assumed to be air
    #      o2_cost_eur : cost of pure oxygen in Euros per cubic meter
    #      he_cost_eur : cost of pure helium in Euros per cubic meter
    #      fill_cost_eur : one time cost for using the compressor to top with air or cfm gas
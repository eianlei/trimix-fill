#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# tmx_tests.py
# github project https://github.com/eianlei/trimix-fill/
#
# some quick testing for functions in tmx_calc.py
#

from tmx_calc import *
# tests for function tmx_calc(filltype="pp", start_bar=0, end_bar=200,
#             start_o2=21, start_he=35, end_o2=21, end_he=35,
#             he_ignore=False):

# run test, short output of results
def runtest(*test_in) :
    print ("tmxcalc(", *test_in, ")")
    result = tmx_calc(*test_in)
    print ("returns: ", result['status_code'])
    print (result['status_text'])

# run test, output all results
def runtest2(*test_in) :
    print ("tmxcalc(", *test_in, ")")
    result = tmx_calc(*test_in)
    for i in result :
        print (i, result[i])

# # the easy normal cases, fill from empty
# runtest("pp", 0, 200, 21, 35, 21, 35, False)
# runtest("cfm", 0, 200, 0, 35, 21, 35, False)
# runtest("tmx", 0, 200, 0, 99, 21, 35, False)
#
# # refill from 90 bar TMX 21/35
# for i in ["pp","cfm", "tmx"] :
#     runtest(i,  90, 200, 20, 34, 21, 35, False)
#
# #wrong inputs should produce errors
# runtest("xxx", 0, 200, 0, 99, 21, 35, False)
# runtest("tmx", -1, 200, 0, 99, 21, 35, False)
# runtest("tmx", 300, 2000, 0, 99, 21, 35, False)
# runtest("tmx", 100, 90, 0, 99, 21, 35, False)
# runtest("tmx", 100, 400, 400, 99, 21, 35, False)
#
# runtest("tmx", 100, 200, -3, 99, 21, 35, False)
# runtest("tmx", 100, 200, 88, -99, 21, 35, False)
# runtest("tmx", 100, 200, 88, 99, -10, 35, False)
# runtest("tmx", 100, 200, 88, 99, 21, -35, False)
#
# runtest("pp", 0, 200, 200, 99, 21, 35, False)
# runtest("pp", 0, 200, 20, 199, 21, 35, False)
# runtest("pp", 0, 200, 20, 99, 200, 35, False)
# runtest("pp", 0, 200, 200, 99, 21, 350, False)
#
# runtest("pp", 0, 200, 60, 70, 21, 35, False)
# runtest("pp", 0, 200, 21, 0, 70, 70, False)
#
# #cfm fill corner cases
# runtest("cfm", 0, 200, 50, 0, 36, 50, True) # maximum 02
# runtest("cfm", 0, 200, 50, 0, 37, 50, True) # too much 02
# runtest("cfm", 0, 200, 50, 0, 20, 50, True) # too little 02

# # Nitrox pp fills
# runtest("pp", 0, 200, 32, 0, 20, 0, True) # fails, 02 < 21%

# # PP fills for Nitrox from empty, test a wide range
# for o2 in range(21,100,1) :
#     runtest("pp", 0, 200, 32, 0, o2, 0, True)

# # PP fills for Nitrox from empty, test a wide range
for xx in range(0,200,10) :
     runtest("cfm", xx, 200, 18, 45, 21, 35, False)
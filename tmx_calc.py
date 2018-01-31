#!/usr/bin/python
# (c) 2018 Ian Leiman, ian.leiman@gmail.com
# tmx_calc.py
# github project https://github.com/eianlei/trimix-fill/
# Python-3 function calculates trimix blending for 3 different fill methods
# use at your own risk, no guarantees, no liability!
#
def tmx_calc(filltype="pp", start_bar=0, end_bar=200,
             start_o2=21, start_he=35, end_o2=21, end_he=35,
             he_ignore=False):
    """calculates trimix blending for 3 different fill methods"""
    # input parameters:
    #  filltype: pp = partial pressure, cfm= decant Helium + continuous flow Nitrox, tmx = tmx cfm
    #  start_bar: tank start pressure in bar
    #  end_bar: tank end pressure in bar
    #  start_o2: tank starting o2%
    #  start_he: tank starting he%
    #  end_o2: wanted 02%
    #  end_he: wanted he%
    #  he_ignore: boolean, true = ignore helium target, plain Nitrox fill
    #
    # return dictionary tmx_result, following keys:
    #  status_code: 0 if all OK, 10...20 input errors 50...60 calculation errors, 99 fatal
    #  status_text: human readable output text, error or result
    #  tbar_2 : for pp fill, the 2nd pressure in bar to fill Helium
    #  add_he: how many bars Helium to pp fill
    #  add_o2 : how many bars Oxygen to pp fill
    #  add_nitrox : how many bars Nitrox to fill by CFM
    #  nitrox_pct : O2% of Nitrox in CFM fill
    #  add_tmx : how many bars TMX to in TMX CFM
    #  tmx_o2_pct :  O2% of TMX to fill
    #  tmx_he_pct :  He% of TMX to fill
    #  mix_o2_pct : resulting O2%, should match end_o2
    #  mix_he_pct : resulting He%, should match end_he
    #  mix_n_pct : resulting N2%
    #
    ##########################################################################
    # define the return values dictionary tmx_result
    # initialize with default values
    tmx_result = {'status_code': 99,  # 99 remains if something fatal happens
                  'status_text': 'FATAL ERROR',  # this is overwritten by something else
                  'tbar_2': 0,
                  'add_he': 0,
                  'add_o2': 0,
                  'add_nitrox': 0,
                  'nitrox_pct': 0,
                  'add_tmx': 0,
                  'tmx_o2_pct': 0,
                  'tmx_he_pct': 0,
                  'mix_o2_pct': 0,
                  'mix_he_pct': 0,
                  'mix_n_pct': 0
                  }

    # error checking for input values, anything wrong and we return an error & skip calculations
    if filltype not in ['pp', 'cfm', 'tmx']:
        tmx_result['status_code'] = 10
        tmx_result['status_text'] = 'filltype not supported <' + filltype + '>'
        return tmx_result
    if start_bar < 0:
        tmx_result['status_code'] = 11
        tmx_result['status_text'] = 'tank start pressure cannot be <0'
        return tmx_result
    if start_bar < 0 or end_bar < 0:
        tmx_result['status_code'] = 12
        tmx_result['status_text'] = 'tank end pressure cannot be <0'
        return tmx_result
    if start_bar > 300:
        tmx_result['status_code'] = 13
        tmx_result['status_text'] = "tank start pressure in Bar cannot be >300"
        return tmx_result
    if end_bar > 300:
        tmx_result['status_code'] = 14
        tmx_result['status_text'] = "tank end pressure in Bar cannot be >300"
    if end_bar <= start_bar:
        tmx_result['status_code'] = 15
        tmx_result['status_text'] = "wanted tank end pressure must be higher than start pressure"
        return tmx_result
    if start_o2 < 0:
        tmx_result['status_code'] = 16
        tmx_result['status_text'] = "starting oxygen content cannot be <0%"
        return tmx_result
    if start_he < 0:
        tmx_result['status_code'] = 17
        tmx_result['status_text'] = "starting helium content cannot be <0%"
        return tmx_result
    if end_o2 < 0:
        tmx_result['status_code'] = 18
        tmx_result['status_text'] = "wanted oxygen content cannot be <0%"
        return tmx_result
    if end_he < 0:
        tmx_result['status_code'] = 9
        tmx_result['status_text'] = "wanted helium content cannot be <0%"
        return tmx_result
    if start_o2 > 100:
        tmx_result['status_code'] = 10
        tmx_result['status_text'] = "starting oxygen content cannot be >100%"
        return tmx_result
    if start_he > 100:
        tmx_result['status_code'] = 11
        tmx_result['status_text'] = "starting helium content cannot be >100%"
        return tmx_result
    if end_o2 > 100:
        tmx_result['status_code'] = 12
        tmx_result['status_text'] = "wanted oxygen content cannot be >100%"
        return tmx_result
    if end_he > 100:
        tmx_result['status_code'] = 13
        tmx_result['status_text'] = "wanted helium content cannot be >100% "
        return tmx_result
    if start_o2 + start_he > 100:
        tmx_result['status_code'] = 14
        tmx_result['status_text'] = "starting O2 + He percentage cannot exceed 100"
        return tmx_result
    if end_o2 + end_he > 100:
        tmx_result['status_code'] = 14
        tmx_result['status_text'] = "wanted O2 + He percentage cannot exceed 100"
        return tmx_result

    # do the calculations
    # two cases: for plain Nitrox and actual Trimix fill
    if he_ignore:
        # calculate for Nitrox fill, igonore end_he target, no Helium is going in
        add_he = 0
        end_o2_bar = end_bar * end_o2 / 100
        start_he_bar = start_bar * start_he / 100
        end_he_bar = start_he_bar
        end_he = 100 * start_he_bar / end_bar
        mix_he_pct = end_he
        tbar_2 = start_bar
        add_air = (end_bar * (1 - end_he / 100 - end_o2 / 100)
                   - start_bar * (1 - start_o2 / 100 - start_he / 100)) / 0.79

        tbar_3 = end_bar - add_air
        add_o2 = tbar_3 - tbar_2
        start_o2_bar = start_bar * start_o2 / 100
        mix_o2_pct = 100 * (start_o2_bar + add_o2 + add_air * 0.21) / end_bar
        mix_he_pct = 100 * (start_he_bar + add_he) / end_bar
        mix_n_pct = 100 - mix_he_pct - mix_o2_pct
        add_nitrox = end_bar - tbar_2
        nitrox_pct = 100 * ((end_o2_bar - start_o2_bar) / add_nitrox)
        add_tmx = end_bar - start_bar
        tmx_he_pct = 100 * (end_he_bar - start_he_bar) / add_tmx
        tmx_o2_pct = 100 * (end_o2_bar - start_o2_bar) / add_tmx
        tmx_preo2_pct = tmx_o2_pct * ((100 - tmx_he_pct) / 100)

    else:
        # calculate for a trimix fill, Helium is added
        end_he_bar = end_bar * end_he / 100
        end_o2_bar = end_bar * end_o2 / 100
        start_he_bar = start_bar * start_he / 100
        add_he = end_he_bar - start_he_bar
        tbar_2 = start_bar + add_he
        add_air = (end_bar * (1 - end_he / 100 - end_o2 / 100)
                   - start_bar * (1 - start_o2 / 100 - start_he / 100)) / 0.79

        tbar_3 = end_bar - add_air
        add_o2 = tbar_3 - tbar_2
        start_o2_bar = start_bar * start_o2 / 100
        mix_o2_pct = 100 * (start_o2_bar + add_o2 + add_air * 0.21) / end_bar
        mix_he_pct = 100 * (start_he_bar + add_he) / end_bar
        mix_n_pct = 100 - mix_he_pct - mix_o2_pct
        add_nitrox = end_bar - tbar_2
        nitrox_pct = 100 * ((end_o2_bar - start_o2_bar) / add_nitrox)
        add_tmx = end_bar - start_bar
        tmx_he_pct = 100 * (end_he_bar - start_he_bar) / add_tmx
        tmx_o2_pct = 100 * (end_o2_bar - start_o2_bar) / add_tmx
        tmx_preo2_pct = tmx_o2_pct * ((100 - tmx_he_pct) / 100)
    # end else

    # error checking for results, anything wrong and we return error code
    if add_he < 0 or add_o2 < -0.1 or add_air < 0:
        tmx_result['status_code'] = 51
        tmx_result['status_text'] = "blending this mix is not possible!" + \
                                    "<add_he {}, add_o2 {}, add_air {}>".format(add_he, add_o2, add_air)
        return tmx_result
    if filltype == "cfm" and nitrox_pct < 21:
        tmx_result['status_code'] = 52
        tmx_result['status_text'] = "Nitrox CFM O2% <21% cannot be made!"
        return tmx_result
    if filltype == "cfm" and nitrox_pct > 36:
        tmx_result['status_code'] = 53
        tmx_result['status_text'] = "Nitrox CFM O2% >36% cannot be made!"
        return tmx_result
    if filltype == "tmx" and tmx_he_pct > 36:
        tmx_result['status_code'] = 54
        tmx_result['status_text'] = "Trimix CFM Helium % >36% cannot be made!"
        return tmx_result
    if filltype == "tmx" and tmx_o2_pct > 36:
        tmx_result['status_code'] = 55
        tmx_result['status_text'] = "Trimix CFM where Oxygen % >36% cannot be made!"
        return tmx_result
    if filltype == "tmx" and tmx_preo2_pct < 12:
        tmx_result['status_code'] = 56
        tmx_result['status_text'] = "Trimix CFM where Oxygen % <18% cannot be made!"
        return tmx_result

    # since we are here, then all error checking has passed, and numerical results should be valid
    # build nice text to return at tmx_result['status_text']
    if add_he > 0:
        he_fill = "From {:.1f} bars add {:.1f} bar Helium," \
            .format(start_bar, add_he)
    else:
        he_fill = " - no helium added"
    if add_o2 > 0.1:
        o2_fill = "From {:.1f} bars add {:.1f} bar Oxygen," \
            .format(tbar_2, add_o2)
    else:
        o2_fill = " - no oxygen added"
    if add_nitrox > 0:
        nitrox_fill = "From {:.1f} bars add {:.1f} bar {:.1f}% NITROX BY CFM,"\
            .format(tbar_2, add_nitrox, nitrox_pct)
    else:
        nitrox_fill = " - no Nitrox added"
    if add_tmx > 0:
        tmx_fill = "From {:.1f} bars add {:.1f} bar {:.1f}/{:.1f} TRIMIX BY CFM,"\
            .format(start_bar, add_tmx, tmx_o2_pct, tmx_he_pct)
    else:
        tmx_fill = " - no Trimix added"

    result_mix = "Resulting mix will be {:.0f}/{:.0f}/{:.0f} (O2/He/N).".format(
        mix_o2_pct, mix_he_pct, mix_n_pct)

    if filltype == "pp":
        result = "PARTIAL PRESSURE BLENDING:\n" \
                 "{}\n" \
                 "{}\n" \
                 "From {:.1f} bars add {:.1f} bar air to {:.1f} bar.  \n" \
                 "{}\n".format(
            he_fill, o2_fill, tbar_3, add_air, end_bar,
            result_mix)

    elif filltype == "cfm":
        result = "Pure Helium + Nitrox CFM blending:\n" \
                 "{}\n" \
                 "{}\n" \
                 "{}\n".format(
            he_fill, nitrox_fill, result_mix)

    elif filltype == "tmx":
        result = "TMX CFM blending:\n{}\n" \
                 "first open helium flow and adjust O2 to {:.1f}%\n" \
                 "then open oxygen flow and adjust O2 to {:.1f}%\n{}\n".format(
            tmx_fill, tmx_preo2_pct, tmx_o2_pct, result_mix)

    ### now copy the calculated values from locals to dictionary we return
    tmx_result['status_code'] = 0         # ok, results are valid
    tmx_result['status_text'] = result    # human readable recipe text
    tmx_result['tbar_2'] = tbar_2
    tmx_result['add_he'] = add_he
    tmx_result['add_o2'] = add_o2
    tmx_result['add_nitrox'] = add_nitrox
    tmx_result['nitrox_pct'] = nitrox_pct
    tmx_result['add_tmx'] = add_tmx
    tmx_result['tmx_o2_pct'] = tmx_o2_pct
    tmx_result['tmx_he_pct'] = tmx_he_pct
    tmx_result['mix_o2_pct'] = mix_o2_pct
    tmx_result['mix_he_pct'] = mix_he_pct
    tmx_result['mix_n_pct'] = mix_n_pct
    return tmx_result
# end

def tmx_cost_calc(liters, endbar, add_o2, add_he, o2_cost_eur, he_cost_eur, fill_cost_eur) :
     """calculate the cost of a trimix fill"""
     # define the return values dictionary tmx_cost_result
     # initialize with default values
     tmx_cost_result = {'status_code': 99,
                        'result_txt' : "ERROR"}

     # cost calculation
     o2_lit = liters * endbar * (add_o2 / endbar)
     he_lit = liters * endbar * (add_he / endbar)
     o2_eur = o2_lit * o2_cost_eur / 1000
     he_eur = he_lit * he_cost_eur / 1000
     total_cost_eur = fill_cost_eur + o2_eur + he_eur
     total_cost_string = "Total cost of the fill is:\n{:.2f} €\n" \
                         " # {:.0f} liters Oxygen costing {:.2f} €\n" \
                         " # {:.0f} liters Helium costing {:.2f} €\n".format( \
         total_cost_eur, o2_lit, o2_eur, he_lit, he_eur)
     tmx_cost_result['result_txt'] = total_cost_string
     return tmx_cost_result
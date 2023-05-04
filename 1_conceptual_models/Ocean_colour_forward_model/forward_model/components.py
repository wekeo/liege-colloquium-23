"""Module responsible for the numerical calculations of the forward model."""

import numpy as np

def calc_aphy(abs, scatt, chl, maxval=0.000000001):

    aphy = abs*chl**(-1*scatt)
    aphy[aphy < maxval] = maxval

    return aphy

def calc_bbp_ph_nu(chl):

    if chl < 2:
        bbp_ph_nu = np.log10(chl) - 0.3
    else:
        bbp_ph_nu = 0

    return bbp_ph_nu

def calc_components(wavs, params, abs_water, abs_increment, scattering_coefficient, chl, nap, cdom):

    # pre calculations
    offset_wavs = wavs - 443
    aphy = calc_aphy(abs_increment, scattering_coefficient, chl)
    bbp_ph_nu = calc_bbp_ph_nu(chl)

    # absorption calculations
    aph = aphy * chl
    aNAP = nap * float(params["IOP_model"]["aNAP_star_443"]) * np.exp(-1 * float(params["IOP_model"]["SNAP"]) * offset_wavs)
    aCDOM = cdom * np.exp(-1 * float(params["IOP_model"]["SCDOM"]) * offset_wavs)
    total_absorption = abs_water + aph + aNAP + aCDOM

    # backscattering calculations
    bbw = float(params["IOPs_pure_water"]["bbw_bw"]) * float(params["IOPs_pure_water"]["bw500"]) * (wavs / 500.0) ** float(params["IOPs_pure_water"]["nw"])
    bbph = (0.002 + 0.01 * np.max([0.0, 0.5 - 0.25 * np.log10(chl)]) * (wavs / 550.0) ** bbp_ph_nu) * 0.416 * chl ** 0.766
    bbpNAP = float(params["IOP_model"]["bbp_star_555"]) * nap * (wavs / 555.0) ** float(params["IOP_model"]["np"])
    total_backscatter = bbw + bbph + bbpNAP

    # calculate Rrs
    gamma = np.pi * float(params["Reflectance_model"]["GothicR"]) * float(params["Reflectance_model"]["fprime_Q"])
    rrs = gamma * total_backscatter / (total_absorption + total_backscatter) / np.pi

    components = {}
    components["aw"] = abs_water
    components["aph"] = aph
    components["aNAP"] = aNAP
    components["aCDOM"] = aCDOM
    components["total_absorption"] = total_absorption
    components["bbw"] = bbw
    components["bbph"] = bbph
    components["bbpNAP"] = bbpNAP
    components["total_backscatter"] = total_backscatter
    components["rrs"] = rrs

    return components

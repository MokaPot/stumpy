#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from . import core

def mass(Q, T, M_T, Σ_T, trivial_idx=None, excl_zone=0, left=False, right=False):
    D = core.mass(Q, T, M_T, Σ_T)
    if trivial_idx is not None:
        zone_start = max(0, trivial_idx-excl_zone)
        zone_stop = trivial_idx+excl_zone+1
        D[zone_start:zone_stop] = np.inf

        #Get left and right matrix profiles
        IL = -1
        PL = np.inf
        if D[:trivial_idx].size:
            IL = np.argmin(D[:trivial_idx])
            PL = D[IL]
        if zone_start <= IL < zone_stop:
            IL = -1

        IR = -1
        PR = -1
        if D[trivial_idx:].size:
            IR = trivial_idx +  np.argmin(D[trivial_idx:])
            PR = D[IR]
        if zone_start <= IR < zone_stop:
            IR = -1

    # Element-wise Min
    I = np.argmin(D)
    P = D[I]

    if trivial_idx is not None and left:
        I = IL
        P = PL

    if trivial_idx is not None and right:
        I = IR
        P = PR

    return P, I

def stamp(T_A, T_B, m, ignore_trivial=False):
    """
    DOI: 10.1109/ICDM.2016.0179
    See Table III

    Timeseries, T_B, will be annotated with the distance location
    (or index) of all its subsequences in another times series, T_A.

    Return: For every subsequence, Q, in T_B, you will get a distance
    and index for the closest subsequence in T_A. Thus, the array
    returned will have length T_B.shape[0]-m+1
    """
    core.check_dtype(T_A)
    core.check_dtype(T_B)
    subseq_T_B = core.rolling_window(T_B, m)
    zone = int(np.ceil(m/2))
    M_T, Σ_T = core.compute_mean_std(T_A, m)

    # Add exclusionary zone
    if ignore_trivial:
        out = [mass(subseq, T_A, M_T, Σ_T, i, zone) for i, subseq in enumerate(subseq_T_B)]
    else:
        out = [mass(subseq, T_A, M_T, Σ_T) for subseq in subseq_T_B]
    out = np.array(out, dtype=object)
    
    return out

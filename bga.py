#!/usr/bin/env python
#
# Copyright (C) 2012 Russ Dill <Russ.Dill@asu.edu>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

import pscad
from decimal import Decimal as D
from string import ascii_uppercase
import itertools
import re

FF784 = {
    'name' :        "FF784",
    'pad_size' :    D("0.45"),
    'pitch' :       D("1.0"),
    'n_x' :         28,
    'n_y' :         28,
    'courtyard_x' : D("29.0"),
    'courtyard_y' : D("29.0"),
    'clearance' :   D("0.15"),
    'mask' :        D("0.05"),
    'silk' :        D("0.2"),
    'no_letter' :   "IOQSXZ"
}

DDR2_CLP = {
    'name' :        "DDR2_CLP",
    'pad_size' :    D("0.33"),
    'pitch' :       D("0.8"),
    'n_x' :         9,
    'n_y' :         22,
    'courtyard_x' : D("11.5"),
    'courtyard_y' : D("22.6"),
    'clearance' :   D("0.15"),
    'mask' :        D("0.05"),
    'silk' :        D("0.2"),
    'no_letter' :   "IOQSYZ",
    'skip' :        "A?.[4-6]|[BCWX].|A[AB]?[37]|[NRU]1|[PTV]9"
}

def bga_letters(skip):
    return itertools.ifilterfalse(lambda x: x in skip, ascii_uppercase)

def bga_dletters(skip):
    return (i[0] + i[1] for i in itertools.product([''] + list(bga_letters(skip)), bga_letters(skip)))

def bga_names(n, skip):
    return (i[0] + str(i[1]) for i in itertools.product(bga_dletters(skip), range(1, n+1)))

def bga(m):

    if 'skip' in m:
        skip = lambda name: re.match(m['skip'], name)
    else:
        skip = None

    row = pscad.row(pscad.circle(m['pad_size'] / D(2)), m['pitch'], m['n_x'], center=True)
    pads = (
        pscad.pad(bga_names(m['n_x'], m['no_letter']), m['clearance'], m['mask'], skip=skip) &
        pscad.rotate(270) & pscad.row(pscad.rotate(90) & row, m['pitch'], m['n_y'], center=True)
    )

    silk = pscad.silk(w=m['silk']) & (
        pscad.square((m['courtyard_x'], m['courtyard_y']), center=True) |

        pscad.translate([-m['courtyard_x'] / D(2), -m['pitch'] * (m['n_y'] - 1) / D(2)]) &
        pscad.left(m['silk'] * D(2)) & pscad.line([0, m['pitch'] * D(2)], center=True)
    )

    pscad.element(pads | silk, m['name'])

if __name__ == "__main__":
    bga(DDR2_CLP)


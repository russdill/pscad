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
import itertools
from decimal import Decimal as D


# http://pdfserv.maxim-ic.com/land_patterns/90-0167.PDF

QSOP16 = {
    'name': "QSOP-16",
    'pad_l': D("1.6"),
    'pad_w': D("0.356"),
    'width': D("5.309"),
    'pitch': D("0.635"),
    'n': 16,
    'rounding': D("0.05"),
    'D': D("4.98")
}

PW_R_PDSO_G16 = {
    'name': "PW (R-PDSO-G16)",
    'pad_l': D("1.60"),
    'pad_w': D("0.35"),
    'width': D("5.60"),
    'pitch': D("0.65"),
    'n': 16,
    'rounding': D("0.05"),
    'D': D("5.10")
}

# http://www.st.com/internet/com/TECHNICAL_RESOURCES/TECHNICAL_LITERATURE/PACKAGE_INFORMATION/CD00004814.pdf
TSSOP20 = {
    'name': "TSSOP-20",
    'pad_l': D("1.165"),
    'pad_w': D("0.36"),
    'width': D("6.095"),
    'pitch': D("0.65"),
    'n': 20,
    'rounding': D("0.05"),
    'D': D("6.6")
}


def sop(m, clearance, mask, silk_width):

    pad_row = pscad.row(pscad.rounded_square(
        (m['pad_w'], m['pad_l']), m['rounding'], center=True), m['pitch'], m['n'] / 2, center=True)

    pads = pscad.pad(itertools.count(1), clearance, mask) & (
        pscad.down(m['width'] / D(2)) & pad_row |
        pscad.up(m['width'] / D(2)) & pscad.rotate(180) & pad_row
    )

    silk = pscad.silk(w=silk_width) & (
        pscad.square([m['D'] + D(2), m['width'] + m['pad_l'] + D(1)], center=True) |

        pscad.down(m['width'] / D(2)) &
        pscad.left(silk_width + m['pitch'] * m['n'] / 4) &
        pscad.line([0, m['pad_l']], center=True)
    )

    pscad.element(pads | silk, m['name'])

if __name__ == "__main__":
    sop(TSSOP20, clearance = D("0.2"), mask = D("0.2"), silk_width = D("0.2"))

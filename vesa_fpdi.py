# module vesa_fpdi.py
#
# Copyright (C) 2013 Russ Dill <Russ.Dill@asu.edu>
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
import patterns


defaults = {
    'clearance' :   "0.30",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'placement' :   "0.25",
    'round_off' :   "0.1",
    'grid' :        "0.1"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad1 = pscad.rounded_square([D("0.7"), D("2.0")], m.round_off, center=True)
    pad1_row1 = pscad.pad(itertools.count(1, 2), m.clearance, m.mask) + (
        pscad.row(pad1, 1, (m.n + 1) / 2, center=True)
    )

    pad1_row2 = pscad.pad(itertools.count(2, 2), m.clearance, m.mask) + (
        pscad.row(pad1, 1, (m.n - 1) / 2, center=True)
    )

    pad2 = pscad.rounded_square([D("1.3"), D("3.4")], m.round_off, center=True)
    pad2_row = pscad.pad(m.n + 1, m.clearance, m.mask) + (
        pscad.row(pad2, (m.n - 1) / D(2) + D("5.7"), 2, center=True)
    )

    bore = pscad.hole(m.clearance, 0) + pscad.circle(D("1.3") / 2)
    bore_row = pscad.row(bore, (m.n - 1) / D(2) + D("3.1"), 2, center = True)

    # Reverse up/down for plug/receptacle
    pads = (
        bore_row,
        pscad.up(D("2.5")) + pad1_row1,
        pscad.down(D("2.5")) + pad1_row2,
        pad2_row,
        bore_row
    )

    all = pads
    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1)
    )

    return all, silk



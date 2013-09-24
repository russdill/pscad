# module cus-14b.py
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

    pad1 = pscad.rounded_square([D("0.7"), D("1.5")], m.round_off, center=True)
    pad1_row = pscad.pad(itertools.count(1), m.clearance, m.mask) + (
                   pscad.row(pad1, D("1.5"), 6, center=True)
    )

    pad2 = pscad.rounded_square([D("0.8"), 1], m.round_off, center=True)
    pad2_row = pscad.pad("7", m.clearance, m.mask) + (
                   pscad.rotate(90) + pscad.row(pad2, D("2.1"), 2, center=True)
    )

    bore = pscad.hole(m.clearance, 0) + pscad.circle(D("0.9") / 2)
    bore_row = pscad.row(bore, 5, 2, center = True)

    pads = (
        bore_row,
        pscad.up(1 + D("1.5") / 2) + pad1_row,
        pscad.left(D("11.8") / 2) + pad2_row,
        pscad.right(D("11.8") / 2) + pad2_row
    )

    all = (
        pads,
        pscad.silk(m.silk) + pscad.square((D("11.3"), D("2.6")), center=True)
    )

    tick = pscad.line((0, D("0.5")), center=True)
    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
        pscad.down(D("1.3")) + pscad.row(tick, D("1.5"), 5, center=True)
    )

    return all, silk



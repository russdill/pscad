# module shl.py
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

    pad1 = pscad.rounded_square([D("0.6"), D("1.25")], m.round_off, center=True)
    pad1_row = pscad.pad(itertools.count(1), m.clearance, m.mask) + (
        pscad.row(pad1, D("1.0"), m.n, center=True)
    )

    pad2 = pscad.rounded_square([D("0.9"), D("1.7")], m.round_off, center=True)
    pad2_row = pscad.pad(m.n + 1, m.clearance, m.mask) + (
        pscad.row(pad2, m.n + 1 + D("0.9"), 2, center=True)
    )

    pads = (
        pscad.up(D("3.35") + D("1.25") / 2) + pad1_row,
        pscad.up(D("1.7") / 2) + pad2_row
    )

    all = (
        pads,
        pscad.silk(m.silk) + pscad.up(D("1.45")) + pscad.square((m.n + D("2.8"), D("4.3")), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1)
    )

    return all, silk



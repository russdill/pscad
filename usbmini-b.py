# module usbmini-b.py
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
    'mask' :        "0.05",
    'silk' :        "0.2",
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.1"
}

def I(v):
    return D("25.4") * D(v)

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad_row = pscad.row(pscad.rounded_square(
        (D("0.5"), D("2.0")), m.round_off, center=True), D("0.8"), 5, center=True)

    gnd_row = pscad.row(pscad.donut(I("0.034"), I("0.045")), D("5.3"), 2)

    side = (
        pscad.pin("G", m.clearance, m.mask, square=True) + (
	    pscad.left(D("3.6")) + pscad.up(2) +
            pscad.rotate(-90) + gnd_row,
        ),

        pscad.hole(m.clearance, 0) + (
            pscad.left(D("1.7")) + pscad.down(D("1.3")) +
            pscad.circle(I("0.018"))
        ),

        pscad.silk(m.silk) + (
            pscad.left(D("3.6")) + pscad.up(D("4.6")) +
            pscad.polygon([(0, 0), (0, D("1.3")), (0, D("3.9")), (0, D("6.6"))],
                          [(0, 1), (2, 3)])
        )
    )

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            pscad.down(D("3.5")) + pad_row
        ),

        side + pscad.mirror([1, 0]) + side,

        pscad.silk(m.silk) + (
            pscad.up(D("4.6")) + pscad.line(D("7.2"), center=True),
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

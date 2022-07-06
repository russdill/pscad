# module usb-a-plug.py
#
# Copyright (C) 2016 Russ Dill <Russ.Dill@asu.edu>
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
    'clearance' :   "0.3048",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad = pscad.rounded_square((D("1.10"), D("2.50")), m.round_off, center=True)

    pad_row = (pscad.left(D("3.5")) + pad, pscad.left(1) + pad,
        pscad.right(1) + pad, pscad.right(D("3.5")) + pad)

    gnd_pin = pscad.donut(D("1.25"), D("1.80"))
    gnd_row = pscad.row(gnd_pin, D("11.40"), 2, center=True)

    hole = pscad.circle(D("0.55"))
    hole_row = pscad.row(hole, D("4.60"), 2, center=True)

    side = (
        pscad.silk(m.silk) + (
            pscad.line(D("12.05") / 2),
            pscad.right(D("12.05") / 2) + pscad.line((0, -D("14.70")))
        )
    )

    all = (
        pscad.pin("5", m.clearance, m.mask) + gnd_row,
        pscad.hole(m.clearance, 0) + hole_row,
        pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            pscad.up(D("2.75")) + pscad.mirror([1, 0]) + pad_row
        ),
        pscad.down(D("17.80")) + side + pscad.mirror([1, 0]) + side,
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

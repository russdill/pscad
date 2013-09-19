# module usb-a.py
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
    'clearance' :   "0.3048",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad = pscad.rounded_square((D("0.8"), D("2.82")), m.round_off, center=True)

    pad_row = (pscad.left(D("3.5")) + pad + pscad.right(D("2.5")) + pad +
        pscad.right(2) + pad + pscad.right(D("2.5")) + pad)

    gnd_pin = pscad.donut(D("1.15"), D("1.40"))

    side = (
        pscad.pin("5", m.clearance, m.mask, square=True) + (
            pscad.up(D("14.15") / 2 - D("10.3")) +
     	    pscad.left(D("13.14") / 2) + gnd_pin
        ),

        pscad.silk(m.silk) + (
            pscad.up(D("14.15") / 2) + pscad.line(D("13.90") / 2) +
            pscad.right(D("13.90") / 2) + pscad.line((0, D("10.30") - D("1.55")))
        )
    )

    all = (
        pscad.mirror([1, 0]) + pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            pscad.up(D("14.15") / 2 - D("10.3") - D("3.71")) + pad_row
        ),

        side + pscad.mirror([1, 0]) + side,
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

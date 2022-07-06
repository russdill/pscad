# module 112-yyy-113
#
# Copyright (C) 2015 Russ Dill <Russ.Dill@asu.edu>
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
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def I(v):
    return D("25.4") * D(v)

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    row = pscad.row(pscad.donut(I("0.035") / 2, I("0.030")),
            I("0.085"), m.pins / 2, center=True)

    A = I("1.21") + I("0.085") * (m.pins / 2 - 1)
    C = I("0.984")
    E = I("0.907") + I("0.085") * (m.pins / 2 - 1)

    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) + (
            pscad.up(I("0.1689") / 2) + row,
            pscad.down(I("0.1689") / 2) + row
        ),

	pscad.hole(m.clearance, 0) + (
            pscad.row(pscad.circle(I("0.126") / 2), E, 2, center=True)
        ),

        pscad.silk(m.silk) + (
            pscad.down(I("0.417") - (C - I("0.335")) / 2) +
                pscad.square((A, C - I("0.335")), center=True)
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

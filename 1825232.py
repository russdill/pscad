# module kk100
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
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.20",
    'drill_d1' :    "0.80",
    'drill_d2' :    "1.00",
    'annulus' :     "0.40",
    'pitch' :       "2.00",
    'body_x' :      "8.60",
    'body_y' :      "4.30",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    row1 = pscad.row(pscad.donut(m.drill_d1 / 2, m.drill_d1 / 2 + m.annulus),
        m.pitch, 3, center=True)

    row2 = pscad.row(pscad.donut(m.drill_d2 / 2, m.drill_d2 / 2 + m.annulus),
        m.pitch * 4, 2, center=True)

    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) +
        row1 + row2,

        pscad.silk(m.silk) +
        pscad.square((m.body_x, m.body_y), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1)
    )

    return all, silk


# module header.py
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

def I(v):
    return D("25.4") * D(v)

defaults = {
    'clearance' :   "0.15",
    'placement' :   "0.5",
    'grid'      :   "0.5",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",

    'pitch'     :   "2.54",
    'drill_d'   :   "1.00",
    'annulus'   :   "0.3",
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pin = pscad.donut(m.drill_d / 2, m.drill_d / 2 + m.annulus)
    all = pscad.pin(itertools.count(1), m.clearance, m.mask) + (
        pscad.left(m.pitch) + pin,
        pscad.up(m.pitch) + pin,
	pin,
	pscad.right(m.pitch) + pin,
	pscad.down(m.pitch) + pin
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, I("0.05"))
        #patterns.corners((3 * m.pitch, 3 * m.pitch), m.pitch / 4, center=True)
    )

    return all, silk


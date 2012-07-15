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

# http://www.molex.com/pdm_docs/sd/022232031_sd.pdf

defaults = {
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.20",
    'drill_d' :     "1.02",
    'annulus' :     "0.40",
    'pitch' :       "2.54",
    'body_y' :      "6.35",
    'placement' :   "0.25",
    'grid' :        "0.1"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    row = pscad.row(pscad.donut(m.drill_d / D(2), m.drill_d / D(2) + m.annulus),
        m.pitch, m.n, center=True)

    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) +
        row,

        pscad.silk(m.silk) +
        pscad.square((m.pitch * m.n, m.body_y), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
        
        pscad.up(m.body_y / D(2)) +
        pscad.left(m.pitch) +
        pscad.square((m.pitch * D(2), m.body_y / D(4)))
    )

    return all, silk


# module shrouded-header
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
    'silk' :        "0.2",
    'placement' :   "0.25",
    'grid' :        "0.1"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    row = pscad.row(pscad.donut(m.drill_d / D(2), m.drill_d / D(2) + m.annulus), m.pitch, m.n_x, center=True)

    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) + 
        pscad.rotate(270) +
        pscad.row(pscad.rotate(90) + row, m.pitch, m.n_y, center=True),

        pscad.silk(m.silk) + (
            pscad.square((m.body_x, m.body_y), center=True),
            pscad.square((m.body_x - m.thickness * D(2), m.body_y - m.thickness * D(2)), center=True),

            pscad.left((m.body_x - m.thickness) / D(2)) +
            pscad.square((m.thickness, m.key), center=True)
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, D("0.5")),
    )

    return all, silk

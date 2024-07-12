# module header-ra.py
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
import string

defaults = {
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    row = pscad.row(pscad.donut(m.drill_d / 2, m.drill_d / 2 + m.annulus), m.pitch_x, m.n_x, center=True)
    names = (i[0] + str(i[1]) for i in itertools.product(string.ascii_uppercase[:int(m.n_y)], range(1, int(m.n_x)+1)))
    all = pscad.pin(names, m.clearance, m.mask) + (
        pscad.rotate(270) + pscad.row(pscad.rotate(90) + row, m.pitch_y, m.n_y, center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.corners((m.body_x, m.body_y), m.pitch_x / 4, center=True)
    )

    return all, silk


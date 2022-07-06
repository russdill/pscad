# module dfn-3
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
import dmath

defaults = {
    'round_off' :   "0.2",
    'grid' :        "0.1",
    'placement' :   "0.25",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'pins' :        "1,2,3"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pin_names = (i for i in m.pins.split(','))
    pad1 = pscad.rounded_square((m.z - m.g1 - m.y, m.x), m.round_off, center=True)
    pad2 = pscad.rounded_square(((m.x - m.g2) / 2, m.y), m.round_off, center=True)

    all = pscad.pad(pin_names, m.clearance, m.mask) + (
        pscad.right(m.c / 2) + pad1,
        pscad.left(m.c / 2) + pscad.rotate(270) +
            pscad.row(pad2, (m.x - m.g2) / 2 + m.g2, 2, center=True)
    )

    courtyard = pscad.expand_to_grid(pscad.bound(all), m.placement, m.grid)
    courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])

    silk = pscad.silk(m.silk) + (
        pscad.translate(courtyard[0]) +
        patterns.brackets(courtyard_sz, m.x)
    )

    return all, silk

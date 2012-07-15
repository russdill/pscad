# module res_lvk
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
from decimal import Decimal as D
import itertools
import patterns

# http://www.ohmite.com/cat/res_lvk.pdf

defaults = {
    'round_off' :   "0.2",
    'grid' :        "0.1",
    'placement' :   "0.15",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    row = pscad.row(pscad.rounded_square([m.l, m.w], m.round_off, center=True), m.a + m.l, 2, center=True)
    all = pscad.pad(itertools.count(1), m.clearance, m.mask) + (
        pscad.rotate(270) +
        pscad.row(pscad.rotate(90) + row, m.b + m.w, 2, center=True)
    )

    courtyard = pscad.expand_to_grid(pscad.bound(all), m.placement, m.grid)
    courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])
    silk = pscad.silk(m.silk) + (
        pscad.translate(courtyard[0]) +
        patterns.brackets(courtyard_sz, m.l)
    )

    return all, silk

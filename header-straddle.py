# module pcie
#
# Copyright (C) 2022 Russ Dill <Russ.Dill@asu.edu>
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
    'pitch' :       "1.27",
    'pad_l' :       "2.80",
    'pad_w' :       "0.60",
    'n' :           40,
    'offset':       True
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    pad = pscad.square((m.pad_w, m.pad_l), center=True)
    row1 = pscad.row(pad, m.pitch, (m.n + 1) // 2, center=True)
    row2 = pscad.row(pad, m.pitch, m.n // 2, center=True)
    if not m.offset:
        row2 = pscad.left(m.pitch / 2) + row2
    all = (
	(pscad.pad(itertools.count(1, 2), m.clearance, m.mask) + row1),
	(pscad.pad(itertools.count(2, 2), m.clearance, m.mask) + pscad.back() + row2)
    )

    return pscad.nopaste() + all

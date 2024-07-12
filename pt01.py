# module 45558-0003.py
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
    'clearance' :   "0.30",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'placement' :   "0.25",
    'grid' :        "0.1"
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    row_1 = pscad.row(pscad.donut(D("1.0") / 2, D("1.0") / 2 + D("0.3")), D("2.5"), 3, center=True)
    row_2 = pscad.row(pscad.donut(D("2.2") / 2, D("2.2") / 2 + D("0.3")), D("10.0"), 2, center=True)
    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) + (
            pscad.down(D("3.3")) + row_1,
            row_2
        ),
        pscad.silk(m.silk) + (
            pscad.up(D("2.4") - D("9.2") / 2) +
            pscad.square((D("10.0"), D("9.2")), center=True)
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),    
    )

    return all, silk



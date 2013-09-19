# module pj-012a.py
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
    m = pscad.wrapper(defaults.items() + m.items())

    pin2 = pscad.donut(D("0.65"), D("0.85"))
    pin13 = pscad.donut(D("0.5"), D("0.7"))

    pins = pscad.down(D("11.5") / 2) + pscad.right(D("11.0") / 2) + pscad.left(D("4.5")) + (
        pscad.up(D("8.6")) + (
            pscad.left(D("3.8")) + pscad.pin("1", m.clearance, m.mask) + pin13,
            pscad.left(D("0.5")) + pscad.pin("3", m.clearance, m.mask) + pin13,
        ),
        pscad.up(D("9.0")) + (
            pscad.right(D("3.5")) + pscad.pin("2", m.clearance, m.mask) + pin2,
        ),
        pscad.up(D("1.5")) + (
            pscad.hole(m.clearance, 0) + pscad.circle(D("0.9"))
        ),
    )

    all = (
        pins,
        pscad.silk(m.silk) + pscad.square((D("11.0"), D("11.5")), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk



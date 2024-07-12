# module 54-00036
#
# Copyright (C) 2016 Russ Dill <Russ.Dill@asu.edu>
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
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    row = pscad.row(pscad.donut(D("1.5") / 2, D("2.1") / 2),
            D("2.5"), 3, center=False)

    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) + (
            pscad.right(D("0.25")) + row,
        ),

        pscad.silk(m.silk) + pscad.polygon([

            (-2,  2),
            ( 2,  2),
            ( 2,  D("2.5")),
            ( 6,  D("2.5")),
            ( 6,  -D("2.5")),
            ( 2,  -D("2.5")),
            ( 2,  -2),
            (-2,  -2)], [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)])
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

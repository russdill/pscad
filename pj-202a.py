# module pj-202a.py
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

    pin1 = pscad.donut(D("1.83"), D("2.43"))
    pin23 = pscad.donut(D("1.59"), D("2.19"))

    pins = pscad.up(D("14.4") / 2 - D("10.7")) + (
        pscad.left(D("4.7")) + pscad.pin("3", m.clearance, m.mask) + pin23,
        pscad.up(3) + pscad.pin("2", m.clearance, m.mask) + pin23,
        pscad.down(3) + pscad.pin("1", m.clearance, m.mask) + pin1,
    )

    all = (
        pins,
        pscad.silk(m.silk) + pscad.up(D("14.4") / 2) + pscad.left(D("9.0") / 2) + pscad.polygon([
            (0, 0),
            (0, D("10.7") - D("2.19") - D("0.2")),
            (0, D("10.7") + D("2.19") + D("0.2")),
            (0, D("14.4")),
            (D("4.5") - D("2.43") - D("0.2"), D("14.4")),
            (D("4.5") + D("2.43") + D("0.2"), D("14.4")),
            (D("9.0"), D("14.4")),
            (D("9.0"), 0)], [
            (0, 1), (2, 3), (3, 4), (5, 6), (6, 7), (7, 0)])
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk



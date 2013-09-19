# module dip.py
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

defaults = {
    'clearance' :   "0.2",
    'mask' :        "0.2",
    'silk' :        "0.4",
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pin_row = pscad.row(pscad.donut(m.drill_r, m.drill_r + m.annulus), m.pitch, m.n / 2, center=True)

    pins = pscad.pin(itertools.count(1), m.clearance, m.mask, square=True) + (
        pscad.down(m.width / 2) + pin_row,
        pscad.up(m.width / 2) + pscad.rotate(180) + pin_row
    )

    length = m.pitch * (m.n + 1) / 2
    silk = pscad.silk(m.silk) + (
        pscad.square([length, m.width - (m.drill_r + m.annulus) * 2 - m.silk * 4], center=True),
        pscad.left(length / 2) + pscad.rotate(270) + pscad.circle(m.width / D(10), sweep=180)
    )

    return pins, silk


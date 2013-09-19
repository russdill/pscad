# module beaglebone.py
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
    'clearance' :   "6 mil",
    'mask' :        "4 mil",
}

def I(v):
    return D("25.4") * D(v)

def header(m):
    def names(prefix):
        return (prefix + str(i) for i in itertools.count(1))

    row = pscad.row(pscad.donut(m.drill_d / D(2), m.drill_d / D(2) + m.annulus), m.pitch, m.n_x, center=True)
    all = pscad.pin(names(m.prefix), m.clearance, m.mask) + (
        pscad.rotate(270) + pscad.row(pscad.rotate(90) + row, m.pitch, m.n_y, center=True)
    )

    return (pscad.rotate(90) + all,)


def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    p_m = dict()

    p_m['n_x'] = 2
    p_m['n_y'] = 23
    p_m['prefix'] = "P8-"
    p_m['annulus'] = "0.3"
    p_m['drill_d'] = "40 mil"
    p_m['pitch'] = "0.1 in"
    p8 = header(pscad.wrapper(m.items() + p_m.items()))

    p_m['prefix'] = "P9-"
    p9 = header(pscad.wrapper(m.items() + p_m.items()))

    p_m['n_x'] = 1
    p_m['n_y'] = 6
    p_m['prefix'] = "J1-"
    j1 = header(pscad.wrapper(m.items() + p_m.items()))

    mhole = pscad.donut(I("0.125") / D(2), I("0.125") / D(2) + I("0.03125"))

    all = (
        pscad.left(I("3.4") / D(2) - I("0.775") - I("0.1") * D(11)) + (
            pscad.up(I("1.9") / D(2)) + p8,
            pscad.down(I("1.9") / D(2)) + p9 + pscad.up(I("0.175")) + pscad.right(I("0.050")) + j1
        ),
        pscad.pin(itertools.count(1), m.clearance, m.mask) + pscad.left(I("3.4") / D(2)) + pscad.down(I("2.15") / D(2)) + (
            pscad.right(I("3.175")) + (pscad.up(I("0.25")) + mhole, pscad.up(I("1.9")) + mhole),
            pscad.right(I("0.575")) + (pscad.up(I("0.125")) + mhole, pscad.up(I("2.025")) + mhole)
        )
    )

    return all

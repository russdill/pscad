# module ps2.py
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
    'clearance' :   "6 mil",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def I(v):
    return D("25.4") * D(v)

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    pin = pscad.donut(D("0.5"), D("0.75"))
    pad = pscad.rounded_square((D("3.0") + I("0.030"), I("0.030")), I("0.015"), center=True)

    pins = pscad.pin(itertools.count(1), m.clearance, m.mask) + (
        pscad.down(D("2.20")) + pscad.row(pin, D("2.0"), 2, center=True),
        pscad.down(D("0.12")) + pscad.row(pin, D("5.0"), 2, center=True),
        pscad.up(D("1.88")) + pscad.row(pin, D("4.0"), 2, center=True),
    ) + pscad.pad("6", m.clearance, m.mask) + (
        pscad.up(D("4.45")) + pad,
    )
    all = (
        pins,
        pscad.silk(D("0.3")) + pscad.circle(D("4.45")),
    )

    return all

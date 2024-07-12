# module spin
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
import dmath


defaults = {
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'n' :           "20",
    'width' :       "0.1",
    'radius' :      "1.0"
}

def pad(m):
    angle = 360 / m.n
    
    w = dmath.sin(dmath.radians(angle / 2)) * 2
    h = m.radius * dmath.cos(dmath.radians(angle / 2))
    piece = pscad.up(h) + pscad.square((w + m.width, m.width), rounded=True, center=True)
    ret = []
    for i in range(0, m.n):
        ret.append(pscad.rotate(i * 360 / m.n) + piece)
    return pscad.union() + tuple(ret)

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    all = pscad.pad(itertools.count(1), m.clearance, m.mask) + pad(m)

    return all

# module solder_jumper
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
    'round_off' :   "0.05",
    'grid' :        "0.10",
    'placement' :   "0.25",
    'clearance' :   "0.15",
    'mask' :        "0.2",
    'silk' :        "0.2",
    'space' :       "5 mil",
    'pad_w' :       "0.80",
    'pad_l' :       "0.95"
}

def mlp_pad(m):
    return pscad.union() + (
        pscad.down(m.pad_l / D(2) - m.round_off) +
        pscad.square((m.pad_w, m.round_off * D(2)), rounded=True, center=True),

        pscad.up((m.pad_l - m.pad_w) / D(2)) +
        pscad.circle(m.pad_w / D(2)) +
        pscad.left(m.pad_w / D(2)) +
        pscad.square((m.pad_w, m.pad_l - m.round_off - m.pad_w / D(2)))
    )

def closed(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad = pscad.left((m.pad_l + m.space) / D(2)) + pscad.rotate(90) + mlp_pad(m)
    all = pscad.pad(itertools.count(1), m.clearance, m.mask) + (
        pad, pscad.mirror([1, 0]) + pad
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, m.pad_w * D("0.6")),
    )

    return all, silk

def open(m):
    return pscad.nopaste() + closed(m)

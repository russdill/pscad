# module personality-chip
#
# Copyright (C) 2019 Russ Dill <Russ.Dill@asu.edu>
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

def I(v):
    return D("25.4") * D(v)

defaults = {
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'pitch' :       "100.0 mil"
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    outer_pad = pscad.square((I("0.060"), I("0.3")), center=True)
    pad = pscad.up(I("0.035") / 2) + pscad.square((I("0.060"), I("0.265")), center=True)
    key_pad = pscad.up(I("0.065") / 2) + pscad.square((I("0.060"), I("0.235")), center=True)

    mask_pad = pscad.down(I("0.030")) + pscad.square((I("0.060"), I("0.160")), center=True)
    mask_pads = (
        pscad.row(mask_pad, m.pitch, 7)
    )

    def names(l):
        return (l + str(i) for i in itertools.count(1))

    pads = (
        outer_pad,
        pscad.right(m.pitch) + pscad.row(pad, m.pitch, 2),
        pscad.right(m.pitch * 3) + key_pad,
        pscad.right(m.pitch * 4) + pscad.row(pad, m.pitch, 2),
        pscad.right(m.pitch * 6) + outer_pad
    )
    all = pscad.pad(names('B'), m.clearance, m.mask) + (
        pads,
    ), pscad.pad(names('A'), m.clearance, m.mask) + pscad.back() + (
        pads,
    ), (
        pscad.pad(names('B'), m.clearance, I("0.080")) + mask_pads,
        pscad.back() + pscad.pad(names('A'), m.clearance, I("0.080")) + mask_pads
    )

    return pscad.nopaste() + all

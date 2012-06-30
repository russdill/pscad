# module pcie
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
    'clearance' :   "0.15",
    'mask' :        "0.05",
    'pitch' :       "1.0"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad = pscad.square((D("0.70"), D("4.0")), center=True)
    key_pad = pscad.up(D("0.40")) + pscad.square((D("0.70"), D("3.20")), center=True)

    mask_dist = D("3.20") - D("2.40") + m.mask
    mask_pad = pscad.down(D("1.2") - mask_dist / D(2)) + pscad.square((D("0.70"), mask_dist), center=True)
    mask_pads = (
        pscad.row(mask_pad, m.pitch, 11),
        
        pscad.right(m.pitch * 10 + D("3.0")) +
        pscad.row(mask_pad, m.pitch, m.n + 1)
    )

    def names(l):
        return (l + str(i) for i in itertools.count(1))

    all = pscad.pad(names('B'), m.clearance, m.mask) + (
        pscad.row(pad, m.pitch, 11),

        pscad.right(m.pitch * 10 + D("3.0")) +
        pscad.row(pad, m.pitch, m.n - 1) +
        pscad.right(m.pitch * m.n - 1) + (
            key_pad,
            pscad.right(m.pitch) +
            pad
        )
    ), pscad.pad(names('A'), m.clearance, m.mask) + pscad.back() + (

        key_pad,
        pscad.right(m.pitch) +
        pscad.row(pad, m.pitch, 10),
        pscad.right(m.pitch * 10 + D("3.0")) +
        pscad.row(pad, m.pitch, m.n + 1)
    ), (
        pscad.pad(names('B'), m.clearance, D("2.40")) + mask_pads,
        pscad.back() + pscad.pad(names('A'), m.clearance, D("2.40")) + mask_pads
    )

    return pscad.nopaste() + all

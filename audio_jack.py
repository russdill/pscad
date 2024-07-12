# module 112-yyy-113
#
# Copyright (C) 2015 Russ Dill <Russ.Dill@asu.edu>
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

    large_pad = pscad.rounded_square((D("2.8"), D("2.8")), m.round_off, center=True)
    small_pad = pscad.rounded_square((D("2.2"), D("2.8")), m.round_off, center=True)

    pads = (
        pscad.down(D("5.1") - D("2.8") / 2) + (
             pscad.left(D("2.2") / 2) + small_pad,
             pscad.right(D("7.0") + D("2.8") / 2) + large_pad,
        ),
        pscad.up(D("5.1") - D("2.8") / 2) + pscad.right(D("0.9")) + small_pad,
        pscad.up(D("1.5") / 2) + pscad.right(D("12.7") + D("0.9") - D("2.8") / 2) + large_pad
    )

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + pads,
	pscad.hole(m.clearance, 0) + (
            pscad.row(pscad.circle(D("1.7") / 2), D("7.0"), 2, center=False)
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

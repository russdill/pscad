# module sc1489
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

    large_pad = pscad.rounded_square((D("2.9"), D("2.75")), m.round_off, center=True)
    small_pad = pscad.rounded_square((D("2.4"), D("2.55")), m.round_off, center=True)

    pads = (
        pscad.right(D("11.7")) + pscad.down(D("2.2") + D("2.75") / 2) + large_pad,
        pscad.right(D("4.3")) + pscad.up(D("2.4") + D("2.55") / 2) + small_pad,
        pscad.right(D("2.4")) + pscad.down(D("2.4") + D("2.55") / 2) + small_pad
    )

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + pads,
	pscad.hole(m.clearance, 0) + (
            pscad.right(D("3.5")) + pscad.row(pscad.circle(D("1.6") / 2), D("7.0"), 2, center=False)
        ),
        pscad.silk(m.silk) + pscad.polygon([

            (0,          D("3.0")),
            (D("14.5"),  D("3.0")),
            (D("14.5"), -D("3.0")),
            (0,         -D("3.0")),
            (0,         -D("2.5")),
            (-D("2.5"), -D("2.5")),
            (-D("2.5"),  D("2.5")),
            (0,          D("2.5"))], [
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)])
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

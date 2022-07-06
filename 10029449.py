# module hdmi
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
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'paste_fraction': "0.70",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad = pscad.rounded_square((D("0.3"), D("2.3")), m.round_off, center=True)
    pad_row = pscad.rotate(180) + pscad.row(pscad.paste_fraction(pad, (1, m.paste_fraction)), D("0.5"), 19, center=True)

    shield = pscad.donut(D("1.30") / 2, D("2.0") / 2)
    shield_row1 = pscad.row(shield, D("14.5"), 2, center=True)
    shield_row2 = pscad.row(shield, D("15.7"), 2, center=True)

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            pscad.right(D("0.25")) + pscad.up(D("7.55") + D("2.3") / 2) + pad_row
        ),
        pscad.pin("20", m.clearance, m.mask) + (
            pscad.up(D("7.5")) + shield_row1 +
            pscad.down(D("4.9")) + shield_row2
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

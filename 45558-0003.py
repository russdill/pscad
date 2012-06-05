# module 45558-0003.py
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


# http://www.molex.com/pdm_docs/sd/455580003_sd.pdf
defaults = {
    'clearance' :   "0.30",
    'mask' :        "0.05",
    'silk' :        "0.2",
    'placement' :   "0.25",
    'grid' :        "0.1"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    row = pscad.row(pscad.donut(D("1.8") / D(2), D("1.8") / D(2) + D("0.5")), D("4.2"), 3)
    all = (
        pscad.pin(itertools.count(1), m.clearance, m.mask) + (
            row,
            pscad.down(D("4.2")) + row
        ),
        pscad.hole(m.clearance, 0) + (
            pscad.up(D("7.30")) +
            pscad.row(pscad.circle(D("3.0") / D(2)), D("8.4"), 2)
        ),
        pscad.silk(m.silk) + (
            pscad.right(D("4.2")) +
            pscad.up(D("7.3") + D("6.6") - D("12.8") / D("2")) +
            pscad.square((D("13.8"), D("12.8")), center=True)
        )
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
        
        pscad.right(D("4.2") - D("4") / D(2)) +
        pscad.up(D("7.3") + D("6.6")) +
        pscad.square((D("4"), D("3.5")))
    )

    return all, silk



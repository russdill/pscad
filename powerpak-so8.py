# module powerpak-so8
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
    "round_off" :   "0.1",
    "clearance" :   "0.2",
    "mask" :        "2.5 mil",
    "silk" :        "0.2",
    "placement" :   "0.25",
    "grid" :        "0.1"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pitch = D("1.27")
    width = D("6.61")
    pad_size0 = [D("0.61"), D("1.27")]
    pad_size1 = [D("0.61"), D("1.02")]
    pad_size2 = [D("1.65"), D("3.81")]
    body = [D("5.0"), D("6.25")]

    thermal_pad = pscad.paste_fraction(pscad.rounded_square(pad_size2, m.round_off, center=True), D("0.5"))

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) +
        pscad.down((width - pad_size0[1]) / D(2)) +
        pscad.row(pscad.rounded_square(pad_size0, m.round_off, center=True), pitch, 4, center=True),

        pscad.pad((i for i in [6, 6, 5, 5]), m.clearance, m.mask) +
        pscad.up((width - pad_size1[1]) / D(2)) +
        pscad.row(pscad.rounded_square(pad_size1, m.round_off, center=True), pitch, 4, center=True),

        pscad.pad((i for i in [6, 5]), m.clearance, m.mask) +
        pscad.down(width / D(2)) +
        pscad.up(pad_size0[1] + D("0.82") + pad_size2[1] / D(2)) +
        pscad.row(thermal_pad, D("0.61") + pad_size2[0], 2, center=True),

        pscad.silk(m.silk) + patterns.brackets(body, D("0.2"), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, D("0.5")),

        pscad.down(width / D(2) + m.silk) +
        pscad.left(pitch * D("1.5")) +
        pscad.line(pad_size0[0], center=True)
    )

    return all, silk


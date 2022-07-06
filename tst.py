# module mlp
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
from decimal import Decimal as D
import dmath
import itertools
import patterns

# http://www.fairchildsemi.com/an/AN/AN-5067.pdf

defaults = {
    'rounding' :    "0.05",
    'quad'      :   "False",
    'placement' :   "0.25",
    'grid'      :   "0.5",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'start_pin' :   "1"
}

def mlp_pad(m):
    pad = pscad.union() + (
        pscad.down(m.pad_l / 2 - m.rounding) +
        pscad.square((m.pad_w, m.rounding * 2), rounded=True, center=True),

        pscad.up((m.pad_l - m.pad_w) / 2) +
        pscad.circle(m.pad_w / 2) +
        pscad.left(m.pad_w / 2) +
        pscad.square((m.pad_w, m.pad_l - m.rounding - m.pad_w / 2))
    )
    if 'pad_paste_fraction' in m:
        return pscad.paste_fraction(pad, m.pad_paste_fraction)
    else:
        return pad

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pads = []
    for i in range(0, m.n):
        pads.append(pscad.rotate(i * 360 / m.n) + pscad.down(m.height / 2) + mlp_pad(m))
    pads = tuple(pads)

    pin_list = range(m.start_pin, m.n - m.start_pin + 3) + range(1, m.start_pin) + [int(m.n) + 1]
    all = pscad.pad(itertools.cycle(pin_list), m.clearance, m.mask) + (
        pads,
    ), pscad.silk(m.silk) + patterns.corners((m.body_x, m.body_y), m.pad_l, center=True)

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, m.pad_w * 2),

        pscad.translate([-m.body_x / 2, m.body_y / 2]) +
        pscad.down(m.silk * 2) +
        pscad.line(m.pad_l * D("0.7"))
    )

    return all, silk

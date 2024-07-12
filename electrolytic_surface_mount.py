# module electrolytic_surface_mount
#
# Copyright (C) 2021 Russ Dill <Russ.Dill@asu.edu>
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
    'round_off' :   "0.2",
    'grid' :        "0.1",
    'placement' :   "0.50",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'pins' :        "P,N",
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    pin_names = (i for i in m.pins.split(','))
    pad = pscad.rounded_square((m.pad_w, m.pad_l), m.round_off, center=True)

    all = pscad.pad(pin_names, m.clearance, m.mask) + (
        pscad.row(pad, m.pitch, 2, center=True)
    )

    points = [
            (-m.body_x / 2, m.body_y / 2 - m.corner),
            (-(m.body_x / 2 - m.corner), m.body_y / 2),
            (m.body_x / 2, m.body_y / 2),
            (m.body_x / 2, -m.body_y / 2),
            (-(m.body_x / 2 - m.corner), -m.body_y / 2),
            (-m.body_x / 2, -(m.body_y /2 - m.corner)),
    ]
    body_lines = pscad.polygon(points)

    silk = pscad.silk(m.silk) + (
        body_lines,
        patterns.placement_courtyard(all, m.placement, m.grid, 0.50),
        patterns.placement_courtyard(body_lines, m.placement, m.grid, 1)
    )

    return all, silk

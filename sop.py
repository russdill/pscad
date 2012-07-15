# module sop
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
    'round_off' :   "0.05",
    'placement' :   "0.25",
    'grid'      :   "0.1",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'paste_fraction': "0.8",
    'paste_max':    "1.0"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    try:
        pin_count = m.n
        pin_names = itertools.count(1)
    except:
        pin_count = len(m.pins.split(','))
        pin_names = (i for i in m.pins.split(','))

    try:
        body_y = m.body_y
    except:
        body_y = m.width - m.pad_l - m.silk * D(3)

    pad_row = pscad.row(pscad.rounded_square(
        (m.pad_w, m.pad_l), m.round_off, center=True), m.pitch, pin_count / 2, center=True)

    if body_y > m.width - m.pad_l - m.silk * D(2):
        edge = m.body_x / D(2) - m.pitch * pin_count / 4
        body = patterns.brackets([m.body_x, body_y], edge, center=True)
    else:
        body = pscad.square([m.body_x, body_y], center=True)

    all = pscad.pad(pin_names, m.clearance, m.mask) + (
        pscad.down(m.width / D(2)) + pad_row,
        pscad.up(m.width / D(2)) + pscad.rotate(180) + pad_row
    ), pscad.silk(m.silk) + body
        
    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, m.pad_w * D(2)),

        pscad.down(m.width / D(2)) +
        pscad.left(m.silk + m.pitch * pin_count / 4) +
        pscad.line([0, m.pad_l * D("0.7")], center=True)
    )

    return all, silk

def with_thermal_pad(m):
    m = pscad.wrapper(defaults.items() + m.items())

    try:
        thermal_name = m.pins.split(',')[-1]
    except:
        thermal_name = m.n + 1

    thermal_size = (m.thermal_x, m.thermal_y)

    return part(m), pscad.pad(thermal_name, m.clearance, m.mask) + (
        patterns.thermal_pad(pscad.square(thermal_size, center=True),
                thermal_size, m.paste_fraction, m.paste_max)
    )

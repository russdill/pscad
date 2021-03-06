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
    'grid'      :   "0.5",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'paste_fraction': "0.35",
    'paste_max':    "1.0",
    'pad_paste_fraction': "1.0",
    'quad' :        False
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    try:
        pin_count = m.n
        pin_names = itertools.count(1)
    except:
        pin_count = len(m.pins.split(','))
        pin_names = (i for i in m.pins.split(','))

    if 'pads_x' in m:
        pads_x = m.pads_x
    elif m.quad:
        pads_x = pin_count / 4
    else:
        pads_x = 0
    pads_y = pin_count / 2 - pads_x

    try:
        body_y = m.body_y
    except:
        body_y = m.width - m.pad_l - m.silk * 3

    if 'height' in m:
        height = m.height
    else:
        height = m.width

    pad = pscad.rounded_square((m.pad_w, m.pad_l), m.round_off, center=True)

    row_y = pscad.down(m.width / 2) + pscad.row(
        pscad.paste_fraction(pad, (1,m.pad_paste_fraction)),
        m.pitch, pads_y, center=True)

    if m.quad:
        row_x = pscad.down(height / 2) + pscad.row(
            pscad.paste_fraction(pad, (1,m.pad_paste_fraction)),
            m.pitch, pads_x, center=True)
        pads = pscad.pad(pin_names, m.clearance, m.mask) + (
            row_y, pscad.rotate(90) + row_x,
            pscad.rotate(180) + row_y, pscad.rotate(270) + row_x
        )
    else:
        pads = pscad.pad(pin_names, m.clearance, m.mask) + (
            row_y, pscad.rotate(180) + row_y
        )

    try:
        if m.quad:
            raise Exception()
        if body_y > m.width - m.pad_l - m.silk * 2:
            edge = m.body_x / 2 - m.pitch * D(pin_count) / 4
            body = patterns.brackets([m.body_x, body_y], edge, center=True)
        else:
            body = pscad.square([m.body_x, body_y], center=True)
        all = pads, pscad.silk(m.silk) + body
    except:
        all = pads

    try:
        corners = m.corners
    except:
        corners = m.pad_w * 2

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, corners),

        pscad.down(m.width / 2) +
        pscad.left(m.silk + m.pitch * pads_y / 2) +
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

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
    'grid'      :   "0.1",
    'clearance' :   "0.15",
    'mask' :        "0.05",
    'silk' :        "0.2"
}

def indent_pad(size, indent):
    return pscad.union() + (
        pscad.translate([-size[0] / D(2), -size[1] / D(2)]) + (
            pscad.square([size[0], size[1] - indent]),

            pscad.right(indent) +
            pscad.square([size[0] - indent, size[1]]),
            
            pscad.down(size[1] - indent) +
            pscad.rotate(45) + pscad.square(indent * dmath.sqrt(D(2)))
        )
    )

def thermal_pad(pad, size, paste_fraction, max_paste_size):
    paste_x = size[0] * dmath.sqrt(paste_fraction)
    paste_y = size[1] * dmath.sqrt(paste_fraction)
    n_x = dmath.ceil(paste_x / max_paste_size)
    n_y = dmath.ceil(paste_y / max_paste_size)

    paste_pad = pscad.rounded_square([paste_y / n_y, paste_x / n_x], D("0.05"), center=True)
    return pscad.union() + (
        pscad.row(pscad.rotate(90) + pscad.row(paste_pad, size[1] / n_y, n_y, center=True),
            size[0] / n_x, n_x, center=True),
        pscad.nopaste() + pad
    )

def mlp_pad(m):
    pad = pscad.union() + (
        pscad.down(m.pad_l / D(2) - m.rounding) +
        pscad.square((m.pad_w, m.rounding * D(2)), rounded=True, center=True),

        pscad.up((m.pad_l - m.pad_w) / D(2)) +
        pscad.circle(m.pad_w / D(2)) +
        pscad.left(m.pad_w / D(2)) +
        pscad.square((m.pad_w, m.pad_l - m.rounding - m.pad_w / D(2)))
    )
    if 'pad_paste_fraction' in m:
        return pscad.paste_fraction(pad, m.pad_paste_fraction)
    else:
        return pad

def mlp_row(m, n):
    return pscad.down(m.width / D(2)) + pscad.row(mlp_pad(m), m.pitch, n, center=True)

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    thermal_size = (m.thermal_x, m.thermal_y)
    row = mlp_row(m, m.n / (4 if m.quad else 2))

    if m.quad:
        pads = (
            row, pscad.rotate(90) + row,
            pscad.rotate(180) + row, pscad.rotate(270) + row
        )
    else:
        pads = row, pscad.rotate(180) + row

    all = pscad.pad(itertools.count(1), m.clearance, m.mask) + (
        pads,
        thermal_pad(indent_pad(thermal_size, m.indent),
                thermal_size, m.paste_fraction, m.paste_max)
    ), pscad.silk(m.silk) + patterns.corners((m.body_x, m.body_y), m.pad_l, center=True)

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, m.pad_w * D(2)),

        pscad.translate([-m.body_x / D(2), m.body_y / D(2)]) +
        pscad.down(m.silk * D(2)) +
        pscad.line(m.pad_l * D("0.7"))
    )

    return all, silk

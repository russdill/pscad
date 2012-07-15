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
    'silk' :        "0.2"
}

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
        patterns.thermal_pad(patterns.indent_pad(thermal_size, m.indent),
                thermal_size, m.paste_fraction, m.paste_max)
    ), pscad.silk(m.silk) + patterns.corners((m.body_x, m.body_y), m.pad_l, center=True)

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, m.pad_w * D(2)),

        pscad.translate([-m.body_x / D(2), m.body_y / D(2)]) +
        pscad.down(m.silk * D(2)) +
        pscad.line(m.pad_l * D("0.7"))
    )

    return all, silk

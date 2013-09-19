# module chip_component
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
import dmath

defaults = {
    'round_off' :   "0.2",
    'grid' :        "0.1",
    'placement' :   "0.25",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'polarized' :   "False",
    'pins' :        "1,2,3",
    'tri' :         "False"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pin_names = (i for i in m.pins.split(','))
    pad = pscad.rounded_square((m.pad_w, m.pad_l), m.round_off, center=True)

    if m.tri:
        tri = pscad.right(m.pitch) + pscad.nopaste() + pad
    else:
        tri = None

    all = pscad.pad(pin_names, m.clearance, m.mask) + (
        pscad.left(m.pitch if m.tri else 0) + pscad.row(pad, m.pitch, 2, center=not m.tri), tri
    )

    if 'body_y' in m:
        body_lines = pscad.rotate(90) + pscad.row(pscad.rotate(90) + pscad.line(m.pitch, center=True), m.body_y, 2, center=True)
    else:
        body_lines = pscad.empty()

    courtyard = pscad.expand_to_grid(pscad.bound((all, body_lines)), m.placement, m.grid)
    courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])

    if m.polarized:
        mark = (
            pscad.right(courtyard[0][0]) +
            pscad.rotate(90) +
            pscad.circle(courtyard_sz[1] / D(6), sweep=180)
        )
    else:
        mark = pscad.empty()

    silk = pscad.silk(m.silk) + (
        pscad.translate(courtyard[0]) +
        patterns.brackets(courtyard_sz, m.pad_w),
        mark,
        body_lines
    )

    return all, silk

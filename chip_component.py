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
    'offset' :      "0",
    'tri' :         "False"
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    pin_names = (i for i in m.pins.split(','))
    pad = pscad.rounded_square((m.pad_w, m.pad_l), m.round_off, center=True)

    if m.tri:
        tri = pscad.right(m.pitch) + pscad.down(m.offset) + pscad.nopaste() + pad
    else:
        tri = None

    all = pscad.pad(pin_names, m.clearance, m.mask) + (
        pscad.left(m.pitch if m.tri else m.pitch / 2) + (pscad.up(m.offset) + pad,) +
        pscad.right(m.pitch) + (pscad.down(0 if m.tri else m.offset) + pad,),
	tri
    )

    if 'body_y' in m:
        body_lines = pscad.rotate(90) + pscad.row(pscad.rotate(90) + pscad.line(m.pitch, center=True), m.body_y, 2, center=True)
    else:
        body_lines = pscad.empty()

    if m.polarized:
        mc = pscad.expand_to_grid(pscad.bound((all, body_lines)), max(D("0.20"), m.placement), m.grid)
        mark = (
            pscad.left(mc[0][0]) +
            pscad.rotate(270) +
            pscad.circle((mc[1][1] - mc[0][1]) / D(6), sweep=180)
        )
    else:
        mark = pscad.empty()

    sep = pscad.rotate(90) + pscad.line(m.pad_l, center=True),
    if m.tri:
        sep = pscad.row(sep, m.pitch, 2, center=True)

    silk = pscad.silk(m.silk) + (sep, mark, body_lines)
    if m.placement != 0:
        courtyard = pscad.expand_to_grid(pscad.bound((all, body_lines)), max(0.25, m.placement), m.grid)
        courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])
        silk += pscad.translate(courtyard[0]) + patterns.corners(courtyard_sz, m.pad_w)
    # Placement courtyard
    #) + pscad.silk(0.001) + (
    #    pscad.translate(courtyard[0]) + patterns.corners(courtyard_sz, m.pad_w)
    #)


    return all, silk

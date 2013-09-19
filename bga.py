# module bga
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
from string import ascii_uppercase
import itertools
import re
import patterns

defaults = {
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'no_letter' :   "IOQSYZ",
    'placement' :   "1",
    'grid' :        "0.1",
    'invert' :      "False",
    'paste_fraction' : "0.80"
}

def bga_letters(skip):
    return itertools.ifilterfalse(lambda x: x in skip, ascii_uppercase)

def bga_dletters(skip):
    return (i[0] + i[1] for i in itertools.product([''] + list(bga_letters(skip)), bga_letters(skip)))

def bga_names(n, skip):
    return (i[0] + str(i[1]) for i in itertools.product(bga_dletters(skip), range(1, n+1)))

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    if 'skip' in m:
        skip = lambda name: re.match(m.skip, name)
    else:
        skip = None

    bga_pad = pscad.paste_fraction(pscad.circle(m.pad_size / 2), m.paste_fraction)
    row = pscad.row(bga_pad, m.pitch, m.n_x, center=True)
    all = (
        pscad.pad(bga_names(m.n_x, m.no_letter), m.clearance, m.mask, skip=skip) +
        pscad.rotate(270) + pscad.row(pscad.rotate(90) + row, m.pitch, m.n_y, center=True),

        pscad.silk(m.silk) + pscad.square((m.body_x, m.body_y), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),

        pscad.translate([-m.body_x / 2, -m.pitch * (m.n_y - 1) / 2]) +
        pscad.left(m.silk * 2) + pscad.line([0, m.pitch * 2], center=True)
    )

    if m.invert:
        return pscad.mirror([1, 0]) + pscad.rotate(270) + (all, silk)

    return all, silk

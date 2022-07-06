# module 10118194-0001lf.py
#
# Copyright (C) 2014 Russ Dill <Russ.Dill@asu.edu>
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
    'clearance' :   "0.30",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'round_off' :   "0.1",
    'placement' :   "0.25",
    'grid' :        "0.5"
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    pad_row = pscad.row(pscad.rounded_square(
        (D("0.4"), D("1.35")), m.round_off, center=True), D("0.65"), 5, center=True)

    gnd_row1 = pscad.row(pscad.donut(D("0.85") / 2, D("1.25") / 2), 5, 2, center=True)
    gnd_row2 = pscad.row(pscad.donut(D("1.15")/ 2, D("1.55") / 2), 7, 2, center=True)
    gnd_pads1 = pscad.row(pscad.rounded_square(
    	(D("1.5"), D("1.55")), m.round_off, center=True), 2, 2, center=True)
    gnd_pads2 = pscad.row(pscad.rounded_square(
    	(D("1.2"), D("1.55")), m.round_off, center=True), D("5.8"), 2, center=True)


    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            pscad.up(D("2.7")) + pad_row
        ),

        pscad.pin("G", m.clearance, m.mask) + pscad.left(D("0.5")) + (
			gnd_row2,
			pscad.up(D("2.70")) + gnd_row1
        ),

        pscad.pad("G", m.clearance, m.mask) + (
        	gnd_pads1, gnd_pads2
        ),

        pscad.silk(m.silk) + (
            pscad.down(D("1.45")) + pscad.line(D("7.89"), center=True),
        )
    )

    return all

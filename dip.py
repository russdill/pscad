#!/usr/bin/env python
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

def dip(name, drill_r, clearance, annulus, mask, pitch, n, width, silk_width):

    pin_row = pscad.row(pscad.circle(drill_r), pitch, n / 2, center=True)

    pins = pscad.pin(itertools.count(1), annulus, clearance, mask, square=True) & (
        pscad.down(width / D(2)) & pin_row |
        pscad.up(width / D(2)) & pscad.rotate(180) & pin_row
    )

    length = pitch * (n + 1) / D(2)
    silk = pscad.silk(w=silk_width) & (
        pscad.square([length, width - (drill_r + annulus) * D(2) - silk_width * D(4)], center=True) |
        pscad.left(length / D(2)) & pscad.rotate(270) & pscad.circle(width / D(10), sweep=180)
    )

    pscad.element(pins | silk, name)

if __name__ == "__main__":
    dip("DIP-32",
        drill_r = D("0.5"), clearance = D("0.2"), mask = D("0.2"), annulus = D("0.5"),
        pitch = D("2.54"), n = 32, width = D(20), silk_width = D("0.4"))

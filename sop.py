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

def sop(name, pad_size, pad_r, clearance, mask, pitch, n, width, silk_width):

    pad_row = pscad.row(pscad.rounded_square(pad_size, pad_r, center=True), pitch, n / 2, center=True)

    pads = pscad.pad(itertools.count(1), clearance,  mask) & (
        pscad.down(width / D(2)) & pad_row |
        pscad.up(width / D(2)) & pscad.rotate(180) & pad_row
    )

    length = pitch * (n + 1) / D(2)
    silk = pscad.silk(w=silk_width) & (
        pscad.square([length, width - pad_size[1] - silk_width * D(4)], center=True) |
        pscad.left(length / D(2)) & pscad.rotate(270) & pscad.circle(width / D(10), sweep=180)
    )

    pscad.element(pads | silk, name)

if __name__ == "__main__":
    sop("TSOP-32",
        pad_size = [D(1), D(4)], pad_r = D("0.2"),
        clearance = D("0.2"), mask = D("0.2"),
        pitch = D(2), n = 32, width = D(20), silk_width = D("0.4"))

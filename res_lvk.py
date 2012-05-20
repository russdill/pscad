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
from decimal import Decimal as D
import itertools

# http://www.ohmite.com/cat/res_lvk.pdf

def res_lvk(name, L, W, A, B, round_off, clearance=D("0.15"), mask=D("0.05"), silk=D("0.2")):

    courtyard = (L * D("2") + A + D("0.6"), W * D("2") + B + D("0.6"))

    row = pscad.row(pscad.rounded_square([L, W], round_off, center=True), A + L, 2, center=True)
    pads = pscad.pad(itertools.count(1), clearance, mask) & (
        pscad.rotate(270) &
        pscad.row(pscad.rotate(90) & row, B + W, 2, center=True)
    )

    bracket = pscad.translate([courtyard[0] / D(2), courtyard[1] / D(2)]) & (
        pscad.line([-L / D(2), 0]) |
        pscad.line([0, -courtyard[1]]) |
        pscad.up(courtyard[1]) & pscad.line([-L / D(2), 0])
    )

    silk_lines = bracket | pscad.mirror([1, 0]) & bracket
    pscad.element(pads | pscad.silk(w=silk) & silk_lines, name)


if __name__ == "__main__":
    # 1204
    res_lvk("LVK12", L=D("1.75"), W=D("1.10"), A=D("1.00"), B=D("0.30"), round_off=D("0.2"))
    # 2010
    #res_lvk("LVK20", L=D("2.55"), W=D("1.55"), A=D("1.40"), B=D("0.50"), round_off=D("0.2"))
    # 2412
    #res_lvk("LVK24", L=D("3.25"), W=D("1.90"), A=D("2.00"), B=D("0.60"), round_off=D("0.2"))
    # 1224
    #res_lvk("LVK25", L=D("1.40"), W=D("3.30"), A=D("2.20"), B=D("1.00"), round_off=D("0.2"))


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

def chip_component(name, pad_size, pitch, round_off, courtyard, clearance, mask, silk, polarized=False, pins=(1, 2)):

    pads = (
        pscad.pad(itertools.count(1), clearance, mask) &
        pscad.row(pscad.rounded_square(pad_size, round_off, center = True), pitch, 2, center = True)
    )

    bracket = pscad.translate([courtyard[0] / D(2), courtyard[1] / D(2)]) & (
        pscad.line([-pad_size[0] / D(2), 0]) |
        pscad.line([0, -courtyard[1]]) |
        pscad.up(courtyard[1]) & pscad.line([-pad_size[0] / D(2), 0])
    )

    silk_lines = bracket | pscad.mirror([1, 0]) & bracket
    if polarized:
        silk_lines |= pscad.left(courtyard[0] / D(2)) & pscad.rotate(90) & pscad.circle(courtyard[1] / D(6), sweep=180)

    pscad.element(pads | pscad.silk(w=silk) & silk_lines, name)

if __name__ == "__main__":
    #chip_component("EIA0402", (D("0.65"), D("0.6")), D("1.0"), D("0.15"), (D("1.9"), D("1.0")), D("0.15"), D("0.2"), D("0.2"), polarized=True)

    chip_component("EIA0603", (D("0.8"), D("0.95")), D("1.6"), D("0.2"), (D("3.0"), D("1.5")), D("0.15"), D("0.2"), D("0.2"), polarized=True)
    #chip_component("EIA0201", (D("0.35"), D("0.3")), D("0.6"), D("0.05"), (D("1.2"), D("0.6")), D("0.15"), D("0.2"), D("0.2"), polarized=True)
    #chip_component("EIA6032", (D("2.3"), D("2.25")), D("5.0"), D("0.25"), (D("7.8"), D("3.9")), D("0.15"), D("0.2"), D("0.2"), polarized=True)

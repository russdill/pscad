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

def I(v):
    return D("25.4") * D(v)

def ptd08a0x0w_pins(m, clearance, mask):
    pwr_pin = pscad.circle(I("0.055") / D(2))
    return pscad.pin(itertools.count(1), D("0.5"), clearance, mask) & (
        pwr_pin |
        pscad.down(m['A']) & pwr_pin &
        pscad.right(m['B']) & pwr_pin &
        pscad.right(m['C']) & pwr_pin
    )

def common_pins(clearance, mask):
    sig_pin = pscad.circle(I("0.028") / D(2))
    return pscad.pin(itertools.count(5), D("0.18"), clearance, mask) & (
        pscad.down(I("0.350")) &
        pscad.rotate(90) &
        pscad.row(sig_pin, I("0.050"), 8)
    )

M10W = {
    'name' : "PTD08A010W",
    'A' : I("0.500"),
    'B' : I("0.275"),
    'C' : I("0.350"),
    'D' : I("0.625"),
    'E' : I("0.785"),
    'F' : I("0.660")
}

M20W = {
    'name' : "PTD08A020W",
    'A' : I("0.625"),
    'B' : I("0.375"),
    'C' : I("0.500"),
    'D' : I("0.875"),
    'E' : I("1.035"),
    'F' : I("0.785")
}

def ptd08a0x0w_template(m):
    clearance = D("0.2")
    mask = D("0.2")
    silk_w = D("0.2")

    pins = ptd08a0x0w_pins(m, clearance, mask)
    pins |= (pscad.right(m['D']) & common_pins(clearance, mask))
    silk = pscad.silk(silk_w) & (
        pscad.translate([m['D'] / D(2), m['A'] / D(2)]) &
        pscad.square([m['E'], m['F']], center=True)
    )
    pscad.element(pins | silk, m['name'])

def ptd08a010w():
    ptd08a0x0w_template(M10W)

def ptd08a020w():
    ptd08a0x0w_template(M20W)

def ptd08a0x0w():
    clearance = D("0.2")
    mask = D("0.2")
    silk_w = D("0.2")

    pins = ptd08a0x0w_pins(M20W, clearance, mask)
    pins |= (pscad.right(M20W['D']) | common_pins(clearance, mask))
    pins |= (pscad.right(M20W['D'] - M10W['D']) & ptd08a0x0w_pins(M10W, clearance, mask))
    silk = pscad.silk(silk_w) & (
        pscad.translate([M20W['D'] / D(2), M20W['A'] / D(2)]) &
        pscad.square([M20W['E'], M20W['F']], center=True)
    )
    pscad.element(pins | silk, "PTD08A0X0W")


if __name__ == "__main__":
    ptd08a010w()

# module ptd08a0x0w
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

def I(v):
    return D("25.4") * D(v)

defaults = {
    'clearance' :   "0.2",
    'mask' :        "2.5 mil",
    'silk' :        "0.2",
    'placement':    "0.25",
    'grid' :        "0.5"
}

M10W_defaults = {
    'a' :           '0.500"',
    'b' :           '0.275"',
    'c' :           '0.350"',
    'd' :           '0.625"',
    'e' :           '0.785"',
    'f' :           '0.660"'
}

M20W_defaults = {
    'a' :           '0.625"',
    'b' :           '0.375"',
    'c' :           '0.500"',
    'd' :           '0.875"',
    'e' :           '1.035"',
    'f' :           '0.785"'
}

def ptd08a0x0w_pins(m):
    pwr_pin = pscad.donut(I("0.055") / 2, I("0.055") / 2 + D("0.5"))
    return pscad.pin(itertools.count(1), m.clearance, m.mask) + (
        pwr_pin,
        pscad.down(m.a) + pwr_pin +
        pscad.right(m.b) + pwr_pin +
        pscad.right(m.c) + pwr_pin
    )

def common_pins(m):
    sig_pin = pscad.donut(I("0.028") / 2, I("0.028") / 2 + D("0.18"))
    return pscad.pin(itertools.count(5), m.clearance, m.mask) + (
        pscad.down(I("0.350")) +
        pscad.rotate(90) +
        pscad.row(sig_pin, I("0.050"), 8)
    )

def ptd08a0x0w_template(m):
    all = (
        ptd08a0x0w_pins(m),

        pscad.right(m.d) +
        common_pins(m),

        pscad.silk(m.silk) +
        pscad.translate([m.d / 2, m.a / 2]) +
        pscad.square([m.e, m.f], center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

def ptd08a010w(m):
    m = pscad.wrapper(defaults.items() + M10W_defaults.items() + m.items())
    return ptd08a0x0w_template(m)

def ptd08a020w(m):
    m = pscad.wrapper(defaults.items() + M20W_defaults.items() + m.items())
    return ptd08a0x0w_template(m)

def ptd08a0x0w(m):
    m = pscad.wrapper(defaults.items() + m.items())
    m10w = pscad.wrapper(defaults.items() + M10W_defaults.items() + m.items())
    m20w = pscad.wrapper(defaults.items() + M20W_defaults.items() + m.items())
    
    all = (
        ptd08a0x0w_pins(m20w),

        pscad.right(m20w.d - m10w.d) +
        ptd08a0x0w_pins(m10w),

        pscad.right(m20w.d) +
        common_pins(m),

        pscad.silk(m.silk) +
        pscad.translate([m20w.d / 2, m20w.a / 2]) +
        pscad.square([m20w.e, m20w.f], center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, 1),
    )

    return all, silk

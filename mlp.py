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
import dmath
import itertools
# http://www.fairchildsemi.com/an/AN/AN-5067.pdf

MLP16 = {
    'name' :        "MLP16",
    'pad_w' :       D("0.42"),
    'pad_l' :       D("1.0"),
    'rounding' :    D("0.05"),
    'pitch' :       D("0.65"),
    'n' :           16,
    'width' :       D("3.7"),
    'quad' :        True,
    'thermal_x' :   D("2.30"),
    'thermal_y' :   D("2.30"),
    'indent' :      D("0.2"),
    'courtyard_x' : D("4"),
    'courtyard_y' : D("4"),
    'paste_fraction' : D("0.60"),
    'paste_max' :   D("1.5")
}

MLP8 = {
    'name' :        "MLP8",
    'pad_w' :       D("0.65"),
    'pad_l' :       D("1.3"),
    'rounding' :    D("0.05"),
    'pitch' :       D("1.27"),
    'n' :           8,
    'width' :       D("7.3"),
    'quad' :        False,
    'thermal_x' :   D("5.0"),
    'thermal_y' :   D("5.36"),
    'indent' :      D("0.1"),
    'courtyard_x' : D("6"),
    'courtyard_y' : D("8"),
    'paste_fraction' : D("0.60"),
    'paste_max' :   D("1.5")
}

RGC_S_PVQFN_N64 = {
    'name' :        "RGC (S_PVQFN_N64)",
    'pad_w' :       D("0.28"),
    'pad_l' :       D("0.85"),
    'rounding' :    D("0.05"),
    'pitch' :       D("0.50"),
    'n' :           64,
    'width' :       D("8.95"),
    'quad' :        True,
    'thermal_x' :   D("4.25"),
    'thermal_y' :   D("4.25"),
    'indent' :      D("0.1"),
    'courtyard_x' : D("9.15"),
    'courtyard_y' : D("9.15"),
    'paste_fraction' : D("0.70"),
    'paste_max' :   D("2"),
    'pad_paste_fraction' : D("0.80")
}


def indent_pad(size, indent):
    return pscad.union() & (
        pscad.translate([-size[0] / D(2), -size[1] / D(2)]) & (
            pscad.square([size[0], size[1] - indent]) |

            pscad.right(indent) &
            pscad.square([size[0] - indent, size[1]]) |
            
            pscad.down(size[1] - indent) &
            pscad.rotate(45) & pscad.square(indent * dmath.sqrt(D(2)))
        )
    )

def thermal_pad(pad, size, paste_fraction, max_paste_size):
    paste_x = size[0] * dmath.sqrt(paste_fraction)
    paste_y = size[1] * dmath.sqrt(paste_fraction)
    n_x = dmath.ceil(paste_x / max_paste_size)
    n_y = dmath.ceil(paste_y / max_paste_size)

    # FIXME: rounded?
    paste_pad = pscad.square([paste_y / n_y, paste_x / n_x], center=True)
    return pscad.union() & (
        pscad.row(pscad.rotate(90) & pscad.row(paste_pad, size[1] / n_y, n_y, center=True),
            size[0] / n_x, n_x, center=True) |
        pscad.nopaste() & pad
    )

def paste_scale_pad(pad, paste_fraction):
    return pscad.union() & (
        pscad.scale(dmath.sqrt(paste_fraction)) & pad |
        pscad.nopaste() & pad
    )

def mlp_pad(m):
    pad = pscad.union() & (
        pscad.down(m['pad_l'] / D(2) - m['rounding']) &
        pscad.square((m['pad_w'], m['rounding'] * D(2)), rounded=True, center=True) |

        pscad.up((m['pad_l'] - m['pad_w']) / D(2)) &
        pscad.circle(m['pad_w'] / D(2)) &
        pscad.left(m['pad_w'] / D(2)) &
        pscad.square((m['pad_w'], m['pad_l'] - m['rounding'] - m['pad_w'] / D(2)))
    )
    if 'pad_paste_fraction' in m:
        return paste_scale_pad(pad, m['pad_paste_fraction'])
    else:
        return pad

def mlp_row(m, n):
    return pscad.down(m['width'] / D(2)) & pscad.row(mlp_pad(m), m['pitch'], n, center=True)

def mlp(m, clearance=D("0.15"), mask=D("0.05"), silk_w=D("0.2")):

    thermal_size = (m['thermal_x'], m['thermal_y'])
    row = mlp_row(m, m['n'] / (4 if m['quad'] else 2))

    if m['quad']:
        pads = pscad.pad(itertools.count(1), clearance, mask) & (
            row | pscad.rotate(90) & row | pscad.rotate(180) & row | pscad.rotate(270) & row |
            thermal_pad(indent_pad(thermal_size, m['indent']),
                thermal_size, m['paste_fraction'], m['paste_max'])
        )
    else:
        pads = pscad.pad(itertools.count(1), clearance, mask) & (
            row | pscad.rotate(180) & row |
            thermal_pad(indent_pad(thermal_size, m['indent']),
                thermal_size, m['paste_fraction'], m['paste_max'])
        )

    corner = pscad.translate([m['courtyard_x'] / D(2), m['courtyard_y'] / D(2)]) & (
        pscad.line([-m['pad_l'] / D(2), 0]) | pscad.line([0, -m['pad_l'] / D(2)])
    )

    silk = pscad.silk(w=silk_w) & (
        corner | pscad.mirror([0, 1]) & corner |
        pscad.mirror([1, 0]) & (
            corner | pscad.mirror([0, 1]) & corner
        ) |

        pscad.translate([-m['courtyard_x'] / D(2), m['courtyard_y'] / D(2)]) &
        pscad.down(silk_w * D(2)) &
        pscad.line(m['pad_l'] / D(2))
    )

    pscad.element(pads | silk, m['name'])

if __name__ == "__main__":
    mlp(RGC_S_PVQFN_N64)

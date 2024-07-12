# module powerpak-so8
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

defaults = {
    "round_off" :   "0.1",
    "clearance" :   "0.2",
    "mask" :        "2.5 mil",
    "silk" :        "0.2",
    "placement" :   "0.25",
    "grid" :        "0.5",
    'paste_fraction': "0.35",
    'pad_paste_fraction': "1.0",
}

def part(m):
    m = pscad.wrapper(list(defaults.items()) + list(m.items()))

    pad_size = [D("0.2950"), D("0.725")]
    pad_size26 = [D("1.150"), D("1.050")]
    pad_size27a = [D("2.175"), D("1.200")]
    pad_size27b = [D("2.875"), D("0.455")]
    pad_sizeSW = [D("2.345"), D("0.275")]
    pad_size28 = [D("0.580"), D("0.380")]
    pad_size25 = [D("1.575"), D("1.050")]
    body_size = [D("4.0"), D("4.0")]

    pad = pscad.paste_fraction(pscad.rounded_square(pad_size, m.round_off, center=True), (1, m.pad_paste_fraction))
    padr = (pscad.rotate(90) + pad,)
    pad26 = pscad.rounded_square(pad_size26, m.round_off, center=True)
    pad27 = (pscad.union() + pscad.rounded_square(pad_size27a, m.round_off, center=True) +
            pscad.left(pad_size27a[0] / 2 - pad_size27b[0] / 2) +
            pscad.up(pad_size27a[1] / 2 - pad_size27b[1] / 2) +
            pscad.nopaste() + pscad.rounded_square(pad_size27b, m.round_off, center=True),)
    pad28 = pscad.rounded_square(pad_size28, m.round_off, center=True)
    pad5 =  (pscad.union() + pad + pscad.down(pad_size[1] / 2 - pad_sizeSW[1] / 2) +
            pscad.left(pad_sizeSW[0] / 2 - pad_size[0] / 2) +
            pscad.nopaste() + pscad.rounded_square(pad_sizeSW, m.round_off, center=True),)
    pad25 = pscad.rounded_square(pad_size25, m.round_off, center=True)


    left = pscad.left(body_size[0] / 2 + D("0.3") - pad_size[1] / 2) + pscad.up(body_size[1] / 2) + (
        pscad.down(1.175) + padr +
	pscad.down(0.45) + padr +
	pscad.down(0.90) + padr +
        pscad.down(0.45) + padr
    )

    bottom = pscad.down(body_size[0] / 2 + D("0.3") - pad_size[1] / 2) + pscad.left(body_size[1] / 2) + (
        pscad.right(0.525) + (pscad.rotate(180) + pad5,) +
	pscad.right(0.45) + pad +
	pscad.right(0.45) + pad +
	pscad.right(0.70) + pad +
        pscad.right(0.45) + pad +
        pscad.right(0.45) + pad
    )

    right = pscad.right(body_size[0] / 2 + D("0.3") - pad_size[1] / 2) + pscad.down(body_size[1] / 2) + (
        pscad.up(0.575) + padr +
	pscad.up(0.45) + padr +
        pscad.up(0.45) + padr +
	pscad.up(0.45) + padr +
        pscad.up(0.45) + padr +
	pscad.up(0.45) + padr +
        pscad.up(0.45) + padr
    )

    top = pscad.up(body_size[0] / 2 + D("0.3") - pad_size[1] / 2) + pscad.right(body_size[1] / 2) + (
        pscad.left(0.525) + pad +
	pscad.left(0.45) + pad +
	pscad.left(0.45) + pad +
	pscad.left(0.45) + pad +
	pscad.left(0.70) + pad +
        pscad.left(0.45) + pad +
        pscad.left(0.45) + pad
    )

    all = (
        pscad.pad(itertools.count(1), m.clearance, m.mask) + (
            left, bottom, right, top,
            (
                pscad.right(body_size[0] / 2 - D("0.725") - pad_size25[0] / 2) +
                pscad.up(body_size[1] / 2 - D("0.725") - D("1.05") + pad_size25[1] / 2) +
                pscad.paste_fraction(pad25, m.paste_fraction)
            ),
            (
                pscad.left(body_size[0] / 2 - D("0.25") - pad_size26[0] / 2) +
                pscad.up(body_size[1] / 2 - D("1.175") - D("0.45") - D("0.3") / 2 + pad_size26[1] / 2) +
                pscad.paste_fraction(pad26, m.paste_fraction)
            ),
            (
                pscad.left(body_size[0] / 2 - D("0.25") - pad_size27a[0] / 2) +
                pscad.down(body_size[1] / 2 - D("1.025") - D("0.45") - D("0.3") / 2 - D("0.3") + pad_size27a[1] / 2) +
                pscad.paste_fraction(pad27, m.paste_fraction)
            ),
            (
                pscad.right(body_size[0] / 2 - D("0.725") - pad_size28[0] / 2) +
                pscad.down(body_size[1] / 2 + D("0.3") - D("0.73") - D("0.39") - pad_size28[1] / 2) +
                pscad.paste_fraction(pad28, (m.paste_fraction, 1))
            ),
        ),
        pscad.silk(m.silk) + patterns.corners(body_size, D("0.2"), center=True)
    )

    silk = pscad.silk(m.silk) + (
        patterns.placement_courtyard(all, m.placement, m.grid, D("0.5")),

        pscad.up(body_size[1] / 2) +
        pscad.left(body_size[0] / 2 + D("0.5")) +
        pscad.rotate(270) + pscad.line(pad_size[0])
    )

    return all, silk


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
from string import ascii_uppercase
import itertools

def bga_letters(skip):
    return itertools.ifilterfalse(lambda x: x in skip, ascii_uppercase)

def bga_dletters(skip):
    return (i[0] + i[1] for i in itertools.product([''] + list(bga_letters(skip)), bga_letters(skip)))

def bga_names(n, skip = 'IOQSXZ'):
    return (i[0] + str(i[1]) for i in itertools.product(bga_dletters(skip), range(1, n+1)))

def bga(name, pad, pitch, n, courtyard, clearance, mask, silk_w):

    row = pscad.row(pscad.circle(pad / D(2)), pitch, n[0], center=True)
    pads = (
        pscad.pad(bga_names(n[0]), clearance, mask) &
        pscad.rotate(270) & pscad.row(pscad.rotate(90) & row, pitch, n[1], center=True)
    )

    silk = pscad.silk(w=silk_w) & (
        pscad.square(courtyard, center=True) |

        pscad.translate([-courtyard[0] / D(2), -pitch * (n[1] - 1) / D(2)]) &
        pscad.left(silk_w * D(2)) & pscad.line([0, pitch * D(2)], center=True)
    )

    pscad.element(pads | silk, name)

if __name__ == "__main__":
    bga("FF784", D("0.45"), D("1.0"), (28, 28), (D("29.0"), D("29.0")), D("0.15"), D("0.05"), D("0.2"))



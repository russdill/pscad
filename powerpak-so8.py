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

def powerpak(name):

    pitch = D("1.27")
    round_off = D("0.1")
    pad_size0 = [D("0.61"), D("1.27")]
    pad_size1 = [D("0.61"), D("1.02")]
    pad_size2 = [D("1.65"), D("3.81")]
    width = D("6.61")
    clearance = D("0.2")
    mask = D("0.2")
    silk_w = D("0.2")
    courtyard = [D("6.26"), D("7.25")]

    thermal_pad = pscad.union() & (
        pscad.rounded_square([pad_size2[0] * D("0.8"), pad_size2[1] * D("0.6")], round_off, center=True) |
        pscad.nopaste() & pscad.rounded_square(pad_size2, round_off, center=True)
    )

    pads = (
        pscad.pad(itertools.count(1), clearance, mask) &
        pscad.down((width - pad_size0[1]) / D(2)) &
        pscad.row(pscad.rounded_square(pad_size0, round_off, center=True), pitch, 4, center=True) |

        pscad.pad((i for i in [6, 6, 5, 5]), clearance, mask) &
        pscad.up((width - pad_size1[1]) / D(2)) &
        pscad.row(pscad.rounded_square(pad_size1, round_off, center=True), pitch, 4, center=True) |

        pscad.pad((i for i in [6, 5]), clearance, mask) &
        pscad.down(width / D(2)) &
        pscad.up(pad_size0[1] + D("0.82") + pad_size2[1] / D(2)) &
        pscad.row(thermal_pad, D("0.61") + pad_size2[0], 2, center=True)
    )

    silk = pscad.silk(silk_w) & (
        pscad.square(courtyard, center=True) |

        pscad.down(width / D(2)) &
        pscad.left(courtyard[0] / D(2) - silk_w * D(3)) &
        pscad.line([0, -pad_size0[1]])
    )

    pscad.element(pads | silk, name)

if __name__ == "__main__":
    powerpak("PowerPAK SO-8")

# module tp
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

defaults = {
    'round_off' :   "0.2",
    'clearance' :   "0.15",
    'mask' :        "2.5 mil",
}

def part(m):
    m = pscad.wrapper(defaults.items() + m.items())

    all = pscad.pad('1', m.clearance, m.mask) + (
          pscad.rounded_square((m.pad_w, m.pad_l), m.round_off, center=True)
    )

    return all


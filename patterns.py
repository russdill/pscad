import pscad
import dmath
from decimal import Decimal as D

def corners(sz, n, center=False):
    corner = pscad.translate([sz[0] / 2, sz[1] / 2]) + (
        pscad.line([-n / 2, 0]),
        pscad.line([0, -n / 2])
    )
    corners = (
        corner,
        pscad.mirror([0, 1]) + corner,
        pscad.mirror([1, 0]) + (
            corner,
            pscad.mirror([0, 1]) + corner
        )
    )
    if not center:
        corners = pscad.translate([sz[0] / 2, sz[1] / 2]) + corners
    return corners,

def brackets(sz, n, center=False):

    bracket = pscad.translate([sz[0] / 2, sz[1] / 2]) + (
        pscad.line([-n / 2, 0]),
        pscad.line([0, -sz[1]]),
        pscad.up(sz[1]) + pscad.line([-n / 2, 0])
    )
    bracket = bracket, pscad.mirror([1, 0]) + bracket
    if not center:
        bracket = pscad.translate([sz[0] / 2, sz[1] / 2]) + bracket
    return bracket,

def placement_courtyard(obj, placement, grid, sz):
    courtyard = pscad.expand_to_grid(pscad.bound(obj), placement, grid)
    courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])
    return pscad.translate(courtyard[0]) + corners(courtyard_sz, sz),

def thermal_pad(pad, size, paste_fraction, max_paste_size):
    paste_x = size[0] * dmath.sqrt(paste_fraction)
    paste_y = size[1] * dmath.sqrt(paste_fraction)
    n_x = dmath.ceil(paste_x / max_paste_size)
    n_y = dmath.ceil(paste_y / max_paste_size)

    paste_pad = pscad.rounded_square([paste_y / n_y, paste_x / n_x], D("0.05"), center=True)
    return pscad.union() + (
        pscad.row(pscad.rotate(90) + pscad.row(paste_pad, size[1] / n_y, n_y, center=True),
            size[0] / n_x, n_x, center=True),
        pscad.nopaste() + pad
    )

def indent_pad(size, indent):
    return pscad.union() + (
        pscad.translate([-size[0] / 2, -size[1] / 2]) + (
            pscad.square([size[0], size[1] - indent]),

            pscad.right(indent) +
            pscad.square([size[0] - indent, size[1]]),

            pscad.down(size[1] - indent) +
            pscad.rotate(45) + pscad.square(indent * dmath.sqrt(D(2)))
        )
    )


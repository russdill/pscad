import pscad
from decimal import Decimal as D

def corners(sz, n, center=False):
    corner = pscad.translate([sz[0] / D(2), sz[1] / D(2)]) + (
        pscad.line([-n / D(2), 0]),
        pscad.line([0, -n / D(2)])
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
        corners = pscad.translate([sz[0] / D(2), sz[1] / D(2)]) + corners
    return corners,

def brackets(sz, n, center=False):

    bracket = pscad.translate([sz[0] / D(2), sz[1] / D(2)]) + (
        pscad.line([-n / D(2), 0]),
        pscad.line([0, -sz[1]]),
        pscad.up(sz[1]) + pscad.line([-n / D(2), 0])
    )
    bracket = bracket, pscad.mirror([1, 0]) + bracket
    if not center:
        bracket = pscad.translate([sz[0] / D(2), sz[1] / D(2)]) + bracket
    return bracket,

def placement_courtyard(obj, placement, grid, sz):
    courtyard = pscad.expand_to_grid(pscad.bound(obj), placement, grid)
    courtyard_sz = (courtyard[1][0] - courtyard[0][0], courtyard[1][1] - courtyard[0][1])
    return pscad.translate(courtyard[0]) + corners(courtyard_sz, sz),

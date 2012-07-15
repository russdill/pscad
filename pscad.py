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

import copy
import sys
import os.path
from numpy import eye, matrix
from decimal import Decimal as D
import dmath

# Returns mm
def parse_unit(val):
    try:
        return D(val)
    except:
        ext = val.lstrip('+-0123456789.eE ')
        m = D(1)
        if len(ext):
            val = val[0:-len(ext)]
            try:
                if ext.lower() in ( "mil", "mils", "thou" ):
                    m = D("0.0254")
                elif ext.lower() in ( "in", "inch", "inches", '"' ):
                    m = D("25.4")
                elif len(ext) == 2 and ext[1] == 'm':
                    e = D('fpnum.kMGT'.find(ext[0]))
                    assert e != -1
                    e = (e - 4) * 3
                    m = 10**e
                elif len(ext) == 1 and ext[0] == 'm':
                    m = 1000
                else:
                    raise
            except:
                raise Exception("Unknown unit " + ext)
        return D(val) * m

def xform1(m, p):
    row = (m * matrix([ p[0], p[1], 1]).transpose()).transpose().tolist()[0]
    return (row[0], row[1])

def xform(m, p):
    try:
        return xform1(m, p)
    except:
        return [ xform(m, n) for n in p ]

def P(n):
    return str(n.quantize(D("0.000001"))) + "mm"

class cache_holder(object):
    def __init__(self, string):
        self.value = string

class local_state(object):
    def __init__(self, other=None):
        if other is None:
            self.m = matrix(eye(3, dtype=D))
            self.render = self.null_render
            self.meta = dict()
            self.name = None
            self.cache = None
            self.onsolder = False
            self.paste = True
        else:
            self.m = copy.deepcopy(other.m)
            self.render = other.render
            self.meta = other.meta
            self.name = other.name
            self.cache = other.cache
            self.onsolder = other.onsolder
            self.paste = other.paste

    def null_render(self, obj, state):
        return []

    def next_name(self):
        try:
            return self.name.next()
        except:
            return str(self.name)

    def get_name(self):
        if self.cache:
            if self.cache.value is None:
                self.cache.value = self.next_name()
            return self.cache.value
        else:
            return self.next_name()

    def get_onsolder(self):
        return self.onsolder

    def get_paste(self):
        return self.paste

def bound(obj, state=None):
    if state is None:
        state = local_state()
    ret = []
    if type(obj) is tuple:
        for o in obj:
            tmp_state = local_state(state)
            ret += bound(o, tmp_state)
    else:
        obj.pre(state)
        ret += obj.bound(state)
    return bound_collapse(ret)

def bound_collapse(bounds):
    if not len(bounds):
        return []
    upper = lower = bounds[0][1]
    right = left = bounds[0][0]
    for p in bounds[1:]:
        upper = min(upper, p[1])
        lower = max(lower, p[1])
        left = min(left, p[0])
        right = max(right, p[0])
    return ((left, upper), (right, lower))

def render(obj, state):
    ret = []
    if type(obj) is tuple:
        for o in obj:
            tmp_state = local_state(state)
            ret += render(o, tmp_state)
    else:
        ret += obj.do_render(state)
    return ret

class pscad(object):
    def __init__(self):
        self.points = []
        self.paths = []

    def __add__(self, obj):
        return link(self, obj)

    def __radd__(self, obj):
        return link(obj, self)

    def pre(self, state):
        try:
            state.render = self.render
        except:
            pass

    def bound(self, state):
        return []

    def do_render(self, state):
        self.pre(state)
        return state.render(self, state)

class empty(pscad):
    def __init__(self):
        super(empty, self).__init__()

class link(pscad):
    def __init__(self, a, b=None):
        super(link, self).__init__()
        if type(a) is link and type(b) is link:
            self.objs = a.objs + b.objs
        elif type(a) is link:
            self.objs = list(a.objs)
            if b is not None:
                self.objs.append(b)
        elif type(b) is link:
            self.objs = [a] + list(b.objs)
        else:
            self.objs = [a]
            if b is not None:
                self.objs.append(b)

    def do_render(self, state):
        ret = []
        for obj in self.objs:
            ret += render(obj, state)
        return ret

    def bound(self, state):
        ret = []
        for obj in self.objs:
            ret += bound(obj, state)
        return ret

class union(pscad):
    def __init__(self, name=None, skip=None):
        super(union, self).__init__()
        self.name = name
        self.skip = skip
        
    def pre(self, state):
        super(union, self).pre(state)
        if self.name is None:
            if state.cache is None:
                state.cache = cache_holder(None)
        else:
            state.name = self.name
            state.cache = None

    def should_skip(self, name):
        try:
            return name in self.skip
        except:
            pass
        try:
            return self.skip(name)
        except:
            pass
        try:
            return len(name) == 0
        except:
            pass
        return False

class back(pscad):
    back = False
    def __init__(self):
        super(back, self).__init__()

    def pre(self, state):
        super(back, self).pre(state)
        state.onsolder = not state.onsolder

class paste(pscad):
    def __init__(self, has=True):
        super(paste, self).__init__()
        self.should_have = has

    def pre(self, state):
        super(paste, self).pre(state)
        state.paste = self.should_have

class nopaste(paste):
    def __init__(self):
        super(nopaste, self).__init__(False)

class multmatrix(pscad):
    def __init__(self, m=None):
        super(multmatrix, self).__init__()
        self.m = matrix(eye(3, dtype=D)) if m is None else m

    def pre(self, state):
        super(multmatrix, self).pre(state)
        state.m *= self.m

class translate(multmatrix):
    def __init__(self, v):
        super(translate, self).__init__()
        self.m[0,2] = D(v[0])
        self.m[1,2] = D(v[1])

class rotate(multmatrix):
    def __init__(self, a):
        super(rotate, self).__init__()
        a = dmath.radians(D(a))
        self.m[0,0] = self.m[1,1] = D(dmath.cos(a))
        self.m[0,1] = D(dmath.sin(a))
        self.m[1,0] = -D(dmath.sin(a))

class scale(multmatrix):
    def __init__(self, v):
        super(scale, self).__init__()
        try:
            _v = [ v[0], v[1] ]
        except:
            v = [ v, v ]
        self.m[0,0] = D(v[0])
        self.m[1,1] = D(v[1])

class mirror(multmatrix):
    def __init__(self, v):
        super(mirror, self).__init__()
        a, b = D(v[0]), -D(v[1])
        a = a / dmath.hypot(a, b)
        b = b / dmath.hypot(a, b)
        self.m[0,0] = 1 - D(2) * a * a
        self.m[0,1] = - D(2) * a * b
        self.m[1,0] = - D(2) * a * b
        self.m[1,1] = 1 - D(2) * b * b

class shape(pscad):
    def __init__(self, v = None):
        super(shape, self).__init__()

    def bound(self, state):
        return xform(state.m, self.points)

class polygon(shape):
    def __init__(self, points, paths=None):
        super(shape, self).__init__()
        self.points = points
        if paths is None:
            paths = range(len(points))
            paths.append(0)
        self.paths = paths

class square(shape):
    def __init__(self, v, center=False, rounded=False):
        super(square, self).__init__()
        try:
            v = [ D(v[0]), D(v[1]) ]
        except:
            v = [ D(v), D(v) ]
        o = (D(0), D(0)) if center else (v[0] / D(2), v[1] / D(2))
        self.points.append((o[0] - v[0] / D(2), o[1] - v[1] / D(2)))
        self.points.append((o[0] - v[0] / D(2), o[1] + v[1] / D(2)))
        self.points.append((o[0] + v[0] / D(2), o[1] + v[1] / D(2)))
        self.points.append((o[0] + v[0] / D(2), o[1] - v[1] / D(2)))
        self.paths.append([0, 1, 2, 3, 0])
        # Only for pads
        self.rounded = rounded

class point(shape):
    def __init__(self):
        super(point, self).__init__()
        self.points.append((D(0), D(0)))

class line(shape):
    def __init__(self, size, center=False):
        super(line, self).__init__()
        try:
            size = [ D(size[0]), D(size[1]) ]
        except:
            size = [ D(size), D(0) ]
        o = (D(0), D(0)) if center else (size[0] / D(2), size[1] / D(2))
        self.points.append((o[0] - size[0] / D(2), o[1] - size[1] / D(2)))
        self.points.append((o[0] + size[0] / D(2), o[1] + size[1] / D(2)))
        self.paths.append([0, 1])

class circle(shape):
    def __init__(self, r, sweep=None):
        super(circle, self).__init__()
        r = D(r)
        self.points.append((D(0), D(0)))
        self.points.append((r, D(0)))
        self.points.append((D(0), r))
        if sweep is not None:
            assert sweep > 0 and sweep < 360
            sweep = dmath.radians(D(sweep))
            self.points.append((dmath.cos(sweep) * r, dmath.sin(sweep) * r))
        self.full = sweep is None

    def center_radius_angle(self, m):
        points = xform(m, self.points)
        c = points[0]
        r, a = [], []
        for p in points[1:]:
            dx, dy = p[0] - c[0], p[1] - c[1]
            r.append(dmath.hypot(dx, dy))
            a.append(dmath.atan2(-dy, dx))
        return c, r, a

    def bound(self, state):
        c, r, a = self.center_radius_angle(state.m)
        # Use derivative of ellipse equation to find angle of min max points
        tx = dmath.atan2(-r[1] * dmath.sin(a[0]), -r[0] * dmath.cos(a[0]))
        ty = dmath.atan2(r[1] * dmath.cos(a[0]), -r[0] * dmath.sin(a[0]))
        # plug those numbers back into the ellipse equations
        dx = dmath.fabs(r[0] * dmath.cos(tx) * dmath.cos(a[0]) - r[1] * dmath.sin(tx) * dmath.sin(a[0]))
        dy = dmath.fabs(r[0] * dmath.cos(ty) * dmath.sin(a[0]) + r[1] * dmath.sin(ty) * dmath.cos(a[0]))
        return ((c[0] - dx, c[1] - dy), (c[0] + dx, c[1] + dy))

class donut(circle):
    def __init__(self, inner, outer):
        super(donut, self).__init__(outer)
        self.child = circle(inner)

class silk(pscad):
    def __init__(self, w):
        super(silk, self).__init__()
        self.w = D(w)

    def render(self, obj, state):
        ret = []
        points = xform(state.m, obj.points)
        if type(obj) == circle:
            c, r, a = obj.center_radius_angle(state.m)
            a = [ dmath.degrees(n) for n in a ]
            if obj.full:
                ret.append("ElementArc [ %s %s %s %s 0 360 %s ]" % (
                    P(c[0]), P(c[1]), P(r[0]), P(r[1]), P(self.w)))
            else:
                # Sweep direction should be clockwise (check for mirrored component)
                if (a[1] - a[0]) % 360 > 0:
                    sweep = a[0] - a[2]
                else:
                    sweep = a[2] - a[0]
                start = (a[0] % 360).quantize(D('1.00'))
                sweep = (sweep % 360).quantize(D('1.00'))
                ret.append("ElementArc [ %s %s %s %s %s %s %s ]" % (
                    P(c[0]), P(c[1]), P(r[0]), P(r[1]), start, sweep, P(self.w)))
                
        else:
           for path in obj.paths:
               for i in range(0, len(path) - 1):
                   p0 = points[path[i]]
                   p1 = points[path[i + 1]]
                   ret.append("ElementLine [ %s %s %s %s %s ]" % (
                       P(p0[0]), P(p0[1]), P(p1[0]), P(p1[1]), P(self.w)))
        return ret

class pad(union):
    def __init__(self, name, clearance, mask, skip=None):
        super(pad, self).__init__(name, skip)
        self.clearance = D(clearance)
        self.mask = D(mask)

    def rect_pad(self, name, points, rounded, state):
        m = []
        ret = []
        for i in range(len(points)):
            p0, p1 = points[i], points[(i + 1) % len(points)]
            m.append(((p0[0] + p1[0]) / D(2), (p0[1] + p1[1]) / D(2)))
        dim0 = dmath.hypot(m[2][0] - m[0][0], m[2][1] - m[0][1])
        dim1 = dmath.hypot(m[3][0] - m[1][0], m[3][1] - m[1][1])

        c = ((m[0][0] + m[2][0]) / D(2), (m[0][1] + m[2][1]) / D(2))

        if dim0.quantize(D("0.000001")) == dim1.quantize(D("0.000001")):
            if rounded:
                ret.append(circ_pad(name, c, dim0 / D(2)), state)
            else:
                ret += self.rect_pad(name, [ points[0], points[1], m[1], m[3] ], False, state)
                ret += self.rect_pad(name, [ m[3], m[1], points[2], points[3] ], False, state)
            return ret
        if dim0 > dim1:
            angle = dmath.atan2(m[2][1] - m[0][1], m[2][0] - m[0][0])
        else:
            angle = dmath.atan2(m[3][1] - m[1][1], m[3][0] - m[1][0])

        flags = []
        if not rounded:
            flags.append("square")
        if state.get_onsolder():
            flags.append("onsolder")
        if not state.get_paste():
            flags.append("nopaste")

        thickness = min(dim0, dim1) / D(2)
        width = max(dim0, dim1) - thickness * D(2)
        p = []
        p.append((c[0] + dmath.cos(angle) * width / D(2), c[1] + dmath.sin(angle) * width / D(2)))
        p.append((c[0] - dmath.cos(angle) * width / D(2), c[1] - dmath.sin(angle) * width / D(2)))
        ret.append("""Pad [ %s %s %s %s %s %s %s "%s" "%s" "%s" ]""" % (
            P(p[0][0]), P(p[0][1]), P(p[1][0]), P(p[1][1]), P(thickness * D(2)),
            P(self.clearance * D(2)), P((self.mask + thickness) * D(2)), name, name,
            ",".join(flags)))
        return ret

    def circ_pad(self, name, c, r, state):
        flags = []
        if state.get_onsolder():
            flags.append("onsolder")
        if not state.get_paste():
            flags.append("nopaste")
        return """Pad [ %s %s %s %s %s %s %s "%s" "%s" "%s" ]""" % (
            P(c[0]), P(c[1]), P(c[0]), P(c[1]), P(r * D(2)),
            P(self.clearance * D(2)), P((self.mask + r) * D(2)), name, name,
            ",".join(flags))

    def render(self, obj, state):
        ret = []
        points = xform(state.m, obj.points)
        if type(obj) == circle:
            name = state.get_name()
            if self.should_skip(name): return ret
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
            r = dmath.hypot(dx, dy)
            ret.append(self.circ_pad(name, points[0], r, state))
        elif type(obj) == square:
            name = state.get_name()
            if self.should_skip(name): return ret
            p = []
            for i in range(0, len(obj.paths[0]) - 1):
                p.append(points[obj.paths[0][i]])
            ret += self.rect_pad(name, p, obj.rounded, state)
        elif type(obj) == union:
            pass

        return ret

class pin(union):
    def __init__(self, name, clearance, mask, square=False, skip=None):
        super(pin, self).__init__(name, skip)
        self.clearance = D(clearance)
        self.mask = D(mask)
        self.square = square

    def render(self, obj, state):
        ret = []
        if type(obj) == donut:
            name = state.get_name()
            if self.should_skip(name): return ret
            c, r1, a1 = obj.center_radius_angle(state.m)
            _, r2, a2 = obj.child.center_radius_angle(state.m)
            ret.append("""Pin [ %s %s %s %s %s %s "%s" "%s" "" ]""" % (
                P(c[0]), P(c[1]), P(r1[0] * D(2)), P(self.clearance * D(2)),
                P((self.mask + r1[0]) * D(2)), P(r2[0] * D(2)), name, name))
            if self.square:     
                tmp_state = local_state(state)
                sq = square(obj.points[1][0] * D(2), center=True)
                un = union(name, tmp_state)
                np = nopaste()
                os = back()
                un.pre(tmp_state)
                np.pre(tmp_state)
                ret += pad(None, self.clearance, self.mask).render(sq, tmp_state)
                os.pre(tmp_state)
                ret += pad(None, self.clearance, self.mask).render(sq, tmp_state)
        return ret

class hole(pscad):
    def __init__(self, clearance, mask):
        super(hole, self).__init__()
        self.clearance = D(clearance)
        self.mask = D(mask)

    def render(self, obj, state):
        ret = []
        points = xform(state.m, obj.points)
        if type(obj) == circle:
            dx = points[1][0] - points[0][0]
            dy = points[1][1] - points[0][1]
            r = dmath.hypot(dx, dy)
            ret.append("""Pin [ %s %s %s %s %s %s "" "" "hole" ]""" % (
                P(points[0][0]), P(points[0][1]), P(r * D(2)),
                P(self.clearance * D(2)), P((self.mask + r) * D(2)),
                P(r * D(2))))
        return ret
 
class mark(pscad):
    def __init__(self):
        super(mark, self).__init__()

    def render(self, obj, state):
        if len(obj.points) > 0:
            assert len(obj.points) == 1
            assert "mark" not in state.meta
            state.meta["mark"] = xform(state.m, obj.points[0])
        return []

class text(pscad):
    def __init__(self, sz = 100):
        super(text, self).__init__()
        self.sz = 100

    def render(self, obj, state):
        if len(obj.points) > 0:
            assert len(obj.points) == 1
            assert "text" not in meta
            p0 = xform(state.m, obj.points[0])
            p1 = xform(state.m, (obj.points[0][0] + 1, obj.points[0][1]))
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            scale = math.hypot(dx, dy)
            angle = (math.degrees(math.atan2(-dy, dx)) + 45) % 360
            state.meta["text"] = (p0, floor(angle / 90), scale * sz)
        return []

class wrapper(dict):
    def __getattr__(self, name):
        v = self[name]
        try:
            v = parse_unit(v)
        except:
            if v.lower() in ("true", "false"):
                v = v.lower() == "true"
        return v

def element(n, desc):
    state = local_state()
    statements = render(n, state)

    if "mark" in state.meta:
        m = state.meta["mark"]
    else:
        m = (D(0), D(0))

    if "text" in state.meta:
        t, dir, scale = state.meta["text"]
    else:
        t, dir, scale = (D(0), D(0)), 0, 100

    print """Element [0x00 "%s" "" "" %s %s %s %s %s %s 0x00]""" % (
        desc, P(m[0]), P(m[1]), P(t[0]), P(t[1]), dir, scale)
    print "("
    for statement in statements:
        print "\t" + statement
    print ")"

# PCB uses screen coordinates, not cartesian
def up(v):
    return translate([0, -v])

def down(v):
    return translate([0, v])

def left(v):
    return translate([-v, 0])

def right(v):
    return translate([v, 0])

def rounded_square(v, r, center=False):
    if r == 0:
        return square(v, center),
    try:
        v = [ D(v[0]), D(v[1]) ]
    except:
        v = [ D(v), D(v) ]

    if r * D(2) == min(v):
        return square(v, center, rounded=True),

    assert r * D(2) < min(v)

    o = (D(0), D(0)) if center else (v[0] / D(2), v[1] / D(2))
    r = D(r)
    return union() + translate(o) + (
        square((v[0] - r * D(2), v[1] - r * D(2)), center=True),
        left(v[0] / D(2) - r) + square([r * D(2), v[1]], center=True, rounded=True),
        right(v[0] / D(2) - r) + square([r * D(2), v[1]], center=True, rounded=True),
        up(v[1] / D(2) - r) + square([v[0], r * D(2)], center=True, rounded=True),
        down(v[1] / D(2) - r) + square([v[0], r * D(2)], center=True, rounded=True)
    ),

def row(obj, pitch, n, center=False):
    ret = tuple(right(i * pitch) + obj for i in range(n))
    if center:
        return left(pitch * (n - 1) / D(2)) + ret,
    else:
        return ret

def expand_to_grid(sq, expand, grid):
    return ((dmath.floor((sq[0][0] - expand) / grid) * grid,
             dmath.floor((sq[0][1] - expand) / grid) * grid),
            (dmath.ceil((sq[1][0] + expand) / grid) * grid,
             dmath.ceil((sq[1][1] + expand) / grid) * grid))

def paste_fraction(pad, fraction):
    return union() + (
        scale(dmath.sqrt(fraction)) + pad,
        nopaste() + pad
    ),

def parse_file(name):
    ret = {"_deps": set()}
    for line in open(name):
        line = line.partition('#')[0].strip()
        try:
            key, value = line.split(None, 1)
        except:
            continue
        key = key.lower()
        if key == "include":
            sub = parse_file(value)
            deps = sub["_deps"] | ret["_deps"] | set((value,))
            ret.update(sub)
            ret["_deps"] = deps
        else:
            ret[key] = value
    return ret

if __name__ == "__main__":
    do_deps = False
    if "-M" in sys.argv:
        do_deps = True
        sys.argv.remove("-M")

    data = parse_file(sys.argv[1])
    module = __import__(data["module"])
    if do_deps:
        deps = [ i.__file__ for i in sys.modules.values() if i and getattr(i, "__file__", None)]
        other = []
        for dep in deps:
            if dep.endswith(".pyc") and os.path.isfile(dep[:-1]):
                other.append(dep[:-1])
        deps = set(deps) | set(other) | data["_deps"]
        print sys.argv[2] + ": " + " \\\n\t".join(deps)
    else:
        objs = getattr(module, data.get("part", "part"))(data)
        sys.stdout = open(sys.argv[2], 'wb')
        element(objs, data["name"])

"""
dmath v0.9.1

Python math module for Decimal numbers.  All functions should return Decimal
numbers.  Probably only works with real numbers.

pi, exp, cos, sin from Decimal recipes:
    http://docs.python.org/lib/decimal-recipes.html

float_to_decimal from Decimal FAQ:
    http://docs.python.org/lib/decimal-faq.html

Copyright (c) 2006 Brian Beck <exogen@gmail.com>,
                   Christopher Hesse <christopher.hesse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# TODO all inputs should be converted using convert_other to Decimal, and all results should be returned as Decimal (don't bother matching input types)
# TODO context should be taken as an argument when appropriate, especially when throwing an error, look at decimal.py for hints
# TODO should use custom convert_other that has the option of converting floats (using float_to_decimal) if an option is set in advance (just not by default)
# TODO try implementing something, say pi, in pyrex to compare the speed

import math
import decimal
from decimal import Decimal, getcontext, setcontext, _convert_other

D = Decimal

#
# utility functions
#

def float_to_decimal(f):
    """Convert a floating point number to a Decimal with no loss of information.
    """
    # Transform (exactly) a float to a mantissa (0.5 <= abs(m) < 1.0) and an
    # exponent.  Double the mantissa until it is an integer.  Use the integer
    # mantissa and exponent to compute an equivalent Decimal.  If this cannot
    # be done exactly, then retry with more precision.

    mantissa, exponent = math.frexp(f)
    while mantissa != int(mantissa):
        mantissa *= 2.0
        exponent -= 1
    mantissa = int(mantissa)

    oldcontext = getcontext()
    setcontext(Context(traps=[Inexact]))
    try:
        while True:
            try:
               return mantissa * Decimal(2) ** exponent
            except Inexact:
                getcontext().prec += 1
    finally:
        setcontext(oldcontext)

#
# constants
#

def pi(context=None):
    """Compute Pi to the current precision."""
    if context is None:
        context = getcontext()
    context.prec += 2
    lasts = 0; t = D(3); s = 3; n = 1; na = 0; d = 0; da = 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    context.prec -= 2
    return +s

def e():
    """Compute the base of the natural logarithm to the current precision."""
    return exp(D(1))

def golden_ratio():
    """Calculate the golden ratio to the current precision."""
    return  (1 + D(5).sqrt()) / 2

#
# transcendental functions
#

def exp(x, context=None):
    """Return e raised to the power of x."""
    if context is None:
        context = getcontext()
    
    context.prec += 2
    i = 0; lasts = 0; s = 1; fact = 1; num = 1
    while s != lasts:
        lasts = s    
        i += 1
        fact *= i
        num *= x     
        s += num / fact   
    context.prec -= 2        
    return +s

def log(x, base=None, context=None):
    """Return the logarithm of x to the given base.
    
    If the base not specified, return the natural logarithm (base e) of x.
    
    """
    if context is None:
        context = getcontext()
    
    if x < 0:
        return D('NaN', context=context)
    elif base == 1:
        raise ValueError("Base was 1!")
    elif x == base:
        return D(1, context=context)
    elif x == 0:
        return D('-Inf', context=context)
    
    context.prec += 2    
    
    if base is None:
        log_base = 1
        approx = math.log(x)
    else:
        log_base = log(base, context=context)
        approx = math.log(x, base)

    lasts, s = 0, D(repr(approx), context=context)
    while lasts != s:
        lasts = s
        s -=  1 - x / exp(s, context=context)
    s /= log_base
    context.prec -= 2
    return +s

def log10(x):
    """Return the base 10 logarithm of x."""
    return log(x, D(10))

#
# trigonometric functions
#

def sin(x, context=None):
    """Return the sine of x in radians."""
    if context is None:
        context = getcontext()

    # Uses the series definition of cos, see:
    # http://en.wikipedia.org/wiki/Trigonometric_function#Series_definitions
    context.prec += 2
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    while s != lasts:
        lasts = s    
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign *= -1
        s += num / fact * sign
    context.prec -= 2
    return +s

def cos(x, context=None):
    """Return the cosine of x in radians."""
    if context is None:
        context = getcontext()
    
    # Uses the series definition of cos, see:
    # http://en.wikipedia.org/wiki/Trigonometric_function#Series_definitions
    context.prec += 2
    i = 0; lasts = 0; s = 1; fact = 1; num = 1; sign = 1
    while s != lasts:
        lasts = s    
        i += 2
        fact *= i * (i - 1)
        num *= x * x
        sign = -sign
        s += num / fact * sign 
    context.prec -= 2        
    return +s

def tan(x, context=None):
    """Return the tangent of x in radians."""
    if context is None:
        context = getcontext()
    
    context.prec += 2
    t = sin(x, context=context) / cos(x, context=context)
    context.prec -= 2
    return +t

#
# inverse trigonometric functions
#

def asin(x, context=None):
    """Return the arcsine of x in radians."""
    if abs(x) > 1:
        raise ValueError("Domain error: asin accepts -1 <= x <= 1")
    
    if context is None:
        context = getcontext()
    
    if x == -1:
        return pi(context=context) / -2
    elif x == 0:
        return D(0, context=context)
    elif x == 1:
        return pi(context=context) / 2
    
    return atan2(x, D.sqrt(1 - x ** 2), context=context)

def acos(x, context=None):
    """Return the arccosine of x in radians."""
    if abs(x) > 1:
        raise ValueError("Domain error: acos accepts -1 <= x <= 1")

    if context is None:
        context = getcontext()
    
    if x == 1:
        return D(0, context=context)
    else:
        PI = pi(context=context)
        if x == -1:
            return PI
        elif x == 0:
            return PI / 2
    
    return PI / 2 - atan2(x, sqrt(1 - x ** 2, context=context), context=context)

def atan(x, context=None):
    """Return the arctangent of x in radians."""
    if context is None:
        context = getcontext()

    c = None    
    if x == 0:
        return D(0, context=context)
    elif abs(x) > 1:
        PI = pi(context=context)
        x_is_inf = x._isinfinity()
        if x_is_inf:
            return PI / D((x._sign, (2,), 0), context=context)
        else:
            c = PI / D((x._sign, (2,), 0), context=context)
            x = 1 / x
    
    context.prec += 2
    x_squared = x ** 2
    y = x_squared / (1 + x_squared)
    y_over_x = y / x
    i = D(0); lasts = 0; s = y_over_x; coeff = 1; num = y_over_x
    while s != lasts:
        lasts = s 
        i += 2
        coeff *= i / (i + 1)
        num *= y
        s += coeff * num
    if c:
        s = c - s
    context.prec -= 2
    return +s

def atan2(y, x, context=None):
    """Return the arctangent of y/x in radians.
    
    Unlike atan(y/x), the signs of both x and y are considered.
    
    """
# TODO check the sign function make sure this still works
# decimal zero has a sign
    abs_y = abs(y)
    abs_x = abs(x)
    y_is_real = not x._isinfinity()
    
    if x != 0:
        if y_is_real:
            a = y and atan(y / x, context=context) or D(0)
            if x < 0:
                a += D((y._sign, (1,), 0)) * pi(context=context)
            return a
        elif abs_y == abs_x:
            x = D((x._sign, (1,), 0))
            y = D((y._sign, (1,), 0))
            return pi(context=context) * (2 - x) / (4 * y)

    if y != 0:
        return atan(D((y._sign, (0,), 'F')))
    elif x < 0:
        return D((y._sign, (1,), 0)) * pi()
    else:
        return D(0)

#
# hyperbolic trigonometric functions
#

def sinh(x):
    """Return the hyperbolic sine of x."""
    if x == 0:
        return D(0)
    
    # Uses the taylor series expansion of sinh, see:
    # http://en.wikipedia.org/wiki/Hyperbolic_function#Taylor_series_expressions
    getcontext().prec += 2
    i, lasts, s, fact, num = 1, 0, x, 1, x
    while s != lasts:
        lasts = s
        i += 2
        num *= x * x
        fact *= i * (i - 1)
        s += num / fact
    getcontext().prec -= 2
    return +s

def cosh(x):
    """Return the hyperbolic cosine of x."""
    if x == 0:
        return D(1)
    
    # Uses the taylor series expansion of cosh, see:
    # http://en.wikipedia.org/wiki/Hyperbolic_function#Taylor_series_expressions
    getcontext().prec += 2
    i, lasts, s, fact, num = 0, 0, 1, 1, 1
    while s != lasts:
        lasts = s
        i += 2
        num *= x * x
        fact *= i * (i - 1)
        s += num / fact
    getcontext().prec -= 2
    return +s

def tanh(x):
    """Return the hyperbolic tangent of x."""
    return +(sinh(x) / cosh(x))

#
# miscellaneous functions
#

def sgn(x):
    """Return -1 for negative numbers, 1 for positive numbers and 0 for zero."""
    # the signum function, see:
    # http://en.wikipedia.org/wiki/Sign_function
    if x > 0:
        return D(1)
    elif x < 0:
        return D(-1)
    else:
        return D(0)

def degrees(x):
    """Return angle x converted from radians to degrees."""
    return x * 180 / pi()

def radians(x):
    """Return angle x converted from degrees to radians."""
    return x * pi() / 180

def ceil(x):
    """Return the smallest integral value >= x."""
    return x.to_integral(rounding=decimal.ROUND_CEILING)

def floor(x):
    """Return the largest integral value <= x."""
    return x.to_integral(rounding=decimal.ROUND_FLOOR)

def hypot(x, y):
    """Return the Euclidean distance, sqrt(x**2 + y**2)."""
    return sqrt(x * x + y * y)

def modf(x):
    """Return the fractional and integer parts of x."""
    int_part = x.to_integral(rounding=decimal.ROUND_FLOOR)
    frac_part = x-int_part
    return frac_part,int_part

def ldexp(s, e):
    """Return s*(10**e), the value of a decimal floating point number with
    significand s and exponent e.
    
    This function is the inverse of frexp.  Note that this is different from
    math.ldexp, which uses 2**e instead of 10**e.
    
    """
    return s*(10**e)

def frexp(x):
    """Return s and e where s*(10**e) == x.
    
    s and e are the significand and exponent, respectively of x.    
    This function is the inverse of ldexp.  Note that this is different from
    math.frexp, which uses 2**e instead of 10**e.
    
    """
    e = D(x.adjusted())
    s = D(10)**(-x.adjusted())*x
    return s, e

def pow(x, y, context=None):
    """Returns x**y (x to the power of y).
    
    x cannot be negative if y is fractional.
    
    """
    context, x, y = _initialize(context, x, y)
    # if y is an integer, just call regular pow
    if y._isinteger():
        return x**y
    # if x is negative, the result is complex
    if x < 0:
        return context._raise_error(decimal.InvalidOperation, 'x (negative) ** y (fractional)')
    return exp(y * log(x))

def tetrate(x, y, context=None):
    """Return x recursively raised to the power of x, y times. ;)
    
    y must be a natural number.
    
    """
    context, x, y = _initialize(context, x, y)

    if not y._isinteger():
        return context._raise_error(decimal.InvalidOperation, 'x *** (non-integer)')

    def _tetrate(x,y):
        if y == -1:
            return D(-1)
        if y == 0:
            return D(1)
        if y == 1:
            return x
        return x**_tetrate(x,y-1)

    return _tetrate(x,y)

#
# internal functions
#
def _initialize(context, *args):
    if context is None:
        context = getcontext()
    
    r = [context]
    for arg in args:
# TODO should something else be seeing NotImplemented?
        e = _convert_other(arg)
        if e is NotImplemented:
            raise TypeError("unsupported operand type: '%s'" \
                            "(if it's a float, try the float_to_decimal function)" % (type(e).__name__,))
        r.append(e)
    
    return r

def _sign(x):
    """Return -1 for negative numbers and 1 for positive numbers."""
    # brian's sign function
    if x._sign == 0:
        return D(1)
    else:
        return D(-1)


sqrt = D.sqrt
fabs = abs
fmod = D.__mod__

__all__ = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees',
           'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'golden_ratio',
           'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians',
           'sgn', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tetrate']

if __name__ == '__main__':
    # TODO put some test functions down here
    pass

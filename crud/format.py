import numpy

"""
Number formatting utilities

Formatting strings: A combination of a character that determines the 
style and a number determining the decimal precision

Styles:
    f    Float
    i    Integer         Same as "f0"
    n    Number          Number format adds a separator between thousands
    k    Thousands
    m    Millions
    b    Billions
    t    Trillions
    p    Percentage
    x    Basis points
    e    Scientific

For example the string 'm2' would convert the number 12,345,678 into 
the string "12.36m"
"""

# Format constants
NUMBER = 'n'
THOUSANDS = 'k'
MILLIONS = 'm'
BILLIONS = 'b'
TRILLIONS = 't'
PERCENTAGE = 'p'
BASIS_POINTS = 'x'
FLOAT = 'f'
SCIENTIFIC = 'e'
INTEGER = 'i'


def decode_format(number_format):
    """
    Convert style string to format string ('{}' style), suffix and value scale
    
    This is the core function used to convert numbers to strings
    """

    style = number_format[0]
    prec = "." + str(int(number_format[1:])) if len(number_format) > 1 else ""

    if style == NUMBER:
        return "," + prec + "g","",1.

    elif style == THOUSANDS:
        return "," + prec + "g","k",1e-3

    elif style == MILLIONS:
        return "," + prec + "g","m",1e-6

    elif style == BILLIONS:
        return "," + prec + "g","bn",1e-9

    elif style == TRILLIONS:
        return "," + prec + "g","tr",1e-12

    elif style == PERCENTAGE:
        return prec + "f","%",1e2

    elif style == BASIS_POINTS:
        return prec + "f","bp",1e4

    elif style == INTEGER:
        return "d","",1.

    elif style == SCIENTIFIC:
        return ".4e","",1.

    else: # style FLOAT
        return prec + "f","",1.



def format_value(value,number_format):
    "Convert number to string using a style string"

    style,sufix,scale = decode_format(number_format)
    fmt = "{0:" + style + "}" + sufix

    return fmt.format(scale * value)
    


def auto_number_format(data):
    top = bot = data
    while isinstance(top,(list,tuple,numpy.ndarray)): top = max(top)
    while isinstance(bot,(list,tuple,numpy.ndarray)): bot = min(bot)
    top = abs(top)
    bot = abs(bot)
    
    if top < 0.4 and bot < 0.4: # assume it is rate-like, hence percentage
        return "p" # percentage

    elif top > 1e15:
        return "e" # scientific

    elif top > 1e12:
        return "t" # trillion

    elif top > 1e9:
        return "b" # billion

    elif top > 1e6:
        return "m" # million

    elif top > 1e4:
        return "k" # thousands

    else:
        avg = (top + bot) / 2.
        prec = 3 - int(numpy.log10(avg))
        return "f{0}".format(prec)      



def auto_precision(value):
    """Return a preferred number of decimal points, based on value"""
    return 3 - int(numpy.log10(abs(value)))

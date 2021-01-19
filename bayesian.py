import pandas as pd
import numpy as np
import scipy.stats as stats
import re
from flask import g


def inverse(var, values):
    values['not_' + var] = 1 - values[var]

def demorgans(var, values):
    if 'and' in var:
        x = [i.start() for i in re.finditer('not', var)]
        if not x: # b_and_a
            values['not_b_or_not_a'] = 1 - values[var]
        elif len(x) == 2: # not_b_and_not_a
            values['b_or_a'] = 1 - values[var]
        elif x[0] == 0: # not_b_and_a
            values['b_or_not_a'] = values[var]
        else: # b_and_not_a
            values['not_b_or_a'] = 1 - values[var]
    elif 'or' in var:
        x = [i.start() for i in re.finditer('not', var)]
        if not x: # b_or_a
            values['not_b_and_not_a'] = 1 - values[var]
        elif len(x) == 2: # not_b_or_not_a
            values['b_and_a'] = 1 - values[var]
        elif x[0] == 0: # not_b_or_a
            values['b_and_not_a'] = values[var]
        else: # b_or_not_a
            values['not_b_and_a'] = 1 - values[var]

def calculate(a, bga, bgna):
    print(a, bga, bgna)
    values = {
        'a': float(a),
        'b_given_a': float(bga),
        'b_given_not_a': float(bgna)
    }

    # inverse
    inverse('a', values)
    inverse('b_given_a', values)
    inverse('b_given_not_a', values)

    # and 
    values['b_and_a'] = values['b_given_a'] * values['a']
    values['not_b_and_a'] = values['not_b_given_a'] * values['a']
    values['b_and_not_a'] = values['b_given_not_a'] * values['not_a']
    values['not_b_and_not_a'] = values['not_b_given_not_a'] * values['not_a']

    # b
    values['b'] = values['b_given_a'] * values['a'] + values['b_given_not_a'] * values['not_a']
    inverse('b', values)

    # a given b
    values['a_given_b'] = values['b_and_a'] / values['b']
    values['not_a_given_b'] = values['b_and_not_a'] / values['b']
    values['a_given_not_b'] = values['not_b_and_a'] / values['not_b']
    values['not_a_given_not_b'] = values['not_b_and_not_a'] / values['not_b']

    # or
    # values['b_or_a'] = values['b'] + values['a'] - values['b_and_a']
    # values['not_b_or_a'] = values['not_b'] + values['a'] - values['not_b_and_a']
    # values['b_or_not_a'] = values['b'] + values['not_a'] - values['b_and_not_a']
    # values['not_b_or_not_a'] = values['not_b'] + values['not_a'] - values['not_b_and_not_a']
    demorgans('b_and_a', values)
    demorgans('not_b_and_a', values)
    demorgans('b_and_not_a', values)
    demorgans('not_b_and_not_a', values)
    values = {k: round(v, 3) for k,v in values.items()}

    return values


# ---------------------------------------

# import pandas as pd
# import numpy as np
# import scipy.stats as stats
# import re
# from flask import g


# def inverse(var, values):
#     values['not_' + var] = 1 - values[var]

# def demorgans(var, values):
#     if 'and' in var:
#         x = [i.start() for i in re.finditer('not', var)]
#         if not x: # b_and_a
#             values['not_b_or_not_a'] = 1 - values[var]
#         elif len(x) == 2: # not_b_and_not_a
#             values['b_or_a'] = 1 - values[var]
#         elif x[0] == 0: # not_b_and_a
#             values['b_or_not_a'] = values[var]
#         else: # b_and_not_a
#             values['not_b_or_a'] = 1 - values[var]
#     elif 'or' in var:
#         x = [i.start() for i in re.finditer('not', var)]
#         if not x: # b_or_a
#             values['not_b_and_not_a'] = 1 - values[var]
#         elif len(x) == 2: # not_b_or_not_a
#             values['b_and_a'] = 1 - values[var]
#         elif x[0] == 0: # not_b_or_a
#             values['b_and_not_a'] = values[var]
#         else: # b_or_not_a
#             values['not_b_and_a'] = 1 - values[var]


            

# def calculate(a, bga, bgna):
#     print(a, bga, bgna)
#     values = {
#         'a': float(a),
#         'b_given_a': float(bga),
#         'b': float(bgna)
#     }

#     # inverse
#     inverse('a', values)
#     inverse('b_given_a', values)
#     inverse('b', values)

#     values['b_and_a'] = values['b_given_a'] * values['a']
#     values['not_b_and_a'] = values['not_b_given_a'] * values['a']

#     values['a_given_not_b'] = values['not_b_and_a'] / values['not_b']
#     inverse('a_given_not_b', values)




#     values['b_and_not_a'] = values['b_given_not_a'] * values['not_a']
#     values['not_b_and_not_a'] = values['not_b_given_not_a'] * values['not_a']

#     # b
#     values['b'] = values['b_given_a'] * values['a'] + values['b_given_not_a'] * values['not_a']
#     inverse('b', values)

#     # a given b

#     values['not_a_given_b'] = values['b_and_not_a'] / values['b']



#     # or
#     values['b_or_a'] = values['b'] + values['a'] - values['b_and_a']
#     values['not_b_or_a'] = values['not_b'] + values['a'] - values['not_b_and_a']
#     values['b_or_not_a'] = values['b'] + values['not_a'] - values['b_and_not_a']
#     values['not_b_or_not_a'] = values['not_b'] + values['not_a'] - values['not_b_and_not_a']

#     values = {k: round(v, 3) for k,v in values.items()}

#     return values




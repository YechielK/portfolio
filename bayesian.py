import pandas as pd
import numpy as np
import scipy.stats as stats
import re
from flask import g


def test(f):
    print(f)


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
            values['b_or_not_a'] = 1 - values[var]
        else: # b_and_not_a
            values['not_b_or_a'] = 1 - values[var]
    elif 'or' in var:
        x = [i.start() for i in re.finditer('not', var)]
        if not x: # b_or_a
            values['not_b_and_not_a'] = 1 - values[var]
        elif len(x) == 2: # not_b_or_not_a
            values['b_and_a'] = 1 - values[var]
        elif x[0] == 0: # not_b_or_a
            values['b_and_not_a'] = 1 - values[var]
        else: # b_or_not_a
            values['not_b_and_a'] = 1 - values[var]

def calculate(d):
    # print(a, bga, bgna)
    values = {key: float(value) for key, value in d.items()}



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

#-------------------------------------------------------

def i_inverse(d):

    # letters
    if 'a' in d and 'a`' not in d:
        d['a`'] = 1 - d['a']
    elif 'a`' in d and 'a' not in d:
        d['a'] = 1 - d['a`']
    
    if 'b' in d and 'b`' not in d:
        d['b`'] = 1 - d['b']
    elif 'b`' in d and 'b' not in d:
        d['b'] = 1 - d['b`']

    # b|a
    if 'b|a' in d and 'b`|a' not in d:
        d['b`|a'] = 1 - d['b|a']
    elif 'b`|a' in d and 'b|a' not in d:
        d['b|a'] = 1 - d['b`|a']
    
    # b|a`
    if 'b|a`' in d and 'b`|a`' not in d:
        d['b`|a`'] = 1 - d['b|a`']
    elif 'b`|a`' in d and 'b|a`' not in d:
        d['b|a`'] = 1 - d['b`|a`']

    # a|b
    if 'a|b' in d and 'a`|b' not in d:
        d['a`|b'] = 1 - d['a|b']
    elif 'a`|b' in d and 'a|b' not in d:
        d['a|b'] = 1 - d['a`|b']
    
    # a|b`
    if 'a|b`' in d and 'a`|b`' not in d:
        d['a`|b`'] = 1 - d['a|b`']
    elif 'a`|b`' in d and 'a|b`' not in d:
        d['a|b`'] = 1 - d['a`|b`']


def i_row(d):

    #  first row
    if 'a' in d and 'b|a' in d and not 'a^b' in d: 
        d['a^b'] = d['b|a'] * d['a']
    elif 'a' in d and 'a^b' in d and not 'b|a' in d:
        d['b|a'] = d['a^b'] / d['a']
    elif 'b|a' in d and 'a^b' in d and not 'a' in d:
        d['a'] = d['a^b'] / d['b|a']
    
    # second row
    if 'b' in d and 'a`|b' in d and not 'b^a`' in d:
        d['b^a`'] = d['a`|b'] * d['b']
    elif 'b' in d and 'b^a`' in d and not 'a`|b' in d:
        d['a`|b'] = d['b^a`'] / d['b']
    elif 'a|b' in d and 'b^a`' in d and not 'b' in d:
        d['b'] = d['b^a`'] / d['a|b']

    #  third row
    if 'a`' in d and '`b|a`' in d and not 'a`^b`' in d: 
        d['a`^b`'] = d['`b|a`'] * d['a`']
    elif 'a`' in d and 'a`^b`' in d and not 'b|a`' in d:
        d['b|a`'] = d['a`^b`'] / d['a`']
    elif 'b|a`' in d and 'a`^b`' in d and not 'a`' in d:
        d['a`'] = d['a`^b`'] / d['b|a`']

    # fourth row
    if 'b`' in d and 'a|b`' in d and not 'b`^a' in d:
        d['b`^a'] = d['a|b`'] * d['b`']
    elif 'b`' in d and 'b`^a' in d and not 'a|b`' in d:
        d['a|b`'] = d['b`^a'] / d['b`']
    elif 'a|b`' in d and 'b`^a' in d and not 'b`' in d:
        d['b`'] = d['b`^a'] / d['a|b`']

        # or ('a' and 'a^b') or ('b|a' and 'a^b'):

def i_corner(d):

    # first corner
    if 'a' in d and 'b|a' in d and not 'a^b' in d:
        d['a^b'] = d['b|a'] * d['a']
    if 'a' in d and 'b`|a' in d and not 'b`^a' in d:
        d['b`^a'] = d['b`|a'] * d['a']

    # third corner
    if 'a`' in d and 'b|a`' in d and not 'b^a`' in d:
        d['b^a`'] = d['b|a`'] * d['a`']
    if 'a`' in d and 'b`|a`' in d and not 'a`^b`' in d:
        d['a`^b`'] = d['b`|a`'] * d['a`']

    # second corner 
    if 'b' in d and 'a|b' in d and not 'a^b' in d:
        d['a^b'] = d['a|b'] * d['b']
    if 'b' in d and 'a`|b' in d and not 'b^a`':
        d['b^a`'] = d['a`|b'] * d['b']
    
    # fourth corner
    if 'b`' in d and 'a|b`' in d and not 'b`^a' in d:
        d['b`^a'] = d['a|b`'] * d['b`']
    if 'b`' in d and 'a`|b`' in d and not 'a`^b`' in d:
        d['a`^b`'] = d['a`|b`'] * d['b`']

def i_get_letter(d):
    
    # first corner
    if 'b`^a' in d and 'a^b' in d and not 'a' in d:
        d['a'] = d['b`^a'] + d['a^b']
    # second corner
    if 'a^b' in d and 'b^a`' in d and not 'b' in d:
        d['b'] = d['a^b'] + d['b^a`']
    # third corner
    if 'b^a`' in d and 'a`^b`' in d and not 'a`' in d:
        d['a`'] = d['b^a`'] + d['a`^b`']
    # fourth corner
    if 'a`^b`' in d and 'b`^a' in d and not 'b`' in d:
        d['b`'] = d['a`^b`'] + d['b`^a']

def i_get_given(d):

    # first corner
    if 'a^b' in d and 'b' in d and not 'a|b' in d:
        d['a|b'] = d['a^b'] / d['b']
    
    # second corner
    if 'b^a`' in d and 'a`' in d and not 'b|a`' in d:
        d['b|a`'] = d['b^a`'] / d['a`']
    
    # third corner
    if 'a`^b`' in d and 'b`' in d and not 'a`|b`' in d:
        d['a`|b`'] = d['a`^b`'] / d['b`']
    
    # fourth corner
    if 'b`^a' in d and 'a' in d and not 'b`|a' in d:
        d['b`|a'] = d['b`^a'] / d['a']

def i_demorgans(d):

    # first
    if 'a^b' in d and not 'a`||b`' in d:
        d['a`||b`'] = 1 - d['a^b']
    elif 'a`||b`' in d and not 'a^b' in d:
        d['a^b'] = 1 - d['a`||b`']
    
    # second 
    if 'b^a`' in d and not 'b`||a' in d:
        d['b`||a'] = 1 - d['b^a`']
    elif 'b`||a' in d and not 'b^a`' in d:
        d['b^a`'] = 1 - d['b`||a']

    # third
    if 'a`^b`' in d and not 'a||b' in d:
        d['a||b'] = 1 - d['a`^b`']
    elif 'a||b' in d and not 'a`^b`' in d:
        d['a`^b`'] = 1 - d['a||b']

    # fourth
    if 'b`^a' in d and not 'b||a`' in d:
        d['b||a`'] = 1 - d['b`^a']
    elif 'b||a`' in d and not 'b`^a' in d:
        d['b`^a'] = 1 - d['b||a`'] 





def i_calculate(d):

    d = {key: round(float(value), 3) for key, value in d.items() if value}

    for i in range(3):
        i_demorgans(d)
        i_inverse(d)
        i_row(d)
        i_corner(d)
        i_get_letter(d)
        i_row(d)
        i_get_given(d)
        i_demorgans(d)
    # print('three', d)
    values = {k: round(v, 3) for k,v in d.items()}
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




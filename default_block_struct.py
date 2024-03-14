from copy import copy
print_struct = [
    [("text","print"),("para",None)],
    ("code","print"),
    ("bracket","("),
    ("arg",[]),
    ("adsb",','),
    ("bracket",")")
]

data_struct = [
    [("text","data")],
    ("data",None)
]

assign_struct = [
    [("para",None),("text","="),("para",None)],
    ("arg",None),
    ("code","="),
    ("arg",None)
]

add_by_struct = [
    [("para",None),("text","+="),("para",None)],
    ("arg",None),
    ("code","+="),
    ("arg",None)
]

minus_by_struct = [
    ("arg", None),
    ("code", "-="),
    ("arg", None)
]

multiply_by_struct = [
    ("arg", None),
    ("code", "*="),
    ("arg", None)
]

subtract_by_struct = [
    ("arg", None),
    ("code", "/="),
    ("arg", None)
]

add_struct = [
    [("para",None),("text","+"),("para",None)],
    ("bracket","("),
    ("arg", None),
    ("adsb"," "),
    ("code", "+"),
    ("arg", None),
    ("adsb"," "),
    ("bracket",")")
]

minus_struct = [
    ("bracket", "("),
    ("arg", None),
    ("code", "-"),
    ("arg", None),
    ("bracket", ")")
]

multiply_struct =[
    "bracket", "(",
    "arg", None,
    "code", "*",
    "arg", None,
    "bracket", ")"
]

subtract_struct = [
    "bracket", "(",
    "arg", None,
    "code", "/",
    "arg", None,
    "bracket", ")"
]

codi_euqal = [
    "arg",None,
    "code","==",
    "arg",None
]

codi_greater = [
    "arg",None,
    "code",">",
    "arg",None
]

codi_less_than = [
    "arg",None,
    "code","<",
    "arg",None
]

codi_greater_equal=[
    "arg",None,
    "code",">=",
    "arg",None
]
codi_less_than_equal = [
    "arg",None,
    "code","<=",
    "arg",None
]

codi_or = [
    "arg",None,
    "adsb"," ",
    "code","or",
    "adsb"," ",
    "arg",None
]

codi_and = [
    "arg",None,
    "adsb"," ",
    "code","and",
    "adsb"," ",
    "arg",None
]
codi_not = [
    "code", "not",
    "adsb", " ",
    "arg", None
]

codi_diff = [
    "arg",None,
    "adsb"," ",
    "code","!=",
    "adsb"," ",
    "arg",None
]

if_struct = [
    "code","if",
    "adsb"," ",
    "arg",[],
    "adsb"," ",
    "end",","
]

for_struct = [
    "code","for",
    "adsb"," ",
    "arg",[],
    "adsb",",",
    "code","in",
    "adsb"," ",
    "arg",None,
    "end",","
]
while_struct = [
    "code","while",
    "adsb"," ",
    "arg",None,
    "end",","
]

def_struct = [
    "code","def",
    "adsb"," ",
    "bracket","(",
    "arg",[],
    "adsb",",",
    "bracket",")",
    "end",","
]

def side_block_struct_load(mode = 1):
    if mode == 1:
        side_block_struct = [
            "adsb",".",
            "name",None
        ]
    else:
        side_block_struct = [
            "adsb",".",
            "name",None,
            "bracket","(",
            "arg",[],
            "adsb",",",
            "bracket",")"
        ]
    return side_block_struct

else_struct = [
    "code","else",
    "end",","
]

elif_struct = [
    "code","elif",
    "adsb"," ",
    "arg",[],
    "adsb"," ",
    "end",","
]

func_struct = [
    "name",None,
    "bracket","(",
    "arg",[],
    "adsb",",",
    "bracket",")"
]

return_struct = [
    "code","return",
    "adsb"," ",
    "arg",[],
    "adsb",","
]
var_struct = [
    "name",None
]

arr_struct = [
    "bracket","[",
    "arg",[],
    "adsb",",",
    "bracket","]"
]

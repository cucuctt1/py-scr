struct = {
    "style":[],
    "color":"",
    "text color":"",
    "block type":"",
    "block_name":"",
    "block setting":[],
    "struct":[]
}
import random_req as rr
import json_process
import os
dir = "../default_block/"




def write_function(data):

    file_name = rr.generate_random_string(10)
    #anti small case
    while os.path.exists(dir+file_name+".json_process"):
        file_name = rr.generate_random_string(10)
    file_dir = dir+file_name+".json_process"
    directory = os.path.dirname(file_dir)
    os.makedirs(directory, exist_ok=True)
    with open(file_dir, 'w'):
        pass
    with open(dir+file_name+".json_process","w") as file:
        json_process.dump(data, file)
def create_struct(style = list(),
                  color="",
                  text_color = "",
                  block_type=""
                  ,block_setting=list(),
                  struct = list(),
                  block_name = ""):
    arg_data = []
    arg = locals()
    for item in arg:
        if item !='arg_data':
            arg_data.append((item,arg[item]))
    block_struct = {}
    for item in arg_data:
        arg_name,arg_value = item
        block_struct[arg_name] = arg_value
    return block_struct

def struct_gennerate(block_name:str,block_function:str,Npara=1,args=False,bgcolor="",textcolor="",*setting):
    style = [("text",block_name)]
    for i in range(Npara):
        style.append(("para",None))
    color = bgcolor
    textcolor = textcolor
    block_setting = list()
    block_type = "custom"
    for item in setting:
        block_setting.append(item)
    struct = [("code",block_function),("bracket","("),("arg",[]),("adsb"," "),("bracket",")")]

    gennerated_struct = create_struct(style=style,color=color,text_color=textcolor,block_type=block_type,block_setting=block_setting,struct=struct,block_name=block_name)

    write_function(gennerated_struct)

struct_gennerate("print","print",1,bgcolor="#BBBBBB",textcolor="#000000")


import blocklogic as b
import flet as ft
import default_block_struct as dbs
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def add_print(stack):
    data = b.block(x=190, y=190, color=ft.colors.GREY, content=None, code_container=stack, id="level 3 block",struct = dbs.print_struct,have_parameter=True,Npara=1,code="print",args=True)
    stack.controls.append(data)
    del data
    stack.update()

def add_data(stack):
    random_data = generate_random_string(10)
    data = b.block( x=235, y=65, color=ft.colors.GREEN, content=None, code_container=stack, id="level 1 block",code=random_data,struct=dbs.data_struct,Npara=1)
    stack.controls.append(data)
    del data
    stack.update()

def add_add(stack):
    data = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",have_parameter=True,Npara=2,struct=dbs.add_struct)
    stack.controls.append(data)
    del data
    stack.update()

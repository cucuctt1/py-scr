import flet as ft
import stack as st
import blocklogic as b
import start_parse as sp
import block_manage as bm
import page_intermediate as pi
from shortcut import shortcut as sc
import global_control as gc
from class_func import class_display as cd
from utility.color_palette import *
from savefunc import read_function as rf
class free_move(ft.GestureDetector):
    def __init__(self,main_target):
        super().__init__()
        self.on_pan_update =self.move
        self.main = main_target

    def move(self,e:ft.DragUpdateEvent):
        for item in self.main.controls:
            if not item.upper_code:
                item.move(e.delta_x,e.delta_y)
        self.main.update()

def das(stack):
    gc.class_buffer = []
    gc.class_method_buffer = {}
    data = rf.load_to_block("myfile.txt")
    for n,item in enumerate(data):
        data[n].code_container = stack
    stack.controls = data

    stack.update()

def main(page:ft.Page):
    page.window_maximized=False

    #stack.add_block(block=card2)
    #stack.add_block(block=card3)
    #stack = st.stack_buffer()
    con = ft.Container(width=30,bgcolor="BLACK")
    side = cd.class_display(wid=300, hei=page.height, page=page, display_layer=gc.global_playground,bgcolor = white_2)
    gc.globals_class_manager = side
    r = ft.Row([gc.globals_class_manager])
    start_btn = ft.FilledButton(text="start",width=100,height=30,on_click=lambda e:sp.start_parse(gc.global_playground))

    add_print = ft.FilledButton(text="add print",width=150,height=30,on_click=lambda e:bm.add_print(gc.global_playground,page))
    add_data = ft.FilledButton(text="data",width=150,height=30,on_click=lambda e:bm.add_variable(gc.global_playground))
    add_add = ft.FilledButton(text="add",width=150,height=30,on_click=lambda e:bm.add_add(gc.global_playground))
    add_assign = ft.FilledButton(text="assign", width=150, height=30, on_click=lambda e: bm.add_assign(gc.global_playground))
    add_def = ft.FilledButton(text="def", width=150, height=30, on_click=lambda e: bm.add_def(gc.global_playground))
    add_for = ft.FilledButton(text="for", width=150, height=30, on_click=lambda e: bm.add_for(gc.global_playground))
    add_if = ft.FilledButton(text="if", width=150, height=30, on_click=lambda e: bm.add_if(gc.global_playground))
    add_class = ft.FilledButton(text="class", width=150, height=30, on_click=lambda e: bm.add_class(gc.global_playground))
    star = ft.FilledButton(text="start2", width=100, height=30, on_click=lambda e: das(gc.global_playground))
    btn_holder = ft.Row(controls=[add_print,add_add,add_data,add_assign,add_def,add_for,start_btn,star,add_if,add_class],spacing=10,wrap=True)
    block2 = b.block(isheader=True,x=30, y=30, color=ft.colors.RED, content=None, code_container=gc.global_playground,id=1)
    #stack.add_block(block2)
    gc.global_playground.add_block(block2)
    stack2 = st.stack_buffer()

    pi.set_page(page)
    stack2.add_block(btn_holder)
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.add(r)
    free = free_move(gc.global_playground)
    page.overlay.append(free)
    page.overlay.append(gc.global_playground)
    page.on_keyboard_event = sc.keyboard_listener
    page.add(stack2)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
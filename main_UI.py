from UIs.vertical_tab import vertical_tab as vt
from UIs import block_display as bd
from load_default import load_normal as ln , load_def as ld,load_class as lc,load_misc as lm,load_python as lp,load_condition as lco,load_container as lcon
from json_process import *
from class_func import class_display as cd
from utility.color_palette import *
from savefunc import read_function as rf
import flet as ft
import blocklogic as b
import start_parse as sp
import page_intermediate as pi
import global_control as gc
from json_process import json_reader as jsrd
from variable import variable_create_ui as vcui
import os
from utility.auto_para import *
from function_UI import func_display as fd
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

# global_func = None
# global_page = None
def update_func():
    pass
def load(page,stack):
    sub_layout1 = ft.Container(width=300, bgcolor="RED", height=page.window_height)
    block_display1 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    block_display1.height = page.window_height
    ln.load(ln.block_dir_list, block_display1, stack, page)
    block_display1.set_display_block(block_display1.block_buffer)

    block_display2 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lcon.load(lcon.block_dir_list, block_display2, stack, page)
    block_display2.set_display_block(block_display2.block_buffer)

    block_display3 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    ld.load(ld.block_dir_list, block_display3, stack, page)
    block_display3.set_display_block(block_display3.block_buffer)
    global_func = block_display3
    block_display4 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lc.load(lc.block_dir_list, block_display4, stack, page)
    block_display4.set_display_block(block_display4.block_buffer)

    block_display5 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lco.load(lco.block_dir_list, block_display5, stack, page)
    block_display5.set_display_block(block_display5.block_buffer)

    block_display6 = cd.class_display(wid=300 - 40, page=page, hei=page.window_height, display_layer=stack,
                                      bgcolor=white)
    block_display6.border = ft.border.all(1, white_3)
    block_display6.border_radius = ft.border_radius.all(5)
    gc.globals_class_manager = block_display6

    tabs = [vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.WIDTH_NORMAL_OUTLINED)), content=block_display1),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.DATASET)), content=block_display2),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.PALLET)), content=block_display3),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_OUTLINED)), content=block_display4),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CONFIRMATION_NUM_OUTLINED)), content=block_display5),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_)), content=block_display6)]
    vertical_drawer = vt.vertical_tab(tab_color=white_3, select_color=accept_col, render_color=white_2,
                                      wid=300, tab_wid=40, select_index=1,
                                      tabs=tabs)
    sub_layout1.content = vertical_drawer
    sub_layout2 = ft.Column([])
    bot_layout = ft.Row([sub_layout1, sub_layout2])

    save_btn = ft.ElevatedButton(text="save", width=100)
    open_btn = ft.ElevatedButton(text="open", width=100)
    export_btn = ft.ElevatedButton(text="export", width=100)

    run_btn = ft.ElevatedButton(text="run", width=100)  # icon

    left = ft.Row([save_btn, open_btn, export_btn])
    main_top_layout = ft.Row([left, run_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    top_layout = ft.Container(height=40, width=page.width, bgcolor=tab_white, content=main_top_layout,
                              padding=ft.padding.only(left=20, right=20),
                              border=ft.border.all(1, white_3))

    main_layout = ft.Column([top_layout, bot_layout], spacing=0)
    return main_layout
def main(page=gc.global_page):

    global global_func,global_page
    gc.global_page = page
    global_page = page
    page.window_maximized = True
    page.padding = ft.padding.all(0)
    print(page.window_max_height)
    stack = gc.global_playground
    stack.height = 1200
    pi.set_page(page)

    #stack.height = page.height*0.65

    #recalculate cord
    def run(e):
        code = sp.get_code(stack)
        with open("temp.py","w") as f:
            f.write(code)

        os.system("start cmd /K python temp.py")


    sub_layout1 = ft.Container(width=300, bgcolor="RED", height=page.window_height)
    block_display1 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    block_display1.height = page.window_height
    ln.load(ln.block_dir_list, block_display1, stack, page)
    block_display1.set_display_block(block_display1.block_buffer)

    block_display2 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lcon.load(lcon.block_dir_list, block_display2, stack, page)
    block_display2.set_display_block(block_display2.block_buffer)

    #block_display3 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    #fd.load_func_buffer(gc.local_CF_buffer,block_display3,page = page,top_layer=stack)
    #block_display3.set_display_block(block_display3.block_buffer)

    block_display3 = gc.global_func_display
    block_display3.page = page
    block_display3.height = page.window_height
    block_display3.main_content.page = page
    block_display3.content.page = page

    block_display4 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lc.load(lc.block_dir_list, block_display4, stack, page)
    block_display4.set_display_block(block_display4.block_buffer)

    block_display5 = bd.Display_container(wid=300 - 40, page=page, hei=page.window_height)
    lco.load(lco.block_dir_list, block_display5, stack, page)
    block_display5.set_display_block(block_display5.block_buffer)

    block_display6 = cd.class_display(wid=300 - 40, page=page, hei=page.window_height, display_layer=stack,
                                      bgcolor=white)
    block_display6.border = ft.border.all(1, white_3)
    block_display6.border_radius = ft.border_radius.all(5)
    gc.globals_class_manager = block_display6

    block_display7 = vcui.variable_container(wid=300-40,page=page,parent=stack,hei=page.window_height)
    #icons.PIX variable create
    #icons.EXTENSION
    #icons.ALL_INBOX
    tabs = [vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.WIDTH_NORMAL_OUTLINED)), content=block_display1),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.DATASET)), content=block_display2),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.PALLET)), content=block_display3),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_OUTLINED)), content=block_display4),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CONFIRMATION_NUM_OUTLINED)), content=block_display5),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.CLASS_)), content=block_display6),
            vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.PIX )), content=block_display7)]
    vertical_drawer = vt.vertical_tab(tab_color=white_3, select_color=accept_col, render_color=white_2,
                                      wid=300, tab_wid=40, select_index=1,
                                      tabs=tabs)
    sub_layout1.content = vertical_drawer
    sub_layout2 = ft.Column([])
    bot_layout = ft.Row([sub_layout1, sub_layout2])

    save_btn = ft.ElevatedButton(text="save", width=100)
    open_btn = ft.ElevatedButton(text="open", width=100)
    export_btn = ft.ElevatedButton(text="export", width=100)

    run_btn = ft.ElevatedButton(text="run", width=100,on_click=run)  # icon

    left = ft.Row([save_btn, open_btn, export_btn])
    main_top_layout = ft.Row([left, run_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    top_layout = ft.Container(height=40, width=page.width, bgcolor=tab_white, content=main_top_layout,
                              padding=ft.padding.only(left=20, right=20),
                              border=ft.border.all(1, white_3))

    main_layout = ft.Column([top_layout, bot_layout], spacing=0)

    def layout_manage(e):
        stack.interact(None,None,2)
        sub_layout1.height = e.control.window_height
        block_display1.height = e.control.window_height
        block_display2.height = e.control.window_height
        block_display3.height = e.control.window_height
        block_display4.height = e.control.window_height
        block_display5.height = e.control.window_height
        block_display6.height = e.control.window_height
        vertical_drawer.height = e.control.window_height
        block_display7.height = e.control.window_height
        main_layout.update()
        bot_layout.update()
        vertical_drawer.update()
        e.control.update()
        page.update()
    header = b.block(x=500,y=300,isheader=True,struct=jsrd.read_json("./header.json"),code_container=stack)
    stack.add_block(header)
    #page.on_window_event = layout_manage
    page.on_resize = layout_manage
    free = free_move(stack)

    page.update()
    page.add(main_layout)
    page.overlay.append(free)
    page.overlay.append(stack)

    page.update()

def add_to_def(id):
    global global_func, global_page
    print(global_func,global_page)
    CF_dir = "./CF_store/"
    filename = id+".json"
    file_dir = CF_dir+filename
    slot = bd.display_slot(wid=250,hei=40,page=global_page,top_layer=gc.global_playground)
    struct = jsrd.read_json(file_dir)
    block = b.block(x=0,y=0,struct=struct,Npara=auto_para(struct),have_parameter=True)
    slot.change_block(block)
    global_func.add_block(slot)
    global_func.set_display_block(global_func.block_buffer)
    global_page.update()
if __name__ == "__main__":
    ft.app(target=main)
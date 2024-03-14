import threading
import time

import flet as ft
from utility.color_palette import *
import blocklogic as b
from json_process import json_reader as jsrd
import copy as c
import pyautogui
import sys
from pynput.mouse import Listener, Button
import threading as t
dir2 = "../default_block/"
var_dir = dir2+"variable/variable.json"
dd = ft.GestureDetector
def click():
    pyautogui.mouseDown()

class stackd(ft.Stack):
    def __init__(self,page=None):
        super().__init__()
        self.page = page
    def interact(self, data,e):
        pass
top_layer = stackd()

class var_slot(ft.Stack):
    def __init__(self,wid,hei,page):
        super().__init__()
        self.height = hei
        self.width = wid
        self.page = page
    def add(self,data):
        self.width = data.block_width
        self.height = data.block_height
        data.top = (self.height-data.block_height)/2
        data.left =(self.width-data.block_width)/2

        self.controls.append(data)

    def interact(self,data,e):
        global top_layer
        new_block = c.deepcopy(data)
        data.top = e.global_y-e.local_y
        data.left = e.global_x-e.local_x
        new_block.code_container = self
        self.controls.remove(data)
        self.controls.append(new_block)
        data.code_container = top_layer
        top_layer.controls.append(data)
        self.page.update()

class variable_container(ft.Container):
    def __init__(self,wid,hei,page):
        super().__init__()
        self.width = wid
        self.height = hei
        self.page = page
        self.primary = white
        self.secondary =white_2
        self.outline = white_3
        self.bgcolor = self.primary
        self.choice_list = []
        self.input_section = ft.TextField(width=self.width,height=40,border_color=self.outline,label="variable name")
        self.accept_btn = ft.OutlinedButton(width=self.width,height=40,text="Create",on_click=self.create_new_var)
        self.variable_display = ft.ListView(expand=True,width=self.width,height=self.height,spacing=15,controls=[],on_scroll_interval=1,auto_scroll=True
                                       ,padding=ft.padding.only(left=0,bottom=2,right=20,top=10))

        self.display = ft.Container(height=self.height-40,width=self.width,content=self.variable_display,border_radius=ft.border_radius.all(10),border=ft.border.all(1,white_3))

        self.dell_button = ft.ElevatedButton(text="Delete",bgcolor="RED",color="WHITE",width=self.width,height=40)
        main_layout = ft.Column([self.input_section,self.accept_btn,self.display,self.dell_button])
        self.content = main_layout

    def create_new_var(self,e):
        if self.input_section.value:
            var = var_slot(wid=150, hei=40, page=self.page)
            data = b.block(x=0, y=0, content=None, code_container=var,
                            name=self.input_section.value, struct=jsrd.read_json(var_dir))
            var.add(data)

            checkbtn = ft.Checkbox(on_change=self.focus)
            self.choice_list.append((checkbtn,False))
            vertical_layout = ft.Row([checkbtn, var])

            self.variable_display.controls.append(vertical_layout)
            self.input_section.value = ""
            try:
                self.input_section.update()
                self.variable_display.update()
            except:
                pass


    def check_choice(self):
        count = 0
        for item in self.choice_list:
            tar,value = item
            if value:
                count+=1
        return count
    def find(self,data):
        for item,datas in enumerate(self.choice_list):
            if datas[0] == data:
                return item
        return -1
    def focus(self,e):
        index = self.find(e.control)
        self.choice_list[index] = (e.control,e.control.value)
        if self.check_choice() == 1:
            self.start_edit(index,e)
        else:
            self.input_section.value = ""
            self.input_section.update()
            self.accept_btn = ft.OutlinedButton(width=self.width, height=40, text="Create",
                                                on_click=self.create_new_var)
            self.content = ft.Column([self.input_section, self.accept_btn, self.display, self.dell_button])
            self.update()

    def start_edit(self,index,ed):
        data = self.variable_display.controls[index].controls[1].controls[0].name
        self.input_section.value = data
        try:
            self.input_section.focus()
            self.input_section.update()
        except:
            pass

        self.accept_btn = ft.OutlinedButton(width=self.width, height=40, text="Change",
                                            on_click=lambda e: self.confirm(index,ed))
        self.content  = ft.Column([self.input_section,self.accept_btn,self.display,self.dell_button])
        self.update()


    def confirm(self,index,ed):
        var = var_slot(wid=150, hei=40, page=self.page)
        data = b.block(x=0, y=0, content=None, code_container=var,
                       name=self.input_section.value, struct=jsrd.read_json(var_dir))
        var.add(data)
        checkbtn = ft.Checkbox(on_change=self.focus)
        vertical_layout = ft.Row([checkbtn, var])
        self.variable_display.controls[index] = vertical_layout
        self.input_section.value = ""
        self.accept_btn = ft.OutlinedButton(width=self.width,height=40,text="Create",on_click=self.create_new_var)
        self.content = ft.Column([self.input_section, self.accept_btn, self.display, self.dell_button])
        self.update()


def main(page:ft.Page):
    global top_layer
    top_layer.page = page
    page.window_maximized=False
    var = variable_container(wid=200,hei=page.height,page=page)
    page.overlay.append(top_layer)
    page.add(var)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
    sys.exit()
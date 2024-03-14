
import flet as ft
class stack_buffer(ft.Stack):
    def __init__(self,wid = 1000,hei =1000):
        super().__init__()
        self.controls = []
        self.height=500

    def add_block(self,block):
        self.controls.append(block)

    def interact(self,data,e):
        pass

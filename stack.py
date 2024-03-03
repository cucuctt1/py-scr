
import flet as ft
class stack_buffer(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.height=500

    def add_block(self,block):
        self.controls.append(block)

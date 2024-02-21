
import flet as ft
class stack_buffer(ft.Stack):
    def __init__(self):
        super().__init__()
        self.controls = []
    def add_block(self,block):
        self.controls.append(block)
    def update2(self):
        self.slot_update()
        self.block_form_update()
        self.update()

    def slot_update(self):
        for block in self.controls:
            self.next_slot_update(block)
    def next_slot_update(self,block):
        block.next_slot_y = block.block_height
        block.next_slot_x = 0
        for code in block.below_code:
            block.next_slot_y += code.block_height
        if block.IsContainer:
            block.next_slot_x_contain = block.offset1
            block.next_slot_y_contain = block.top_part
            block.next_slot_y = block.top_part+block.bot_part+20
            block.block_height = block.top_part+block.bot_part + 20
            for code in block.contain:
                block.next_slot_y_contain += code.block_height
                block.next_slot_y +=code.block_height
                block.block_height += code.block_height

            #block.update()
            block.next_slot_y += block.next_slot_y_contain-30
    def block_form_update(self):
        for block in self.controls:
            if block.IsContainer:
                block.load_block()
                pass

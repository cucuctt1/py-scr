import flet as ft
import container_block as ctb
import setting
class start_block(ft.GestureDetector):
    def __init__(self,x,y,container,id):
        super().__init__()

        self.left = x
        self.top = y
        self.belowcode = []
        self.block_hei = setting.START_BLOCK_HEIGHT

        self.content = ft.Container(bgcolor=setting.START_BLOCK_COLOR,width=150,height=30,content=ft.Text("test"))
        self.on_pan_start = self.ontop
        self.on_pan_update = self.drag
        self.code_container = container
        self.next_slot = self.top+30
        self.id = id
        self.upper = None #cant change
        #next slot
        self.nextslot = 30
    def drag(self,e:ft.DragUpdateEvent):
        e.control.top = ( e.control.top + e.delta_y)
        e.control.left = (e.control.left + e.delta_x)
        for codeblock in self.belowcode:
            codeblock.top = codeblock.top + e.delta_y
            codeblock.left = codeblock.left + e.delta_x
        self.code_container.update()
    def ontop(self,e:ft.DragStartEvent):
        self.code_container.controls.remove(self)
        self.code_container.controls.append(self)
        self.code_container.update()

    def reset_nextslot(self):
        for block in self.code_container.controls:
            sumofhei = 0
            for slot in block.belowcode:
                sumofhei += slot.block_hei
            block.nextslot = block.block_hei+sumofhei

    def add(self,block):
        self.belowcode.append(block)
        block.top = self.nextslot+self.top
        print(self.nextslot)
        self.reset_nextslot()
        block.left = self.left

        try:
            self.code_container.update()
        except:
            pass



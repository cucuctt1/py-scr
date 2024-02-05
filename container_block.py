import flet as ft
import setting

class container_block(ft.GestureDetector):
    def __init__(self, x, y, code_container, upper, id):
        super().__init__()
        self.top = y
        self.left = x
        self.belowcode = []
        self.code_container = code_container

        self.contain = []
        self.contain_nextslot = 30

        self.upper = upper
        self.id = id

        self.color = setting.CONTAINER_BLOCK_COLOR
        self.block_hei = setting.CONTAINER_BLOCK_HEIGHT

        self.drag_interval = 5
        self.on_pan_start = self.startdrag
        self.on_pan_update = self.updatedrag
        self.on_pan_end = self.enddrag

        self.nextslot = 30

        self.contain_hei = 30
        self.contain_wid = 20

        self.content =ft.Column([
            ft.Container(width=150,height=30,bgcolor=self.color,content=ft.Text("container"+str(self.id))),
            ft.Container(width=self.contain_wid,height=self.contain_hei,bgcolor=self.color),
            ft.Container(width=150,height=20,bgcolor=self.color)
        ],spacing=0)

    def updatedrag(self, e: ft.DragUpdateEvent):
        e.control.top = e.control.top + e.delta_y
        e.control.left = e.control.left + e.delta_x
        for codeblock in self.belowcode:
            codeblock.top = codeblock.top + e.delta_y
            codeblock.left = codeblock.left + e.delta_x
        for codeblock in self.contain:
            codeblock.top = codeblock.top + e.delta_y
            codeblock.left = codeblock.left + e.delta_x
            # codeblock.update()
        self.code_container.update()

    def startdrag(self, e: ft.DragStartEvent):
        self.code_container.controls.remove(self)
        self.code_container.controls.append(self)
        for block in self.contain:
            self.code_container.controls.remove(block)
            self.code_container.controls.append(block)
        self.first_pos_top = self.top
        self.first_pos_left = self.left
        if self.upper != None:
            self.belowcode = self.get_codeblock_list()
        self.lpos = []
        self.tpos = []
        for codeblock in self.belowcode:
            self.lpos.append(codeblock.left)
            self.tpos.append(codeblock.top)

        self.code_container.update()

    def enddrag(self, e: ft.DragStartEvent):
        self.reset_nextslot()
        if self.upper != None:
            if abs(self.first_pos_top - e.control.top) > 30 or abs(self.first_pos_left - e.control.left) > 150:
                blocklist = self.get_codeblock_list()
                self.belowcode = blocklist
                for block in blocklist:
                    block.upper = self
                    self.upper.belowcode.remove(block)
                self.removeitself()
            else:
                self.top = self.first_pos_top
                self.left = self.first_pos_left
                for n, codeblock in enumerate(self.belowcode):
                    codeblock.top = self.tpos[n]
                    codeblock.left = self.lpos[n]
                self.code_container.update()
        else:

            self.stick(e)

    def reset_nextslot(self):
        for block in self.code_container.controls:
            sumofhei = 0
            for slot in block.belowcode:
                sumofhei += slot.block_hei
            block.nextslot = block.block_hei+sumofhei

    def get_codeblock_list(self):
        index = self.upper.belowcode.index(self)
        results = self.upper.belowcode[index + 1:]
        return results

    def removeitself(self):
        if self.upper != None:
            self.upper.belowcode.remove(self)
            self.upper = None
            self.reset_nextslot()

    def stick(self,e):
        for block in self.code_container.controls:
            if block != self and block not in self.belowcode and block.upper == None:
                if (e.control.top-(block.nextslot+block.top) < 60 and
                        e.control.top-(block.nextslot+block.top) >=-20 and
                        e.control.left-block.left < 150 and
                        e.control.left-block.left >=-50) :
                    self.upper = block
                    block.add(self)
                    for code in self.belowcode:
                        block.add(code)
                        code.upper = block
                    self.belowcode = []
                    self.nextslot = 30
                    break
                else:
                    if isinstance(block,type(self)):
                        #print(e.control.top-(block.contain_nextslot+block.top) < 60 , e.control.top-(block.contain_nextslot+block.top) , e.control.left-(block.contain_wid+block.left) < 150, e.control.left-(block.contain_wid+block.left) )
                        if e.control.top-(block.contain_nextslot+block.top) < 60 and e.control.top-(block.contain_nextslot+block.top) >=-10 and e.control.left-(block.contain_wid+block.left) < 150 and e.control.left-(block.contain_wid+block.left) >=-30 :
                            self.add_to_container(block)

    def add(self, block):
        self.belowcode.append(block)
        block.top = self.nextslot+self.top
        print(self.nextslot)
        self.reset_nextslot()
        block.left = self.left

        self.code_container.update()

    def reset_contain_nextslot(self):
        sumofhei = 0
        for block in self.contain:
            sumofhei += block.block_hei
        self.contain_nextslot = 30+sumofhei
        self.contain_hei = self.contain_nextslot
        self.content.controls[1].height = self.contain_nextslot
        self.content.controls[1].update()
        print(self.contain_nextslot,self.content.controls[1].height)
        self.block_hei = setting.CONTAINER_BLOCK_HEIGHT+sumofhei
        self.code_container.update()

    def add_to_container(self,container):
        container.contain.append(self)

        self.upper = container
        for code in self.belowcode:
            code.upper = container

        self.top = container.top+container.contain_nextslot
        self.left = container.left+container.contain_wid
        container.reset_contain_nextslot()

        for block in self.belowcode:
            print("contain next slot",container.contain_nextslot)
            block.top = container.top + container.contain_nextslot
            block.left = container.left + container.contain_wid
            container.contain.append(block)
            container.reset_contain_nextslot()
        self.belowcode = []
        self.code_container.update()
        container.reset_contain_nextslot()

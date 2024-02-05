import flet as ft
import container_block as ctb
import setting
class code_block(ft.GestureDetector):
    def __init__(self, x, y, code_container, upper, id):
        super().__init__()
        self.code_container = code_container
        self.left = x
        self.top = y
        self.id = id
        self.upper = upper
        self.block_hei = setting.CODE_BLOCK_HEIGHT

        self.drag_interval = 5
        self.on_pan_update = self.updatedrag
        self.on_pan_start = self.startdrag
        self.on_pan_end = self.enddrag

        self.belowcode = []
        self.nextslot = 30
        self.content = ft.Container(bgcolor=setting.CODE_BLOCK_COLOR, content=ft.Text("test" + str(self.id) + str(self.nextslot)),
                                    width=150, height=setting.CODE_BLOCK_HEIGHT)

    def updatedrag(self,e:ft.DragUpdateEvent):
        e.control.top = e.control.top + e.delta_y
        e.control.left = e.control.left + e.delta_x
        for codeblock in self.belowcode:
            codeblock.top = codeblock.top + e.delta_y
            codeblock.left = codeblock.left + e.delta_x
        self.code_container.update()

    def startdrag(self,e:ft.DragStartEvent):
        self.code_container.controls.remove(self)
        self.code_container.controls.append(self)
        self.first_pos_top = self.top
        self.first_pos_left = self.left
        if self.upper!=None:
            self.belowcode=self.get_codeblock_list()
        self.lpos = []
        self.tpos = []
        for codeblock in self.belowcode:
            self.lpos.append(codeblock.left)
            self.tpos.append(codeblock.top)
        self.code_container.update()

    def enddrag(self,e:ft.DragStartEvent):
        self.reset_nextslot()
        if self.upper!=None:
            if abs(self.first_pos_top-e.control.top) > 30 or abs(self.first_pos_left-e.control.left) > 150:
                blocklist = self.get_codeblock_list()
                self.belowcode = blocklist
                if not isinstance(self.upper,ctb.container_block):
                    for block in blocklist:
                        block.upper = self
                        self.upper.belowcode.remove(block)
                else:
                    if self in self.upper.contain:
                        for block in blocklist:
                            block.upper = self
                            self.upper.contain.remove(block)
                            self.upper.reset_contain_nextslot()
                    else:
                        for block in blocklist:
                            block.upper = self
                            self.upper.belowcode.remove(block)
                self.removeitself()
            else:
                self.top = self.first_pos_top
                self.left = self.first_pos_left
                for n,codeblock in enumerate(self.belowcode):
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
        if not isinstance(self.upper,ctb.container_block):
            index = self.upper.belowcode.index(self)
            results = self.upper.belowcode[index+1:]
            return results
        else:
            index = self.upper.contain.index(self)
            results = self.upper.contain[index+1:]
            return  results

    def removeitself(self):
        if self.upper!=None:
            if isinstance(self.upper,ctb.container_block):
                if self not in self.upper.contain:
                    self.upper.belowcode.remove(self)
                    self.upper = None
                    self.reset_nextslot()
                else:
                    self.upper.contain.remove(self)
                    self.upper.reset_contain_nextslot()
                    self.upper = None
                    self.reset_nextslot()
            else:
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
                    if isinstance(block,ctb.container_block):
                        #print(e.control.top-(block.contain_nextslot+block.top) < 60 , e.control.top-(block.contain_nextslot+block.top) , e.control.left-(block.contain_wid+block.left) < 150, e.control.left-(block.contain_wid+block.left) )
                        if e.control.top-(block.contain_nextslot+block.top) < 60 and e.control.top-(block.contain_nextslot+block.top) >=-10 and e.control.left-(block.contain_wid+block.left) < 150 and e.control.left-(block.contain_wid+block.left) >=-30 :
                            self.add_to_container(block)

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

    def add(self,block):
        self.belowcode.append(block)
        block.top = self.nextslot+self.top

        self.reset_nextslot()
        block.left = self.left

        self.code_container.update()


import flet as ft
import os


class block(ft.GestureDetector):
    def __init__(self, iscontainer=False, have_parameter=False,
                 isheader=False, executable=False,
                 id=1, x=0, y=0, color=None, content=None, code_container=None,
                 block_height=30, block_width=150, code=None, below_code=[], upper_code=None, contain=[]):
        super().__init__(self)

        self.IsContainer = iscontainer
        self.HaveParameter = have_parameter
        self.IsHeader = isheader
        self.Executable = executable

        self.id = id
        self.top = y
        self.left = x
        self.color = color

        self.content = content
        self.code_container = code_container
        self.expand = True

        self.block_height = block_height
        self.block_width = block_width

        self.below_code = list(below_code)
        self.upper_code = upper_code
        self.contain = list(contain)

        self.offset1 = 20
        self.top_part = 30
        self.bot_part = 20
        self.next_slot_x = 0
        self.next_slot_y = block_height
        self.next_slot_x_contain = 0
        self.next_slot_y_contain = 30

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.end_drag
        self.load_block()

    def load_block(self):
        if self.IsContainer:

            self.content = ft.Column([
                ft.Container(height=self.top_part, width=self.block_width, bgcolor=self.color,
                             content=ft.Text("this is container")),
                ft.Container(height=20 + self.next_slot_y_contain - 30, width=self.offset1, bgcolor=self.color),
                ft.Container(height=self.bot_part, width=self.block_width, bgcolor=self.color)
            ], spacing=0)
        else:
            self.content = ft.Container(height=30, width=150, content=ft.Text("test"), bgcolor=self.color)

    def drag(self, e: ft.DragUpdateEvent):
        self.move(delta_x=e.delta_x, delta_y=e.delta_y)
        self.code_container.update()

    def move(self, delta_x, delta_y):
        self.left += delta_x
        self.top += delta_y

        for child_block in self.below_code:
            child_block.move(delta_x, delta_y)
        if self.IsContainer:
            for child_block in self.contain:
                child_block.move(delta_x, delta_y)
        self.code_container.update()

    def move_to_end(self,target):#end of code container list

        self.code_container.controls.remove(target)
        self.code_container.controls.append(target)

    def move_ontop(self):
        self.move_to_end(self)
        for below in self.below_code:
            below.move_ontop()
        if self.IsContainer:
            for code in self.contain:
                code.move_ontop()

    def start_drag(self, e: ft.DragStartEvent):
        self.move_ontop()
        self.temp = self.upper_code
        self.start_pos_x, self.start_pos_y = e.control.left, e.control.top
        below_code = self.get_below()
        self.start_pos_list = [(code.left, code.top) for code in below_code]
        if self.upper_code:
            self.remove_self(mode=2)
        self.code_container.slot_update()



    def end_drag(self, e: ft.DragEndEvent):
        self.code_container.slot_update()
        filtered_block = filter(lambda block: block != self and block not in self.below_code and block not in self.contain,
                                self.code_container.controls)

        for block in filtered_block:

            status = self.stick_check(block)

            if block.IsContainer:
                if not block.upper_code:
                    if status == 1:

                        block.add_to_below(self)
                        self.below_code = []

                        return None
                    elif status == 2:

                        block.add_to_contain(self)
                        self.below_code = []
                        return None
                elif status == 2:

                    block.add_to_contain(self)
                    self.below_code = []
                    return None
            else:
                if status == 1:
                    block.add_to_below(self)
                    self.below_code = []

                    return None

        self.code_container.update2()

        if self.upper_code:
            if self.leave_check(self.start_pos_x, self.start_pos_y):
                self.remove_self()
                if self.IsContainer:
                    self.content.controls[1] = ft.Container(height=20 + self.next_slot_y_contain - 30,
                                                            width=self.offset1, bgcolor=self.color)
                self.code_container.slot_update()
                self.upper_code = None
                pass
            else:
                del_x = e.control.left - self.start_pos_x
                del_y = e.control.top - self.start_pos_y
                self.move(-del_x, -del_y)
                if self in self.upper_code.contain:
                    for code in self.below_code:
                        code.upper_code = self.upper_code
                        self.upper_code.contain.append(code)
                    self.below_code = []
                else:
                    for code in self.below_code:
                        code.upper_code = self.upper_code
                        self.upper_code.below_code.append(code)
                    self.below_code = []
        self.code_container.slot_update()

        self.place_fix()
        self.code_container.update2()


    def stick_check(self, block) -> int:
        upper_check = self.upper_code is None
        if upper_check:
            X_axis_check = -30 <= self.left - (block.left + block.next_slot_x) < 150
            Y_axis_check = -15 <= self.top - (block.top + block.next_slot_y) < 30
        else:
            X_axis_check = False
            Y_axis_check = False

        container_check = block.IsContainer
        if container_check:
            X_axis_check_container = -60 <= self.left - (block.left + block.next_slot_x_contain) < 150
            Y_axis_check_container = -15 <= self.top - (block.top + block.next_slot_y_contain) < 30
        else:
            X_axis_check_container = False
            Y_axis_check_container = False

        if X_axis_check_container and Y_axis_check_container:
            return 2
        if X_axis_check and Y_axis_check:
            return 1

        return 0

    def leave_check(self, del_x, del_y):
        X_check = abs(del_x - self.left) > 100
        Y_check = abs(del_y - self.top) > 30
        return X_check or Y_check

    def add_to_list(self, target_list, target_element):
        target_list.append(target_element)

    def add_to_contain(self, block):

        self.block_height += block.block_height
        self.add_to_list(self.contain, block)
        block.upper_code = self
        block.place(self.left + self.next_slot_x_contain, self.top + self.next_slot_y_contain)
        self.next_slot_update()
        for code in block.below_code:
            code.upper_code = self
            self.add_to_list(self.contain, code)
            block.place(self.left + self.next_slot_x_contain, self.top + self.next_slot_y_contain)
        block.below_code = []


    def add_to_below(self, block):

        self.add_to_list(self.below_code, block)
        block.upper_code = self
        block.place(self.left, self.top + self.next_slot_y)
        self.next_slot_update()
        for code in block.below_code:
            code.upper_code = self
            self.add_to_list(self.below_code, code)
            code.place(self.left, self.top + self.next_slot_y)
        if block.IsContainer:
            block.next_slot_y_contain = block.top_part
            for code in block.contain:
                code.place(block.left+block.offset1,block.next_slot_y_contain+block.top)
                block.next_slot_y_contain +=code.block_height

        block.below_code.clear()

    def place(self, x, y):
        self.top = y
        self.left = x
        for child in self.contain:
            child.top = self.top + self.top_part
            child.left = self.left + self.offset1
            child.place(self.left + self.offset1, self.top + self.top_part)

    def remove_self(self, mode=1):
        below_code = self.get_below()
        if self.upper_code:
            if self in self.upper_code.contain:
                if mode == 1:
                    self.upper_code.contain.remove(self)
                for code in below_code:
                    self.upper_code.contain.remove(code)
                    code.upper_code = self
                    self.below_code.append(code)
            else:
                if mode == 1:
                    self.upper_code.below_code.remove(self)
                for code in below_code:
                    self.upper_code.below_code.remove(code)
                    if mode == 1:
                        code.upper_code = self
                    self.below_code.append(code)
        if mode == 1:
            self.upper_code = None

    def get_below(self):
        if self.upper_code:
            if self in self.upper_code.contain:
                index = self.upper_code.contain.index(self)

                return list(self.upper_code.contain[index + 1:])
            else:
                index = self.upper_code.below_code.index(self)

                return list(self.upper_code.below_code[index + 1:])
        else:
            return self.below_code

    def next_slot_update(self):
        self.code_container.slot_update()

    #call to the upper code
    def place_fix(self):
        if self.upper_code:
            self.upper_code.next_slot_y_contain = self.upper_code.top_part
            for code in self.upper_code.contain:
                code.place(self.upper_code.left+self.upper_code.offset1,self.upper_code.next_slot_y_contain+self.upper_code.top)
                self.upper_code.next_slot_y_contain+=code.block_height
            self.upper_code.place_fix()


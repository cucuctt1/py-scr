import flet as ft
import block_logic as bl




class block(ft.GestureDetector):
        def __init__(self,iscontainer=False,haveparameter=False,
                     isheader=False,executable=False,
                     id=1,x=0,y=0,color=None,content=None,code_container=None,block_hei=30,
                     block_wid=150,code=None,below_code= [],upper_code=None,contain= []):
            #init part
            super().__init__(self)
            #setting prop
            self.IsContainer = iscontainer
            self.HaveParameter = haveparameter
            self.IsHeader = isheader
            self.Executable = executable # for comment block : False

            #basic prop
            self.id = id #specific id
            self.top = y
            self.left = x
            self.color = color

            self.content = content
            self.code_container = code_container
            self.expand = True
            #calculate prop
            self.block_height = block_hei
            self.block_width = block_wid

            #code execute prop
            #self.code = code

            #belong prop
            #None for default
            self.below_code = list(below_code) #list
            self.upper_code = upper_code #single element
            self.contain = list(contain) #list
                                # only for self.IsContainer = True
            self.offset1 = 20
            self.top_part = 30
            self.bot_part = 20
            self.next_slot_x = 0
            self.next_slot_y = block_hei
            self.next_slot_x_contain = 0
            self.next_slot_y_contain = 30
            self.on_pan_start = self.startdrag
            self.on_pan_update = self.drag
            self.on_pan_end = self.enddrag
            self.load_block()

        def load_block(self):
            if self.IsContainer:
                print("loaded",self.id)
                self.content = ft.Column([
                    ft.Container(height=self.top_part,width=self.block_width,bgcolor=self.color,content=ft.Text("this is container")),
                    ft.Container(height=20+self.next_slot_y_contain,width=self.offset1,bgcolor=self.color),
                    ft.Container(height=self.bot_part,width=self.block_width,bgcolor=self.color)
                ],spacing=0)
            else:
                self.content = ft.Container(height=30, width=150, content=ft.Text("test"), bgcolor=self.color)

        def drag(self,e:ft.DragUpdateEvent):

            self.move(delta_x=e.delta_x,delta_y=e.delta_y)
            self.code_container.update()

        def move(self,delta_x,delta_y):

            self.left +=delta_x
            self.top +=delta_y
            if not self.upper_code:
                for child_block in self.below_code:
                    child_block.move(delta_x,delta_y)
            if self.IsContainer:
                for child_block in self.contain:
                    child_block.move(delta_x,delta_y)
            self.code_container.update()

        def startdrag(self,e:ft.DragStartEvent):
            self.start_pos_x,self.start_pos_y = e.control.left,e.control.top
            below_code = self.get_below()
            self.start_pos_list = []
            for code in below_code:
                self.start_pos_list.append((code.left,code.top))
            if self.upper_code:
                self.remove_self(mode=2)
            #self.debug_level(0)
            self.code_container.slot_update()
            print(self.below_code)
        def debug_level(self,level):
            print(level,self.below_code)
            for contain in self.below_code:
                for a in contain.contain:
                    a.debug_level(level+1)
            for a in self.contain:
                a.debug_level(level+1)
            print(level+1,self.contain)


        def enddrag(self,e:ft.DragEndEvent):
            self.code_container.slot_update()
            filtered_block = filter(lambda block: block != self and block not in self.below_code and block not in self.contain,
                                    self.code_container.controls)

            for block in filtered_block:
                status = self.stick_check(block)
                if block.IsContainer:
                    if not block.upper_code:
                        if status==1:
                            block.add_to_below(self)
                            break
                        elif status == 2:
                            block.add_to_contain(self)
                            break

                else:
                    if status == 1:
                        block.add_to_below(self)
                        print(block.id)
                        break
            self.code_container.update()


            if self.upper_code:
                if self.leave_check(self.start_pos_x,self.start_pos_y):
                    print("leaved")

                    self.remove_self()
                    print(self.next_slot_y_contain)
                    if self.IsContainer:
                        self.content.controls[1] = ft.Container(height=20+self.next_slot_y_contain-30,width=self.offset1,bgcolor=self.color)
                    self.code_container.slot_update()
                    self.upper_code = None
                    pass
                else:
                        #bouce back
                    del_x = e.control.left-self.start_pos_x
                    del_y = e.control.top-self.start_pos_y
                    self.move(-del_x,-del_y)
                    if self in self.upper_code.contain:
                        for code in self.below_code:
                            code.upper_code = self.upper_code
                            self.upper_code.contain.append(code)
                        self.below_code = []
                        #self.upper_code.add_to_contain(self)
                    else:
                        for code in self.below_code:
                            code.upper_code = self.upper_code
                            self.upper_code.below_code.append(code)
                        self.below_code = []
            self.code_container.slot_update()
            self.code_container.update()
            self.update()
            pass

        #bouce back = place
        def stick_check(self,block) ->int:
            # state 0 = No stick detected
            # state 1 = below stick detected
            # state 2 = contain stick detected
            upper_check = self.upper_code == None
            if upper_check:
                X_axis_check = self.left-(block.left+block.next_slot_x) < 150 and self.left-(block.left+block.next_slot_x) >=-30
                Y_axis_check = self.top-(block.top+block.next_slot_y) < 30 and self.top-(block.top+block.next_slot_y) >= -15
            else:
                X_axis_check = False
                Y_axis_check = False

            container_check = block.IsContainer == True
            if container_check:
                X_axis_check_container = self.left-(block.left+block.next_slot_x_contain) < 150 and self.left-(block.left+block.next_slot_x_contain) >=-60
                Y_axis_check_container = self.top-(block.top+block.next_slot_y_contain) < 30 and self.top-(block.top+block.next_slot_y_contain) >=-15
            else:
                X_axis_check_container = False
                Y_axis_check_container = False

            if X_axis_check_container and Y_axis_check_container:
                return 2
            if X_axis_check and Y_axis_check:
                return 1

            return 0

        def leave_check(self,del_x,del_y):
            X_check = abs(del_x-self.left) > 100
            Y_check = abs(del_y-self.top) > 30
            return X_check or Y_check
        def add_to_list(selft,target_list,target_element):
            if target_element not in target_list:
                target_list.append(target_element)
        def add_to_contain(self,block):
            print("added to contain")
            self.block_height += block.block_height
            self.add_to_list(self.contain,block)
            block.upper_code = self
            block.place(self.left+self.next_slot_x_contain,self.top+self.next_slot_y_contain)
            self.next_slot_update()
            for code in block.below_code:
                code.upper_code = self
                self.add_to_list(self.contain,code)
                block.place(self.left+self.next_slot_x_contain,self.top+self.next_slot_y_contain)
            block.below_code = []
            print(self.contain)

        def add_to_below(self,block):
            print("added to below")
            self.add_to_list(self.below_code,block)
            block.upper_code = self
            block.place(self.left,self.top+self.next_slot_y)
            self.next_slot_update()
            for code in block.below_code:
                code.upper_code = self
                self.add_to_list(self.below_code,code)
                code.place(self.left,self.top+self.next_slot_y)
            print(self.below_code)
            block.below_code = []

        def place(self,x,y):
            self.top = y
            self.left = x
            for child in self.contain:
                child.top = self.top+self.top_part
                child.left = self.left+self.offset1
                child.place(self.left+self.offset1,self.top+self.top_part)

        def remove_self(self,mode = 1):
            below_code = self.get_below()
            if self.upper_code:
                if self in self.upper_code.contain:
                    if mode==1:
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
            if mode==1:
                self.upper_code = None

        def get_below(self):
            if self.upper_code:
                if self in self.upper_code.contain:
                    index = self.upper_code.contain.index(self)
                    print(self.upper_code.contain[index+1:])
                    return list(self.upper_code.contain[index+1:])
                else:
                    index = self.upper_code.below_code.index(self)
                    print(self.upper_code.below_code[index+1:])
                    return list(self.upper_code.below_code[index+1:])
            else:
                return self.below_code
        def next_slot_update(self):
            self.code_container.slot_update()




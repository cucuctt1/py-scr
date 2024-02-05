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
            self.next_slot_x = 0
            self.next_slot_y = block_hei
            self.next_slot_x_contain = 0
            self.next_slot_y_contain = 30
            self.on_pan_start = self.startdrag
            self.on_pan_update = self.drag
            self.on_pan_end = self.enddrag
            #self.installize_parameter


        #basic block logic

        # update drag
        def drag(self,e:ft.DragUpdateEvent):
            self.move(e.delta_x,e.delta_y)
            self.place_status = self.check_for_leave(e.control.left,e.control.top)
            self.code_container.update()


        def move(self,delta_x,delta_y):
            self.left += delta_x
            self.top += delta_y
            if self.IsContainer:
                for children in self.contain:
                    children.move(delta_x,delta_y)
            if self.upper_code == None:
                for children in self.below_code:
                    children.move(delta_x, delta_y)



        #start drag
        def startdrag(self,e:ft.DragStartEvent):
            self.first_pos_x = e.control.left
            self.first_pos_y = e.control.top
            self.pos_list = []#pair tuple
            below_code = self.get_below_code()

            for children in below_code:
                self.pos_list.append((children.left,children.top))

            self.move_to_top()
            if self.upper_code:
                #print(below_code)
                self.below_code = below_code
                for n in range(len(self.below_code)):
                    self.below_code[n].upper_code = self
                self.upper_code = None
                print(self.below_code)



        def push_to_top(self,target):
            self.code_container.controls.remove(target)
            self.code_container.controls.append(target)


        def move_to_top(self):
            self.push_to_top(self)
            for children in self.below_code:
                self.push_to_top(children)
            for children in self.contain:
                self.push_to_top(children)

            self.code_container.update()

        #end drag
        def check_for_leave(self,p1,p2):
            if self.upper_code and (p1-self.first_pos_x) > 150 or abs(p2-self.first_pos_y):
                return True
            return False
        def enddrag(self,e:ft.DragEndEvent):
            if not self.upper_code:
                self.stick()
                pass
            else:

                if abs(self.first_pos_y - e.control.top) > 30 or abs(self.first_pos_x - e.control.left) > 150:
                    self.below_code = self.get_below_code()
                    temp = self.upper_code
                    self.remove_self(self.upper_code,self.below_code)
                    temp.reset_next_slot()

                else:
                    self.top = self.first_pos_y
                    self.left = self.first_pos_x
                    for n,block in enumerate(self.below_code):
                        block.left,block.top = self.pos_list[n]
                self.code_container.update()



        # stick to block
        def stick(self):
            filtered_controls = filter(lambda c: c != self and c not in self.below_code and c not in self.contain,
                                       self.code_container.controls)
            for block in filtered_controls:

                block_nsl_x,block_nsl_y = block.next_slot_x,block.next_slot_y
                if self.check_for_stick(0,block_nsl_y,block.left,block.top):

                    block.add_block(self,"below")
                    self.below_code = []
                    self.upper_code = block
                    self.code_container.update()
                    break
        def check_for_stick(self,block_next_slot_x,block_next_slot_y,block_left,block_top):
            check_upper = self.upper_code == None
            X_axis_check = self.left-(block_next_slot_x+block_left) < 60 and self.left-(block_next_slot_x+block_left) >=-20
            Y_axis_check = self.top-(block_next_slot_y+block_top) < 150 and self.top-(block_next_slot_y+block_top) >=-50

            return check_upper and X_axis_check and Y_axis_check


        # other function

        def reset_next_slot(self):
            self.next_slot_y = self.block_height
            self.next_slot_x = self.left
            if self.below_code:
                for child in self.below_code:
                    self.next_slot_y += child.block_height

            ### add next slot for contain
            self.next_slot_y_contain = self.block_height
            self.next_slot_x_contain = self.offset1

            if self.IsContainer:
                for child in self.contain:
                    self.next_slot_y_contain +=child.block_height
                    child.reset_next_slot()
                #child.reset_next_slot()

        # add for container block
        def add_block(self,block,container):
            if container == "below":
                self.below_code.append(block)
                block.top = self.next_slot_y+self.top
                block.left = self.left
                self.reset_next_slot()
                if block.upper_code == None:
                    for below_code in block.below_code:
                        self.add_block(below_code,"below")
                block.upper_code = self
                block.below_code = []
            else:
                self.contain.append(block)
                block.top = self.next_slot_y_contain+self.top
                block.left = self.left+self.next_slot_x_contain
                self.reset_next_slot()
                if block.upper_code == None:
                    for below_code in block.below_code:
                        self.add_block(below_code,"contain")
                block.upper_code = self
                block.below_code = []

        def get_below_code(self):
            # get index
            if self.upper_code:
                if self in self.upper_code.contain:
                    self_index = self.upper_code.contain.index(self)
                    return self.upper_code.contain[self_index+1:]
                else:
                    self_index = self.upper_code.below_code.index(self)
                    return self.upper_code.below_code[self_index+1:]
            else:
                return self.below_code

        def remove_block(self):
            below_code = self.get_below_code()
            if self in self.upper_code.contain:
                self.upper_code.contain.remove(self)

                for code in below_code:
                    self.upper_code.contain.remove(code)
                    code.upper_code = self
                    self.below_code.append(code)
                self.upper_code = None
            else:
                self.upper_code.below_code.remove(self)
                for code in below_code:
                    self.upper_code.below_code.remove(code)
                    code.upper_code = self
                    self.below_code.append(code)
                self.upper_code = None






        def assign_self(self,target):
            self.upper_code = target
            target.below_code.append(self)
            for child in self.below_code:
                target.below_code.append(child)
                child.upper_code = target
            self.below_code = []

        def remove_self(self,target,below):

            target.below_code.remove(self)
            for child in below:
                target.below_code.remove(child)
                child.upper_code = self
            self.upper_code = None

        def printstatus(self,block):
            print("block upper",block.upper_code,"block below",block.below_code)

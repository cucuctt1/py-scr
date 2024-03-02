#new block test
import flet as ft
import default_block_struct

def check_type(text):
    try:
        result = int(text) if '.' not in text else float(text)
        return result
    except ValueError:
        return text
def text_tranform(text):
    if isinstance(text,str):
        return '"'+text+'"'
    else:
        return text

class block(ft.GestureDetector):
    def __init__(self, iscontainer=False, have_parameter=False,
                 isheader=False, executable=False,
                 id=1, x=0, y=0, color=None, content=None, code_container=None,
                 block_height=30, block_width=150, code=None, below_code=[], upper_code=None, contain=[],Npara=0,struct = None
                 ,args = False):
        super().__init__(self)

        self.IsContainer = iscontainer
        self.HaveParameter = have_parameter
        self.IsHeader = isheader
        self.Executable = executable

        if self.HaveParameter:
            self.Npara = Npara
        else:
            self.Npara = 0

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
        self.parameter_buffer = [None]*(self.Npara)
        self.args = args

        self.offset_height = 20
        self.offset1 = 20
        self.top_part = 30
        self.bot_part = 20

        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.end_drag
        self.text_wid = 5*10

        self.sideblock_offset = 30
        self.hook = None
        self.side_block = None

        #code parser
        self.code = code #string data
        self.struct = struct
        self.load_block()


    #rule
    # indivitual element for better control
    def load_para(self,element_array):#->data

        spacing = 10

        para_wid = 30 #default
        para_hei = 20 #default
        para_x,para_y= None,None
        para_block = ft.Container(bgcolor=ft.colors.WHITE,width=para_wid,height=para_hei,top=para_y,left=para_x)

        text_data = ""
        text_size = None #default
        text_wid = (len(text_data))*10
        text_hei = None
        text_y = None
        text_x = None
        text_block = ft.Text(size=text_size,value=text_data,width=text_wid,height=text_hei,top=text_y,left=text_x)

        right_padding = 10
        row_buffer = []

        for item in element_array:
            block_type, data = item
            if block_type=="text":
                text_block = ft.Text(size=text_size, value=text_data, width=text_wid, height=20)
                text_block.value = data
                text_block.width = (len(data))*10
                row_buffer.append(text_block)
            else:
                content_text_field = ft.TextField(width=para_wid,text_size=15,dense=False,bgcolor=ft.colors.WHITE,cursor_height=para_hei-3,content_padding=ft.padding.only(top=-4,left=3,right=3),on_change=self.on_change)
                para_block = ft.Container(bgcolor="",width=para_wid,height=para_hei,content=content_text_field)
                row_buffer.append(para_block)
        return list(row_buffer)

    def on_change(self,e):
        data = e.control.value
        data_len = len(data)*10-(len(data)*0.653333)
        print(len(data))
        for index,item in enumerate(self.arg_buffer):
            if e.control is item.content:
                self.change_wid(data_len,item)
                break
        #print(vars(e))

        pass
    def change_wid(self,wid,slot):
        slot.width = max(30,wid)

        self.size_manage()
        self.reset_para_size()
        self.code_container.update()
        pass
    def get_row_wid(self,row):
        res = 0
        for item in row:
            res+=item.width
            res+=10
        return res+10

    def get_center(self,item):
        if self.IsContainer:
            center  =(self.top_part-item.height)/2
        else:
            center = (self.block_height-item.height)/2
        return center

    def posion_manage(self,row,para_array,spacing = 10,size=10):
        change_x = 5
        for n,packed_data in enumerate(row):
            data_type,data = packed_data
            if data_type == "text":
                text_wid = (len(data)*size)
                para_array[n].left = change_x
                para_array[n].top = self.get_center(para_array[n])
                change_x += text_wid+spacing

            else:
                block_wid = para_array[n].width
                para_array[n].left = change_x
                para_array[n].top = self.get_center(para_array[n])
                try:
                    index = self.arg_buffer.index(para_array[n])
                    side_block = self.parameter_buffer[index]
                    if side_block:
                        side_wid = side_block.get_side_block_wid()
                    else:
                        side_wid = 0
                except:
                    side_wid = 0
                change_x += block_wid+spacing


    def get_side_block_wid(self):
        if self.side_block:
            wid = self.side_block.block_width
            return wid + self.side_block.get_side_block_wid() + 1
        else:
            return 0

    def load_block(self,text = "dd"):
        if self.struct:
            self.data = self.struct[0]
        else:
            self.data = [("text","none")]
        self.para_data = self.load_para(self.data)
        self.posion_manage(self.data,self.para_data)
        self.arg_buffer = [item for item in self.para_data if isinstance(item,ft.Container)]

        self.block_width = max(self.block_width,self.get_row_wid(self.para_data))
        display = ft.Stack()
        display.controls.extend(self.para_data)

        if self.IsContainer:
            self.content = ft.Column([
                ft.Container(height=self.top_part, width=self.block_width, bgcolor=self.color,
                             content=display),
                ft.Container(height=self.offset_height, width=self.offset1, bgcolor=self.color),
                ft.Container(height=self.bot_part, width=self.block_width, bgcolor=self.color)
            ], spacing=0)
        else:
            self.content = ft.Container(height=self.block_height, width=self.block_width, content=display, bgcolor=self.color,border=ft.border.all(1,ft.colors.BLACK),border_radius=4)
    def get_below(self):
        if self.upper_code:
            if self in self.upper_code.contain:
                index = self.upper_code.contain.index(self)
                return list(self.upper_code.contain[index+1:])
            else:
                index = self.upper_code.below_code.index(self)
                return list(self.upper_code.below_code[index+1:])
        else:
            return self.below_code
    def reset_height(self):
        self.offset_height = 20
        for item in self.contain:
            self.offset_height+=item.block_height
        if self.IsContainer:
            self.block_height = self.top_part+self.bot_part+self.offset_height
        if self.upper_code:
            self.upper_code.reset_height()

        self.place_block()
        self.content_update()

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
        if self.HaveParameter:
            for code in self.parameter_buffer :
                if code != None:
                    code.move_ontop()
        if self.side_block:
            self.side_block.move_ontop()

    def start_drag(self,e:ft.DragStartEvent):
        self.move_ontop()
        # print("block_height",self.block_height,"block_width",self.block_width)
        self.temp_upper = self.upper_code
        self.start_pos_x,self.start_pos_y = e.control.left,e.control.top
        if self.upper_code and self not in self.upper_code.parameter_buffer:
            below_code = self.get_below()
            self.start_pos_list  = [(code.left,code.top) for code in below_code]
            if self.upper_code:
                if self in self.upper_code.contain:
                    self.upper_code.contain.remove(self)
                    self.upper_code.contain = [item for item in self.upper_code.contain if item not in below_code]
                else:
                    self.upper_code.below_code.remove(self)
                    self.upper_code.below_code = [item for item in self.upper_code.below_code if item not in below_code]
                for item in below_code:
                    self.add_to_below(item)
                self.upper_code.reset_height()
                self.code_container.update()
                #self.upper_code.load_block()
                self.upper_code = None
        elif self.upper_code and not self.IsContainer:
            index = self.upper_code.parameter_buffer.index(self)
            self.upper_code.parameter_buffer[index] = None
            self.upper_code.reset_para_size()
            self.upper_code.place_block()
            self.upper_code = None
            self.code_container.update()
        elif self.hook:
            temp = self.hook.side_block
            self.hook.side_block = None
            temp.reset_para_size()
            self.hook = None
            self.code_container.update()
        print("execute",self.code_parser(),"->")
        exec(self.code_parser())
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
        if self.HaveParameter:
            for child_block in self.parameter_buffer:
                if child_block:
                    child_block.move(delta_x,delta_y)
        if self.side_block:
            self.side_block.move(delta_x,delta_y)

    def end_drag(self,e : ft.DragEndEvent):
        for item in self.code_container.controls:
            stick_status = self.stick_check(item)
            if item.HaveParameter and not self.below_code and not self.IsContainer:
                for n,para_slot in enumerate(item.arg_buffer):
                    stick_status_para = self.stick_check(item,para=para_slot)
                    if stick_status_para == 3:
                        item.add_to_para(self,n)
                        return
            if item.IsContainer:
                if item.upper_code:
                    if stick_status == 2:
                        item.add_to_contain(self)
                        self.reset_height()
                        self.code_container.update()
                        return
                else:
                    if stick_status == 1:
                        item.add_to_below(self)
                        self.reset_height()
                        self.code_container.update()
                        return
                    if stick_status == 2:
                        item.add_to_contain(self)
                        self.reset_height()
                        self.code_container.update()
                        return
            else:
                if not item.upper_code:
                    if stick_status == 1:
                        item.add_to_below(self)
                        self.reset_height()
                        self.code_container.update()
                        return
                if not item.IsContainer and not self.hook and not self.IsContainer:
                    if stick_status == 4:
                        item.add_to_sideblock(self)
                        self.code_container.update()

    def get_next_slot_contain(self):
        result = 0
        for item in self.contain:
            result+=item.block_height
        return result
    def get_next_slot_below(self):
        result = 0
        for item in self.below_code:
            result+=item.block_height
        return result

    def stick_check(self,target,para = None) -> int: # return status
        upper_check = self.upper_code is None
        if upper_check:
            x_axis_check = -15 <= self.left - target.left < 80
            y_axis_check = -8 <=self.top - (target.top+target.get_next_slot_below()+target.block_height) < 25
        else:
            x_axis_check = False
            y_axis_check = False
        container_check = target.IsContainer
        if container_check:
            x_axis_check_contain = -30 <= self.left - (target.left) < 80
            y_axis_check_contain = -8 <=self.top - (target.top+target.get_next_slot_contain()+target.top_part) < 25
        else:
            x_axis_check_contain = False
            y_axis_check_contain = False
        have_parameter_check = target.HaveParameter
        if have_parameter_check and para:
            x_axis_check_para = -5 <= self.left -(para.left+target.left) < 25
            y_axis_check_para = -3 <= self.top - (para.top+target.top) < 18

        else:
            x_axis_check_para = False
            y_axis_check_para = False

        hook_check = not self.hook
        if hook_check and not target.side_block:
            x_axis_check_sideblock = -5 <= self.left -(target.left+target.block_width) < 25
            y_axis_check_sideblock = -3 <= self.top - (target.top) < 18
        else:
            x_axis_check_sideblock = False
            y_axis_check_sideblock = False

        if x_axis_check_sideblock and y_axis_check_sideblock:
            return 4
        if x_axis_check_para and y_axis_check_para:
            return 3
        if y_axis_check_contain and x_axis_check_contain:
            return 2
        if x_axis_check and y_axis_check:
            return 1
        return 0

    def add_to_sideblock(self,target):
        self.side_block = target
        target.hook = self
        self.size_manage()
        self.place_block()
    def add_to_para(self,target,slot):
        if not self.parameter_buffer[slot]:
            target.upper_code = self
            self.parameter_buffer[slot] = target
            self.arg_buffer[slot].content.value = ""
            self.set_size_para(target, slot)
            self.size_manage()
            self.place_block()
    def content_update(self):
        if self.IsContainer:
            display = ft.Stack()
            display.controls.extend(self.para_data)
            self.content.controls[1] = ft.Container(height=self.offset_height, width=self.offset1, bgcolor=self.color)
            self.content.controls[0] = ft.Container(height=self.top_part, width=self.block_width, bgcolor=self.color,
                         content=display)
            self.content.controls[2] = ft.Container(height=self.bot_part, width=self.block_width, bgcolor=self.color)
        try:
            self.content.content.update()
        except:
            pass
        try:
            self.content.controls[0].update()
        except:
            pass
    def set_size_para(self,item,slot):
        self.arg_buffer[slot].height = item.block_height-1
        self.arg_buffer[slot].width = item.block_width-1+self.parameter_buffer[slot].get_side_block_wid()
        try:
            self.content.content.update()
        except:
            try:
                self.content.controls[0].update()
            except:
                pass

    def get_max_height(self):
        max_hei = 30
        for item in self.parameter_buffer:
            if item:
                max_hei = max(max_hei, item.get_max_height())
                max_hei = max(max_hei,item.block_height)
        return max_hei
    def get_max_width(self):
        wid = self.para_data[-1].left+self.para_data[-1].width+10
        return wid
    def args_manage(self):
        if self.args:
            if self.parameter_buffer[-1] or self.arg_buffer[-1].content.value:
                print("add 1 para")
                para_wid = 30  # default
                para_hei = 20  # default
                self.Npara += 1
                self.struct[0].append(("para", None))
                self.parameter_buffer.append(None)
                print(self.parameter_buffer)
                self.data = self.struct[0]
                content_text_field = ft.TextField(width=para_wid, text_size=15, dense=False, bgcolor=ft.colors.WHITE,
                                                  cursor_height=para_hei - 3,
                                                  content_padding=ft.padding.only(top=-4, left=3, right=3),
                                                  on_change=self.on_change)
                para_block = ft.Container(bgcolor="", width=para_wid, height=para_hei, content=content_text_field)
                self.para_data.append(para_block)
                self.arg_buffer.append(para_block)
                self.content.content.controls.append(para_block)
            elif self.Npara>1 and (not self.arg_buffer[-2].content.value and not self.parameter_buffer[-2]):
                print("remove 1 para")
                self.Npara = max(1,self.Npara-1)
                self.struct[0].pop()
                self.parameter_buffer.pop()
                self.data = self.struct[0]
                self.para_data.pop()
                self.arg_buffer.pop()
                self.content.content.controls.pop()

    def size_manage(self):
        for item in self.parameter_buffer:
            if item:
                if self.IsContainer:
                    self.top_part = self.get_max_height()+10
                    self.reset_height()
                else:
                    self.block_height = self.get_max_height()+10
                    self.height = self.block_height
        self.args_manage()
        self.posion_manage(self.data, self.para_data)
        temp = self.get_max_width()

        self.block_width = max(self.block_width,temp)
        self.width = self.block_width

        if self.upper_code and self.upper_code.HaveParameter and self in self.upper_code.parameter_buffer:
            self.upper_code.set_size_para(self, self.upper_code.parameter_buffer.index(self))
            self.upper_code.size_manage()
            self.upper_code.content_update()
            self.upper_code.place_block()
        self.reset_height()
        self.place_block()
        self.content_update()

    def reset_para_size(self):
        for n,item in enumerate(self.parameter_buffer):
            if not item:
                if not self.arg_buffer[n].content.value:
                    self.arg_buffer[n].width = 30
                    self.arg_buffer[n].height = 20
        if self.IsContainer:
            self.top_part = self.get_max_height()
            self.reset_height()
        else:
            self.height = self.get_max_height()
            self.block_height = self.height
        self.args_manage()
        self.posion_manage(self.data, self.para_data)
        self.width = max(150,self.get_max_width())
        self.block_width = self.width
        self.size_manage()
        if self.upper_code:
            try:
                self.upper_code.set_size_para(self, self.upper_code.parameter_buffer.index(self))
            except:
                pass
            self.upper_code.reset_para_size()
        if self.hook:
            self.hook.reset_para_size()
        self.reset_height()
        self.content_update()
        pass

    def add_to_contain(self,target):
        self.contain.append(target)
        target.upper_code = self
        self.offset_height += target.block_height
        for target_below_code in target.below_code:
            target_below_code.upper_code = self
            self.contain.append(target_below_code)
            self.offset_height+=target.block_height
        target.below_code = []
        self.block_height = self.reset_height() #replace with function

        self.content_update()
        self.place_block()

    def add_to_below(self,target):
        self.below_code.append(target)
        target.upper_code = self
        for target_below_code in target.below_code:
            target_below_code.upper_code = self
            self.below_code.append(target_below_code)
        target.below_code = []
        self.content_update()
        self.place_block()

    def place_block(self):
        top_val = self.top
        left_val = self.left
        if self.IsContainer:
            y_change = self.top_part
            x_change = self.offset1
            for item in self.contain:
                item.top = y_change+top_val
                item.left = left_val + x_change
                item.place_block()
                y_change +=item.block_height
        y_change = self.block_height
        x_change = 0
        for item in self.below_code:
            item.top = y_change+top_val
            item.left = left_val+x_change
            item.place_block()
            y_change += item.block_height
        if self.HaveParameter and self.parameter_buffer:
            for para in self.parameter_buffer:
                if para:
                    index = self.parameter_buffer.index(para)
                    para.top = self.arg_buffer[index].top+self.top+1
                    para.left = self.arg_buffer[index].left + self.left+1
                    para.place_block()
                    self.code_container.update()
        if self.side_block:

            self.side_block.top = self.top
            self.side_block.left = self.left+self.block_width+1
            self.side_block.place_block()


    def code_parser(self):
        parsed_code = ""
        n_para = 0
        struct = iter(self.struct[1:])

        for pack_data in struct:
            kw,data = pack_data
            if kw == "code":
                parsed_code +=data
                pass
            elif kw == "bracket":
                parsed_code+=data
                pass
            elif kw == "arg":
                if isinstance(data,list):
                    _,adsb = next(struct)
                    for narg,data in enumerate(self.parameter_buffer):
                        if data:
                            parsed_code+=data.code_parser()
                            parsed_code+=adsb
                        elif self.arg_buffer[narg].content.value:
                            parsed_code+=str(text_tranform(check_type(self.arg_buffer[narg].content.value)))
                            parsed_code+=adsb
                    parsed_code = parsed_code[:-1]
                else:
                    next(struct)
                    if self.parameter_buffer[n_para]:
                        value = self.parameter_buffer[n_para].code_parser()
                        parsed_code += value
                    else:
                        value = self.arg_buffer[n_para].content.value
                        parsed_code += str(text_tranform(check_type(value)))
                    n_para+=1
                pass
            elif kw == "adsb":
                parsed_code+=data
                pass
            elif kw == "end":
                parsed_code+=data
                pass
            elif kw == "name":
                parsed_code+=self.code
                pass
            elif kw == "data":
                if isinstance(self.code,str):
                    parsed_code+='"'+self.code+'"'
            else:
                parsed_code+=""
                pass

        return parsed_code

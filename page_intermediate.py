import blocklogic as b
import UI
import function_ui.function_ui as fu
import container.for_edit as fe
import flet as ft

page:ft.Page = None
restriction_area:ft.Container = None
edit_target = None
global_data = None
def set_page(page_data):
    global page,restriction_area
    page = page_data
    restriction_area = ft.Container(width=page.width,height=page.height,bgcolor="BLACK",opacity=0.5)
def func_sig():
    pass
def for_sig():
    pass
def load_data(data,target:fu.function_UI):
    target.load_data(data)

def get_signal_block(data,type = "func",target=None):

    global edit_target,global_data

    edit_target = target
    global_data = data

    if type == "func":
        function_ui = fu.function_UI(page.width)
        load_data(data,target=function_ui)
        open_window(function_ui)
    else:
        for_ui = fe.function_UI(page.width)
        load_data(data,target=for_ui)
        open_window(for_ui)
    page.update()
def open_window(target:ft.Container):

    target_wid = target.width if target.width else page.width
    if target.height:
        target_hei = target.height
    else:
        target_hei = page.height

    center_wid = (page.width-target_wid)/2
    center_hei = (page.height-target_hei)/2
    target.top =  center_hei
    target.left = center_wid

    page.overlay.append(restriction_area)
    page.overlay.append(target)

def close_overlay(target):
    page.overlay.remove(target)
    page.overlay.remove(restriction_area)
    page.update()
def send_signal_block(data,type="func"):
    ori_npara, ori_para_data, ori_block_struct = global_data
    #send signal to block
    if type=='func':
        code_name,func_name,para_data = data
        npara = len(para_data)

        temp,main_data = ori_block_struct['struct'][0]
        style_data = ori_block_struct['style']

        main_data = "def "+code_name
        ori_block_struct['struct'][0] = (temp,main_data)
        style_data[1] = ('text',func_name)
        for i in range(npara-ori_npara):
            style_data.insert(-1,('para', None))
        ori_npara = npara
        new_para_data = []
        for n,p_data in enumerate(para_data):
            para_name,para_dval = p_data
            arg = {'style': [('text', '')],
                   'color': '#FF6A00', 'text color': '#000000',
                   'block type': 'variable', 'block name': 'variable',
                   'block setting': [],
                   'struct': [('name', None), ('def_val', None)]
                   }
            arg['style'][0] = ('text',para_name)
            arg['struct'][1] = ('def_val', para_dval)
            new_para_data.append(arg)
        repacked_data = ori_npara,new_para_data,ori_block_struct
        edit_target.read_data(repacked_data)
    else:
        ori_npara = len(data)+1
        new_para_data = []
        ori_block_struct['style'] = [('text', 'for'), ('text', 'in'), ('para', None), ('btn', None)]
        ori_block_struct['struct'] = [('code', 'for '), ('code', 'in '), ('arg', None), ('adsb', ':')]
        for index,item in enumerate(data):
            arg = {'style': [('text', '')],
                   'color': '#FF6A00', 'text color': '#000000',
                   'block type': 'variable', 'block name': 'variable',
                   'block setting': [],
                   'struct': [('name', None), ('def_val', None)]
                   }
            arg['style'][0] = ('text',item)
            new_para_data.append(arg)
            ori_block_struct['style'].insert(1,('para',None))
            if index==0:
                ori_block_struct['struct'].insert(1,('adsb', '  '))
            else:
                ori_block_struct['struct'].insert(1, ('adsb', ' , '))
            ori_block_struct['struct'].insert(1, ('arg', None))

        repacked_data = ori_npara,new_para_data,ori_block_struct
        print(new_para_data)
        print(ori_block_struct)
        edit_target.read_data(repacked_data)
    pass

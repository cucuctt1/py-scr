import flet as ft
import stack as st
import blocklogic as b
import default_block_struct as dbs
import start_parse as sp
import block_manage as bm
import page_intermediate as pi
def main(page:ft.Page):
    page.window_maximized=False

    #stack.add_block(block=card2)
    #stack.add_block(block=card3)
    stack = st.stack_buffer()
    con = ft.Container(width=30,bgcolor="BLACK")
    r = ft.Row([con,stack])
    start_btn = ft.FilledButton(text="start",width=100,height=30,on_click=lambda e:sp.start_parse(stack))

    add_print = ft.FilledButton(text="add print",width=150,height=30,on_click=lambda e:bm.add_print(stack,page))
    add_data = ft.FilledButton(text="data",width=150,height=30,on_click=lambda e:bm.add_variable(stack))
    add_add = ft.FilledButton(text="add",width=150,height=30,on_click=lambda e:bm.add_add(stack))
    add_assign = ft.FilledButton(text="assign", width=150, height=30, on_click=lambda e: bm.add_assign(stack))
    add_def = ft.FilledButton(text="def", width=150, height=30, on_click=lambda e: bm.add_def(stack))
    add_for = ft.FilledButton(text="for", width=150, height=30, on_click=lambda e: bm.add_for(stack))
    add_if = ft.FilledButton(text="if", width=150, height=30, on_click=lambda e: bm.add_if(stack))
    star = ft.FilledButton(text="start2", width=100, height=30, on_click=lambda e: print(page.overlay))
    btn_holder = ft.Row(controls=[add_print,add_add,add_data,add_assign,add_def,add_for,start_btn,star,add_if],spacing=10,wrap=True)
    block2 = b.block(isheader=True,x=30, y=30, color=ft.colors.RED, content=None, code_container=stack,id=1)
    stack.add_block(block2)

    stack2 = st.stack_buffer()
    #data = b.block(x=190, y=190, color=ft.colors.GREY, content=None, code_container=stack2, id="level 3 block",
                   #struct=None, have_parameter=True, Npara=1, code="print", args=True)
    pi.set_page(page)
    stack2.add_block(btn_holder)
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.overlay.append(r)
    page.add(stack2)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
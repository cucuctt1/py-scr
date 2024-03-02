import flet as ft
import stack as st
import blocklogic as b
import default_block_struct as dbs

def main(page:ft.Page):
    page.window_maximized=False

    #stack.add_block(block=card2)
    #stack.add_block(block=card3)
    stack = st.stack_buffer()

    #content = ft.Container(height=30,width=150,content=ft.Text("test"),bgcolor=ft.colors.AMBER)
    block1 = b.block(iscontainer=True,x=30, y=0, color=ft.colors.ORANGE, content=None, code_container=stack, have_parameter=True,id=2,Npara=2)


    block5 = b.block( x=235, y=65, color=ft.colors.GREEN, content=None, code_container=stack, id="level 1 block",code="print test",struct=dbs.data_struct)
    block6 = b.block( x=235, y=65, color=ft.colors.GREEN, content=None, code_container=stack, id="level 1 block",code="print sss",struct=dbs.data_struct)
    block3 = b.block(x=190, y=190, color=ft.colors.GREY, content=None, code_container=stack, id="level 3 block",struct = dbs.print_struct,have_parameter=True,Npara=1,code="print",args=True)
    block4 = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",have_parameter=True,Npara=2,struct=dbs.add_struct)
    block7 = b.block(x=130, y=65, color=ft.colors.TEAL, content=None, code_container=stack, id="level 2 block",have_parameter=True,Npara=2,struct=dbs.add_struct)
    block8 = b.block(x=235, y=65, color=ft.colors.GREEN, content=None, code_container=stack, id="level 1 block",
                     code="add sss", struct=dbs.data_struct)

    block2 = b.block(isheader=True,x=30, y=30, color=ft.colors.RED, content=None, code_container=stack,id=1)
    stack.add_block(block1)
    stack.add_block(block2)
    stack.add_block(block3)
    stack.add_block(block6)
    stack.add_block(block8)
    stack.add_block(block7)
    stack.add_block(block4)
    stack.add_block(block5)

    #block1.add_to_contain(block3)

    block2.add_to_below(block1)

    #block2.add_block(block3)

    #block2.add(block3)

    page.add(stack)
    stack.slot_update()
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
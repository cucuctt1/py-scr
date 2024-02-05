import flet as ft
import startblock as stbl
import codeblock as cb
import stack as st
import container_block as ctb
import block as b

def main(page:ft.Page):
    page.window_maximized=False

    #stack.add_block(block=card2)
    #stack.add_block(block=card3)
    stack = st.stack_buffer()
    #startblock = stbl.start_block(0,0,stack,1)
    # block2 = cb.code_block(None,None,stack,startblock,2)
    # block3 = cb.code_block(None,None,stack,startblock,3)
    # block4 = cb.code_block(None,None,stack,startblock,4)
    # block5 = cb.code_block(None, None, stack, startblock, 5)
    # block6 = ctb.container_block(None,None,stack,startblock,6)
    # block7 = ctb.container_block(None, None, stack, startblock, 7)
    # stack.add_block(block3)
    # stack.add_block(block2)
    #stack.add_block(startblock)
    # stack.add_block(block4)
    # stack.add_block(block5)
    # stack.add_block(block6)
    # stack.add_block(block7)
    # startblock.add(block2)
    # startblock.add(block3)
    # startblock.add(block4)
    # startblock.add(block5)
    # startblock.add(block6)
    # startblock.add(block7)

    content = ft.Container(height=30,width=150,content=ft.Text("test"),bgcolor=ft.colors.AMBER)
    block1 = b.block(iscontainer=True,x=30, y=0, color=ft.colors.AMBER, content=content, code_container=stack, id=2)
    content = ft.Container(height=30, width=150, content=ft.Text("test"), bgcolor=ft.colors.RED)
    block3 = b.block(x=190, y=190, color=ft.colors.AMBER, content=content, code_container=stack, id=3)

    content = ft.Container(height=30, width=150, content=ft.Text("test"), bgcolor=ft.colors.GREEN)

    block2 = b.block(isheader=True,x=30, y=30, color=ft.colors.AMBER, content=content, code_container=stack)
    stack.add_block(block1)
    stack.add_block(block2)
    stack.add_block(block3)
    block1.add_to_contain(block3)
    block2.add_to_below(block1)

    #block2.add_block(block3)

    #block2.add(block3)
    page.add(stack)

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
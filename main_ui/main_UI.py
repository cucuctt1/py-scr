import time

import flet as ft
import vertical_tab.vertical_tab as vt
import console.console_UI as c
from utility.color_palette import *
import time as t
def main(page: ft.Page):

    page.window_maximized = False

    vtab = vt.vertical_tab(tab_color="#AA00AA",render_color=white_3,select_color=white,wid=300,select_index=2,hei=page.height,tabs=[vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.DATASET)),content=ft.Text("homo")),
                                               vt.tab(tab=ft.Container(content=ft.Icon(name=ft.icons.ADD)),content=ft.Text("no homo"))])
    st = ft.Stack(width=page.width-300,height=page.height-300)
    con = c.console(wid=page.width,hei=300)


    ver = ft.Column([st,con],spacing=0)
    fh = ft.Row([vtab,ver],spacing=0)
    def change_size():
        hei,wid = page.height,page.width
        print(hei,wid)
        vtab.height = hei
        st.width = page.width-300
        st.height = page.height-300
        con.width = page.width-300
        vtab.update()
        st.update()
        con.update()
        ver.update()
        fh.update()
        page.update()
    def dd(e):
        change_size()
    page.on_window_event = dd
    #page.on_window_event = on_resize
    page.add(fh)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
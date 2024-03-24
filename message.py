import flet
from flet import *


class btn(flet.IconButton):
    def __init__(self, func, height, icon, color, data):
        super().__init__()
        self.func = func
        self.height = height
        self.icon = icon
        self.color = color
        self.on_click = self.func
        self.data = data

        self.content = flet.Row(
            controls=[
                Container(
                    on_click = self.func,
                    expand=True,
                    height=self.height,
                    content=Icon(
                        self.icon,
                        color=self.color
                    ),
                    data=self.data,
                )
            ]
        )


class Application(UserControl):
    def __init__(self, pg: Page):
        super().__init__()

        self.pg = pg
        self.animation_style = animation.Animation(500, AnimationCurve.DECELERATE)
        self.init_helper()

    def switch_page(self, e, point):
        print(point)
        for page in self.switch_control:
            self.switch_control[page].offset.x = 2
            self.switch_control[page].update()

        self.switch_control[point].offset.x = 0
        self.switch_control[point].update()

        self.indicator.offset.y = e.control.data
        self.indicator.update()

    def init_helper(self):
        self.page1 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='blue',
            content=Text('PAGE 1', size=50)
        )

        self.page2 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='green',
            content=Text('PAGE 2', size=50)
        )

        self.page3 = Container(
            alignment=alignment.center,
            offset=transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor='orange',
            content=Text('PAGE 3', size=50)
        )

        self.switch_control = {
            'page1': self.page1,
            'page2': self.page2,
            'page3': self.page3,
        }

        self.indicator = Container(
            bgcolor='red',
            width=5,
            height=40,
            offset=transform.Offset(0, 0),
            animate_offset=animation.Animation(500, AnimationCurve.DECELERATE)
        )

        self.side_bar_column = Column(
            spacing=0,
            controls=[
                btn(func=lambda e:self.switch_page(point='page1'), height=40, icon=icons.LIGHTBULB, color='blue', data=0),
                btn(func=lambda e:self.switch_page(point='page2'), height=40, icon=icons.LOOP, color='blue', data=1)
            ]
        )

        self.pg.add(
            # The main page
            Container(
                padding=padding.only(top=30),
                expand=True,
                bgcolor='red',
                content=Row(
                    spacing=0,
                    controls=[
                        # side bar
                        Container(
                            # padding=padding.only(top=30),
                            bgcolor='white',
                            width=50,
                            content=Row(
                                spacing=0,
                                controls=[
                                    Column(
                                        spacing=0,
                                        expand=True,
                                        controls=[
                                            Container(
                                                expand=True,
                                                content=self.side_bar_column
                                            ),
                                            Container(
                                                content=Column(
                                                    controls=[
                                                        self.indicator,
                                                    ]
                                                )
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ),

                        # block bar
                        Container(
                            expand=True,
                            content=Stack(
                                controls=[
                                    self.page1,
                                    self.page2,
                                    self.page3,
                                ]
                            )
                        ),

                        # workspace
                        # idc this tho
                        Container(
                            bgcolor='yellow',
                            expand=True
                        )
                    ]
                )
            )
        )


# if __name__ == "__main__":
flet.app(target=Application)
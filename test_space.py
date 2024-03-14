from pynput.mouse import Listener

def is_clicked(x, y, button, pressed):
    if button and not pressed:
        print(pressed)
        return False # to stop the thread after click

with Listener(on_click=is_clicked) as listener:
    listener.join()
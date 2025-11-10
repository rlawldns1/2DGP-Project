from pico2d import *
import logo_mode


width = 1280
height = 720
open_canvas(width,height)

logo_mode.init()

while logo_mode.running:
    logo_mode.handle_events()
    logo_mode.update()
    logo_mode.draw()
    delay(0.1)

logo_mode.finish()
close_canvas()
from pico2d import *
import play_mode


width = 1280
height = 720
open_canvas(width,height)

play_mode.init()

while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    delay(0.1)

play_mode.finish()
close_canvas()
from pico2d import *
import logo_mode
import game_framework


width = 1280
height = 720
open_canvas(width,height)

game_framework.run(logo_mode)
close_canvas()
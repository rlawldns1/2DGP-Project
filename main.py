from pico2d import *
import tournament_mode as start_mode
import game_framework


width = 1280
height = 720
open_canvas(width,height)

game_framework.run(start_mode)
close_canvas()
from pico2d import *



open_canvas()

p = load_image('punch_1.png')

frame = 0
for x in range(0,800,5):
    clear_canvas()
    p.clip_draw(frame*128,0,128,128,x,90)
    update_canvas()
    frame = (frame + 1) % 5
    delay(0.1)

close_canvas()
# Render a 2D grid of 1s and 0s into a graphical QR code

import turtle as t

CANVAS_SIZE = 600


def _square(x, y, size):
    t.penup()
    t.setpos(x, y)
    t.pendown()
    t.setheading(0)
    t.begin_fill()
    for i in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()


def draw_grid(qr_modules):
    t.tracer(0)  # turn off animation for max speed
    t.hideturtle()

    t.Screen().setup(CANVAS_SIZE, CANVAS_SIZE)
    t.Screen().title('QR Code')
    t.color('BLACK')
    module_size = CANVAS_SIZE/(len(qr_modules)+8)  # assuming square grid and leaving 4 modules margin on each side
    top = CANVAS_SIZE//2 - 4 * module_size
    left = -top

    for row in range(len(qr_modules)):
        for col in range(len(qr_modules[0])):
            # DEBUG check for any unallocated squares - remove when working
            # if qr_modules[row][col] == 8:
            #     t.color('green')
            # else:
            #     t.color('black')

            if qr_modules[row][col]:
                _square(left + col * module_size, top - row * module_size, module_size)

    t.update()
    t.exitonclick()

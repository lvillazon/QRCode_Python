# Generate QR codes
# This is intended as a v2 attempt,
# based on what I have learned from my Java project
# but it is not intended as a straight port and will try to use more
# efficient table-driven algorithms
import time
from enum import Enum
from visualiser import draw_grid
from qr_code import generate_qr_code

Module = Enum('Module', ['BLACK', 'WHITE'])

# generate a known QR code to validate
if __name__ == '__main__':
    print('Python QR Code generator')
    #draw_grid(generate_qr_code('HELLO WORLd'))
    start = time.monotonic_ns()
    qr_code = generate_qr_code('the quickest brownest fox yobrownest fox you ever u ever brownest fox you ever did see w')
    duration = (time.monotonic_ns() - start)//10000000
    print("Completed in {:d}ms".format(duration))
    draw_grid(qr_code)

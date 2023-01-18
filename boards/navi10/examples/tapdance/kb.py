import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.D10, board.MOSI, board.MISO, board.D8)
    col_pins = (
        board.D4,
        board.D7,
        board.SCK,
    )
    diode_orientation = DiodeOrientation.COLUMNS
    i2c = board.I2C
    led_pin = board.D9
    neopixel = board.NEOPIXEL

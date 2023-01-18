import neopixel

from kb import KMKKeyboard

from kmk.extensions.LED import LED
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.layers import Layers as _Layers
from kmk.modules.modtap import ModTap
from kmk.modules.tapdance import TapDance

Mydebug = False
Nav10 = KMKKeyboard()

pixelmap = {
            '000' : (0,   0,   0),
            '001' : (0,   0,   255),
            '010' : (0,   255, 0),
            '011' : (0,   255, 255),
            '100' : (255, 0,   0),
            '101' : (255, 0,   255),
            '110' : (255, 255, 0),
            '111' : (255, 255, 255)
           }


class Layers(_Layers):
    def __init__(self, leds, pixel):
        super().__init__()
        self._leds = leds
        self._pixel = pixel
        self._last_top_layer = 0
        self._pixel.brightness = 0.3
        self._pixel.fill((0, 0, 255))

    def set_leds(self, pixmap):
        self._pixel.fill(pixelmap[pixmap])
        if self._last_top_layer != 0:
            if Mydebug:
                print('led on')
            self._leds.set_brightness(0, leds=[0])
        else:
            if Mydebug:
                print('led off')
            self._leds.set_brightness(100, leds=[0])

    def after_hid_send(self, keyboard):
        super().after_hid_send(keyboard)
        if keyboard.active_layers[0] != self._last_top_layer:
            if Mydebug:
                print(keyboard.active_layers)
            self._last_top_layer = keyboard.active_layers[0]
            if Mydebug:
                print(f'switch layer to {self._last_top_layer}')
            a = b = c = '0'
            for x in keyboard.active_layers:
                if x == 0:
                    a = '1'
                if x == 1:
                    b = '1'
                if x == 2:
                    c = '1'
            pixmap = c + b + a
            self.set_leds(pixmap)


modtap = ModTap()
modtap.tap_time = 200
tapdance = TapDance()
tapdance.tap_time = 200

leds = LED(led_pin=[Nav10.led_pin], brightness=100)
pixel = neopixel.NeoPixel(Nav10.neopixel, 1)
Nav10.modules.append(Layers(leds, pixel))
Nav10.modules.append(modtap)
Nav10.modules.append(tapdance)
Nav10.extensions.append(leds)
Nav10.extensions.append(MediaKeys())

# Cleaner key names
_______ = KC.TRNS
XXXXXXX = KC.NO

TAPPY_KEY = KC.TD(
    # Tap once for switch to Media Keys or tap hold to Function Keys
    KC.MT(KC.TG(2), KC.TG(1))
)

Nav10.keymap = [
    [  # Nav Keys
        TAPPY_KEY,  KC.HOME,    KC.PGUP,
        KC.DELETE,  KC.END,     KC.PGDOWN,
        XXXXXXX,    KC.UP,      XXXXXXX,
        KC.LEFT,    KC.DOWN,    KC.RIGHT
    ],
    [  # Function Keys
        _______,    KC.PAUS,    KC.VOLU,
        KC.ENTER,   KC.MUTE,    KC.VOLD,
        XXXXXXX,    KC.SLCK,    XXXXXXX,
        _______,    _______,    _______
    ],
    [  # Media keys
        _______,    KC.TRNS,    KC.VOLU,
        XXXXXXX,    KC.MUTE,    KC.VOLD,
        XXXXXXX,    KC.MSTP,    XXXXXXX,
        KC.MPRV,    KC.MPLY,    KC.MNXT
    ],
]

if __name__ == '__main__':
    # Nav10.debug_enabled = True
    Nav10.go()

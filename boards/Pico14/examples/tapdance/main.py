from kb import KMKKeyboard
from kmk.extensions.LED import LED
from kmk.keys import KC
from kmk.modules.layers import Layers as _Layers
from kmk.modules.tapdance import TapDance

Mydebug = False
Pico14 = KMKKeyboard()

class Layers(_Layers):
    def __init__(self, leds):
        super().__init__()
        self._leds = leds
        self._last_top_layer = 0

    def set_leds(self, keyboard):
        if self._last_top_layer != 0:
            if Mydebug:
                print("led on")
            self._leds.set_brightness(100, leds=[0])
        else:
            if Mydebug:
                print("led off")
            self._leds.set_brightness(0, leds=[0])

    def after_hid_send(self, keyboard):
        super().after_hid_send(keyboard)
        if keyboard.active_layers[0] != self._last_top_layer:
            self._last_top_layer = keyboard.active_layers[0]
            if Mydebug:
                print(f"switch layer to {self._last_top_layer}")
            self.set_leds(keyboard)

tapdance = TapDance()
tapdance.tap_time = 200
leds = LED(led_pin=[Pico14.led_pin], brightness=0)
Pico14.modules.append(Layers(leds))
Pico14.modules.append(tapdance)
Pico14.extensions.append(leds)

TAPPY_KEY = KC.TD(
    # Tap once to toggle the layer
    KC.TG(1)
)

# Make this for better looking formatting...
______ = KC.TRNS
XXXXXX = KC.NO

Pico14.keymap = [[
  # Layer 0 QWERTY
    TAPPY_KEY,  KC.SLASH, KC.ASTERISK,
    KC.N7,      KC.N8,    KC.N9,
    KC.N4,      KC.N5,    KC.N6,
    KC.N1,      KC.N2,    KC.N1,
    KC.N0,      XXXXXX,   KC.DOT
  ], [
  # Layer 1
    ______,     ______,   ______,
    KC.HOME,    KC.UP,    KC.PGUP,
    KC.LEFT,    KC.ENTER, KC.RIGHT,
    KC.END,     KC.DOWN,  KC.PGDN,
    KC.INS,     XXXXXX,   KC.DEL
  ]
]

if __name__ == '__main__':
    Pico14.go()

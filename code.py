# Gemma IO demo
# Adafruit CircuitPython 4.0.0-beta.7 on 2019-04-13; Adafruit CircuitPlayground Express with samd21g18

from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut
from touchio import TouchIn
import adafruit_dotstar as dotstar
import board
import time

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.4)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Capacitive touch on A0 and A2
touch0 = TouchIn(board.A0)
touch2 = TouchIn(board.A2)


def wheel(pos):
    """Input a value 0 to 255 to get a color value.
    The colours are a transition r - g - b - back to r."""
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos * 3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos * 3), 0, int(pos * 3)]
    else:
        pos -= 170
        return [0, int(pos * 3), int(255 - pos * 3)]


RED = (255, 0, 0)
OFF = (0, 0, 0)


class Morse:
    PACE = 0.2
    CHARS = {
        '.': (1, RED),
        '-': (3, RED),
        ' ': (2, OFF),
    }

    def __init__(self, text):
        self.text = text

    def start(self):
        dot[0] = OFF
        dot.show()
        self.time = time.monotonic()
        self.pos = 0

    def next(self):
        if self.pos == len(self.text):
            dot[0] = OFF
            dot.show()
            time.sleep(Morse.PACE * 7)
            self.pos = 0
        else:
            delay, dot[0] = Morse.CHARS[self.text[self.pos]]
            dot.show()
            time.sleep(Morse.PACE * delay)
            dot[0] = OFF
            dot.show()
            time.sleep(Morse.PACE)
            self.pos += 1


CYCLE_SECONDS = 24  # seconds

# States
QUIET = 0
SOS = 1

# Initialization
mode = QUIET
sos_started = None
color_started = time.monotonic()
color = 0
message = Morse("... --- ...")

if __name__ == "__main__":
    button_down = None
    while True:
        now = time.monotonic()
        if mode == QUIET:
            if now - color_started > CYCLE_SECONDS / 256:
                dot[0] = wheel(color)
                color = (color + 1) % 256
                dot.show()
                color_started = now
        else:
            message.next()

        # Use A0 & A2 as capacitive touch to turn on internal LED
        if touch0.value and touch2.value and button_down is None:
            button_down = now
            led.value = True
        elif (touch0.value and touch2.value
              and button_down
              and now - button_down > 0.20
        ):
            led.value = False
        elif (
                not (touch0.value or touch2.value)
                and button_down
                and now - button_down > 0.20
        ):
            led.value = False
            button_down = None
            mode = QUIET if mode == SOS else SOS
            if mode == QUIET:
                color_started = now
                color = 0
                print("A0 & A2 touched - Quiet")
            elif mode == SOS:
                sos_started = now
                print("A0 & A2 touched - SOS")
                message.start()

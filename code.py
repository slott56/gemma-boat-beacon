# Gemma IO demo
# Adafruit CircuitPython 4.0.0-beta.7 on 2019-04-13; Adafruit CircuitPlayground Express with samd21g18
# V2 -- better FSA design.

from digitalio import DigitalInOut, Direction, Pull
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

RED = (255, 0, 0)
OFF = (0, 0, 0)

class Display:
    """Superclass for displays. This is actually off, and duration doesn't matter."""
    def __init__(self, duration):
        self.duration = duration
        self.started = None
        self.elapsed = None
    def start(self, clock):
        self.started = clock
        dot[0] = OFF
        dot.show()
    @property
    def running(self):
        return self.elapsed and self.elapsed < self.duration
    def now(self, clock):
        self.elapsed = clock-self.started

class ColorWheel(Display):
    @staticmethod
    def pos_color(pos):
        """Input a value 0 to 255 to get a color value.
        The colours are a transition g - r - b."""
        if (pos < 0):
            return [0, 0, 0]
        if (pos > 255):
            return [0, 0, 0]
        if (pos < 85):
            return [int(pos * 3), int(255 - (pos*3)), 0]
        elif (pos < 170):
            pos -= 85
            return [int(255 - pos*3), 0, int(pos*3)]
        else:
            pos -= 170
            return [0, int(pos*3), int(255 - pos*3)]
    @property
    def running(self):
        return True
    def now(self, clock):
        super().now(clock)
        step = int(256 * (self.elapsed % self.duration) / self.duration)
        dot[0] = self.pos_color(step)
        dot.show()

class SignalLevel(Display):
    """LED Level: Low or High. Uses global ``dot`` LED array."""
    def __init__(self, duration, color=OFF):
        super().__init__(duration)
        self.color = color
    def start(self, clock):
        super().start(clock)
        dot[0] = self.color
        dot.show()

Low = SignalLevel
High = SignalLevel

class Sequence(Display):
    """Duration a consequence of the sequence of steps."""
    def __init__(self, *steps):
        super().__init__(None)
        self.steps = steps
        self.pos = None
        self.current = None
    def start(self, clock):
        super().start(clock)
        self.pos = 0
        self.current= self.steps[self.pos]
        self.current.start(clock)
    @property
    def running(self):
        return self.pos != len(self.steps)
    def now(self, clock):
        super().now(clock)
        self.current.now(clock)
        if not self.current.running:
            self.advance(clock)
    def advance(self, clock):
        self.pos = self.pos + 1
        if self.running:
            self.current = self.steps[self.pos]
            self.current.start(clock)

class MorseElement(Sequence):
    """
    Superclass of Morse code elements: dot, dash, and space.
    """
    length = None
    color = OFF
    def __init__(self, pace):
        super().__init__(Low(pace), High(pace*self.length, self.color))

class Dot(MorseElement):
    length = 1
    color = RED

class Dash(MorseElement):
    length = 3
    color = RED

class Space(MorseElement):
    length = 2
    color = OFF

class End(MorseElement):
    length = 7
    color = OFF

class Morse(Sequence):
    PACE = 0.2
    CHARS = {
        '.': Dot,
        '-': Dash,
        ' ': Space,
    }
    def __init__(self, text):
        elements = [Morse.CHARS[c](self.PACE) for c in text] + [End(self.PACE)]
        super().__init__(*elements)
    def advance(self, clock):
        self.pos = (self.pos + 1) % len(self.steps)
        self.current = self.steps[self.pos]
        self.current.start(clock)

# class ButtonPairState:
#     """Candidate superclass for ButtonPair states"""
#     pressed = False
#     @staticmethod
#     def read(bp):
#         pass

class ButtonPairUp:
    pressed = False
    @staticmethod
    def read(bp):
        if bp.b1.value and bp.b2.value:
            bp.led.value = True
            ButtonPairDown.started = bp.now
            return ButtonPairDown
        return ButtonPairUp

class ButtonPairDown:
    pressed = False
    started = None
    @staticmethod
    def read(bp):
        if not bp.b1.value and not bp.b2.value:
            bp.led.value = False
            return ButtonPairDownUp
        else:
            if bp.now - ButtonPairDown.started > 0.25:
                bp.led.value = False
        return ButtonPairDown

class ButtonPairDownUp:
    pressed = True
    @staticmethod
    def read(bp):
        return ButtonPairDownUp

class ButtonPair:
    def __init__(self, b1, b2, led):
        self.b1 = b1
        self.b2 = b2
        self.led = led
        self.state = ButtonPairUp

    def press(self, now):
        self.now = now
        self.state = self.state.read(self)
        if self.state.pressed:
            # Consumed!
            self.state = ButtonPairUp
            return True

class QuietMode:
    display = Display(24)  # off
    @staticmethod
    def next():
        return ColorMode

class ColorMode:
    display = ColorWheel(24)
    @staticmethod
    def next():
        return SOSMode

class SOSMode:
    display = Morse("... --- ...")
    @staticmethod
    def next():
        return QuietMode

if __name__ == "__main__":
    # Initialization
    mode = ColorMode
    mode.display.start(time.monotonic())
    buttons = ButtonPair(touch0, touch2, led)

    while True:
        now = time.monotonic()
        mode.display.now(now)
        if buttons.press(now):
            mode = mode.next()
            mode.display.start(now)

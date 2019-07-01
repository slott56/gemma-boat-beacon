#################
gemma-boat-beacon
#################

A Gemma M0 app to act as a handy beacon.

For more information on the Gemma M0, see
https://www.adafruit.com/product/3501

There are two user stories here.

1.  When you've left your sailboat in an anchorage and plan to return after dark, it can be hard to find.
    All the sailboats are reduced to large, shadowy hulks when you're scooting through them in your little dinghy.
    How can you locate your boat?

    Answer. Distinctive lighting.

2.  When you've got a problem, and you're signaling an SOS, you need everything that makes light to be working at night.

    Answer. Your distinctive lighting should also have an SOS mode.

Here's how you can do this with a Gemma M0.

Finite State Automata
=====================

The code makes extensive use of the **State** design pattern. It shows two implementations of stateful processing.

-   The display has time-based state changes. This involves a fairly complex tree of class definitions.
    Each object is provided a ``now()`` with the current time. The subclasses of ``Display`` all transition
    from ``running`` to ``not running`` when some time has expired.

-   A ``Sequence`` subclass shares the ``now()`` method, but can advance through different states
    of display. The time is pushed down into subordinate objects until the finish running. Then
    an ``advance()`` method is used to move to the next display.

-   The button input has a touch-sensor-based state changes. The ``ButtonPair`` class hierarchy
    tracks touches on two of the touchpads. This uses touch to move to ``ButtonDown``. When released,
    it moves to ``ButtonDownUp``. Once this is consumed, the state can be reset to the
    starting state of ``ButtonUp``.

-   The overall operating mode (Color cycle, Red SOS, or Off) is also an automaton defined as three
    closely-related classes. Each of these classes uses a Display object, and has a function to return
    the next operating mode when a button press has been detected.

TODO
====

This version uses the capacitative touch to trigger SOS mode.
A future version will rely on an external push-button to trigger SOS mode.

Add photo with packaging options including external LED
and button.

Add supply to run from 12V boat power instead of batteries.

Add more formal unit tests.

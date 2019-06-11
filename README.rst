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

Unit Testing
============

::

    PYTHONPATH=.:mocks pytest tests.py


TODO
====

This version uses the capacitative touch to trigger SOS mode.
A future version will rely on an external push-button to trigger SOS mode.

Add photo with packaging options including external LED
and button.

Add supply to run from 12V boat power instead of batteries.

Add more formal unit tests.

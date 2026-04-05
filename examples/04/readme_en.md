# Buzzer for K230

This folder contains examples of working with the buzzer on the YAHBOOM K230 board.

## Description

A buzzer is a component that produces sound.
The K230 uses a passive buzzer controlled via PWM.

This means:
- you can control frequency (pitch)
- you can control duration

## Examples

- `04_1_basic_buzzer.py` — basic sounds and alarm pattern
- `04_2_melody_buzzer.py` — playing a melody

## Quick Start

```python
from ybUtils.YbBuzzer import YbBuzzer
buzzer = YbBuzzer()
buzzer.beep()
```

## Control

Main method:

```python
buzzer.on(frequency, volume, duration)
```

Example:

```python
buzzer.on(2000, 50, 0.5)
```

## Important

A passive buzzer requires a PWM signal,
so the sound depends on frequency.

Higher frequency → higher pitch.

## Tip

Always turn off the buzzer when done:

```python
buzzer.off()
```

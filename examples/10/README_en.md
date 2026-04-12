# Timer Examples for K230

## What is a Timer

**Timer** is a hardware or software mechanism that allows you to execute code at specific time intervals. Timers are useful for creating periodic tasks without blocking the main program flow.

### Basic Concepts

- **Timer(-1)** — virtual (software) timer. Used when high timing precision is not critical
- **ONE_SHOT** — one-shot mode. The timer triggers once and then stops
- **PERIODIC** — periodic mode. The timer triggers repeatedly at equal intervals
- **callback** — a function that is automatically called when the timer triggers

## How Timer Works

```python
from machine import Timer

# Create a timer
timer = Timer(-1)

# Option 1: Start by period (in milliseconds)
timer.init(period=100, mode=Timer.ONE_SHOT, callback=my_function)

# Option 2: Start by frequency (in Hertz)
timer.init(freq=5, mode=Timer.PERIODIC, callback=my_function)

# Stop the timer
timer.deinit()
```

## Examples in This Folder

| File | Description | Components Used |
|------|----------|-----------------|
| `01_timer_basic.py` | Basic example: one-shot and periodic modes | Timer |
| `02_timer_button.py` | Periodic button state checking | Timer, YbKey |
| `03_timer_uart.py` | Periodic UART data checking | Timer, YbUart |
| `04_timer_rgb.py` | RGB LED color switching | Timer, YbRGB |
| `05_timer_buzzer.py` | Periodic sound signals | Timer, YbBuzzer |

## Practical Timer Applications

- **Sensor polling** — periodic reading of sensor data
- **Device control** — blinking LEDs, controlling motors
- **Communication handling** — checking UART, I2C, SPI for incoming data
- **Background tasks** — scheduled actions without blocking main code
- **Creating animations** — switching states at regular intervals

## Running the Examples

Connect to the K230 board via Thonny IDE or another editor and run any script:

```python
# Run the button example
%run 02_timer_button.py

# After running, press the button on the board and observe the console output
```

## Tips for Beginners

1. **Timer frequency** — choose a reasonable frequency. Too high (e.g., 100 Hz) may overload the processor
2. **Callback functions** — keep them as short and fast as possible
3. **Global variables** — use `global` to preserve state between callback calls
4. **Stopping timers** — always call `deinit()` when the timer is no longer needed

## See Also

- [MicroPython Timer Documentation](https://docs.micropython.org/en/latest/library/machine.Timer.html)
- Other examples in the `examples/` folder

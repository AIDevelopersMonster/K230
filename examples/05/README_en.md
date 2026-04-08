# K230 Examples: Button, RGB LED, Speaker

Welcome! This folder contains **5 simple examples** to get started with the K230 board. 
Here you will learn how to control a button, LED, and speaker.

## 📚 What You Will Learn

- How to read button state
- How to control an RGB LED (different colors)
- How to play sounds through a speaker
- How to combine multiple components together

## 🛠️ Requirements

### Software
- Python 3.x
- `ybUtils` library (pre-installed on K230 board)

### Hardware
- K230 board
- Button (connected to GPIO61)
- RGB LED
- Speaker (buzzer)

## 📦 Installation

1. **Make sure Python is working on your board:**
   ```bash
   python --version
   ```

2. **Install the `ybUtils` library** (if not already installed):
   ```bash
   pip install ybUtils
   ```

3. **Connect the components:**

   | Component | Connection | Notes |
   |-----------|------------|-------|
   | Button | GPIO61 | Uses pull-up (PULL_UP) |
   | RGB LED | Board GPIO pins | Check type (common anode/cathode) |
   | Speaker | Through resistor | For board protection |

   > 💡 **Important about the button:** 
   > - Not pressed = logical "1" (high level)
   > - Pressed = logical "0" (low level)
   > - This is called "active low"

## 📋 Examples List

| # | File | Description | Difficulty |
|---|------|-------------|------------|
| 1 | [01_button_basic.py](01_button_basic.py) | Reads button state and prints to console | ⭐ Easy |
| 2 | [02_button_led.py](02_button_led.py) | Button turns LED on/off | ⭐⭐ Simple |
| 3 | [03_rgb_led.py](03_rgb_led.py) | Button cycles through 7 RGB colors | ⭐⭐ Simple |
| 4 | [04_speaker_basic.py](04_speaker_basic.py) | Button plays a beep sound | ⭐⭐ Simple |
| 5 | [05_button_rgb_speaker.py](05_button_rgb_speaker.py) | Combined: button + color + sound | ⭐⭐⭐ Medium |

## 🚀 How to Run

### Running an Example

Select an example and run:

```bash
python 01_button_basic.py
```

Or any other:
```bash
python 02_button_led.py
python 03_rgb_led.py
python 04_speaker_basic.py
python 05_button_rgb_speaker.py
```

### What You Will See

**Example 1 (button):**
```
Starting example: press the user button on K230 board
Button pressed!
Button pressed!
```

**Example 2 (button + LED):**
- LED lights up when button is pressed
- Turns off when you release the button

**Example 3 (RGB LED):**
- Each button press changes the color:
  - 🔴 Red → 🟢 Green → 🔵 Blue → 🟡 Yellow → 🔵 Cyan → 🟣 Magenta → ⬛ Off

**Example 4 (speaker):**
- Short beep sound when button is pressed

**Example 5 (combined):**
- Mode 0: 🔴 Red + beep sound
- Mode 1: 🟢 Green, no sound
- Mode 2: 🔵 Blue, no sound

## 🔧 Troubleshooting

### Problem: Button not responding
**Solution:**
- Check connection to GPIO61
- Make sure the button is working
- Verify pull-up is enabled

### Problem: No sound
**Solution:**
- Check speaker connections
- Make sure the speaker is working
- Check all contacts

### Problem: Wrong RGB colors
**Solution:**
- Check wire order (R, G, B)
- Find out LED type (common anode or cathode)
- Invert values if needed

## 📖 Key Concepts

### What is GPIO?
**GPIO** (General Purpose Input/Output) are universal pins on a microcontroller 
that can be programmed as input (reading) or output (control).

### What is Pull-up?
**Pull-up** is a resistor that connects a pin to power (+3.3V).
When the button is not pressed, the pin reads "1". When pressed, it connects to ground and reads "0".

### What is an RGB LED?
An **RGB LED** contains three LEDs in one package:
- **R** (Red)
- **G** (Green)  
- **B** (Blue)

By combining the brightness of each, you can create any color.

## 🎯 Next Steps

After studying these examples, try:
1. Change colors in example 3 to your favorites
2. Create a melody instead of a simple beep
3. Add a timer or button press counter
4. Combine examples with your own ideas!

## ❓ Questions?

If something is unclear:
- Re-read the comments in each example code
- Experiment with parameters
- Study the `ybUtils` documentation

Happy learning! 🎉

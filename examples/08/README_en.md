# PWM Examples for K230

## 📚 What is PWM?

**PWM (Pulse Width Modulation)** is a method of controlling signal power by changing the duration of pulses at a constant frequency.

### In Simple Terms:

Imagine you quickly turn a light on and off. If you keep it on for 50% of the time and off for 50% of the time, your eye perceives this as half brightness. PWM works exactly the same way!

### Key Concepts:

1. **Frequency (freq)** — how many times per second the signal turns on and off. Measured in Hertz (Hz).
   - Example: 1000 Hz = 1000 cycles per second

2. **Duty Cycle** — the percentage of time the signal is in the ON state.
   - 0% — signal is always OFF
   - 50% — signal is ON half the time
   - 100% — signal is always ON

### PWM Visualization:

```
100% duty: ████████████████████ (always ON)
50% duty:  ████████░░░░░░░░░░░░ (half the time)
25% duty:  ████░░░░░░░░░░░░░░░░ (quarter of the time)
0% duty:   ░░░░░░░░░░░░░░░░░░░░ (always OFF)
```

## 🔧 What is PWM Used For?

1. **LED Brightness Control** — changing duty cycle changes perceived brightness
2. **Motor Speed Control** — more power = faster rotation
3. **Sound Signal Generation** — changing frequency creates different notes
4. **Servo Motors** — precise position control

## 📌 Pins on Yahboom K230 Board

| Pin | Function |
|-----|----------|
| IO42 | PWM0 |
| IO43 | PWM1 |

## 🚀 How to Run Scripts?

### Method 1: Using Thonny IDE (Recommended for Beginners)

1. Install [Thonny IDE](https://thonny.org/)
2. Connect the K230 board to your computer via USB
3. In Thonny, select: `Tools → Options → Interpreter → MicroPython (K230)`
4. Open the `.py` file and click the "Run" button (▶️)

### Method 2: Via Command Line (REPL)

1. Connect to the board via serial port (e.g., PuTTY or screen)
2. Connection speed: 115200 baud
3. Copy the script code into the terminal or upload the file to the board
4. Run with command: `import filename` (without .py)

### Method 3: Upload File to Board

1. Save the script to the board's main directory
2. Rename to `main.py` for automatic startup on boot
3. Or run manually via `import`

## 📁 Example Descriptions

| File | Description | What You Learn |
|------|-------------|----------------|
| `01_pwm_basic.py` | Basic PWM signal | Creating simple PWM signals |
| `02_pwm_led_fade.py` | LED fade effect | Loops, changing duty cycle |
| `03_pwm_button_control.py` | Button control | Working with buttons, conditions |
| `04_pwm_uart_control.py` | UART control | Receiving data, error handling |
| `05_pwm_music.py` | Simple melody | Changing frequency for sound |

## 💡 Tips for Beginners

1. **Start with the first example** — it's the simplest and shows the basics
2. **Experiment with parameters** — change `freq` and `duty`, observe results
3. **Connect an LED** — to pin IO42 through a resistor (220 Ohm) for visual feedback
4. **Read code comments** — they explain each line in detail
5. **Don't be afraid to make mistakes** — if something doesn't work, check connections and parameters

## 🔗 Useful Links

- GitHub Repository: https://github.com/AIDevelopersMonster/K230
- K230 Documentation: 

---
*Author: AIDevelopersMonster*

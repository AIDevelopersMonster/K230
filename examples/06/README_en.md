# UART Examples for K230

This folder contains **UART** (Universal Asynchronous Receiver-Transmitter) examples for the K230 board.  
These examples will help you understand how to transmit data between devices.

---

## 📚 What is UART?

**UART** is a simple way to exchange data between two devices using just two wires.

### How it works:
- One device sends data through **TX** (transmit pin)
- Another device receives through **RX** (receive pin)
- And vice versa — for the response

### 🔌 Wiring Connection

To connect two devices, wire them **crosswise**:

| Device 1 | → | Device 2 |
|----------|---|----------|
| TX       | → | RX       |
| RX       | → | TX       |
| GND      | → | GND      |

⚠️ **Important:** Do NOT connect TX to TX or RX to RX!

### ⚙️ Communication Settings

Both devices must use the same settings:
- **Baudrate (Speed):** 115200 bits/sec
- **Data bits:** 8
- **Stop bits:** 1
- **Parity:** None

---

## 🛠 What You'll Need

- K230 board
- USB-UART adapter (e.g., CP2102, CH340, FTDI)
- Jumper wires for connection
- Terminal program on your computer:
  - **Windows:** PuTTY, Tera Term, Arduino IDE (Serial Monitor)
  - **Linux/macOS:** `screen`, `minicom`, `picocom`

---

## 🚀 How to Run the Examples

1. **Connect the hardware:**
   - Wire K230 to the UART adapter using the diagram above
   - Connect the adapter to your computer via USB

2. **Find the port name:**
   - **Windows:** COM3, COM4, etc. (check Device Manager)
   - **Linux:** `/dev/ttyUSB0`, `/dev/ttyACM0`
   - **macOS:** `/dev/tty.usbserial-*`

3. **Open the terminal:**
   ```bash
   # Linux/macOS example
   screen /dev/ttyUSB0 115200
   
   # Or in PuTTY, specify the port and baudrate 115200
   ```

4. **Upload the script to K230** and run it

5. **Send commands** from the terminal and observe the results

---

## 📁 Example Descriptions

| File | What it does | Useful for |
|------|--------------|------------|
| `01_uart_basic.py` | Sends a greeting and displays incoming data | First step — test the connection |
| `02_uart_echo.py` | Repeats (echoes) all received messages | Testing receive and transmit |
| `03_uart_button.py` | Sends a message when button is pressed | Monitoring events from the board |
| `04_uart_rgb_control.py` | Changes RGB LED color by command | Remote device control |
| `05_uart_buzzer_music.py` | Plays sounds by command | Alarms, notifications |

---

## 💡 Example Commands

### For `04_uart_rgb_control.py`:
Send one of these commands in the terminal:
```
red      → red light
green    → green light
blue     → blue light
off      → turn off light
```

### For `05_uart_buzzer_music.py`:
```
beep     → short beep sound
alarm    → alarm signal (3 beeps)
```

---

## ❓ Common Issues

| Problem | Solution |
|---------|----------|
| Nothing appears | Check TX↔RX wiring, ensure baudrate is 115200 |
| Garbled text | Wrong baudrate on one of the devices |
| Port not found | Check UART adapter drivers, reconnect the cable |

---

## 📖 What's Next?

Try to:
- Change the baudrate
- Send your own custom messages
- Create a dialogue between two boards
- Add new commands for device control

Happy learning UART! 🎉

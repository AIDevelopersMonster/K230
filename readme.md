# K230 MicroPython Examples

This repository is a practical collection of MicroPython examples for the Yahboom K230 platform. It is organized as a step-by-step learning path: starting with REPL and Python basics, then moving into pin mapping, GPIO, UART, I2C, PWM, timers, watchdog usage, and simple peripheral projects with LEDs, buttons, buzzers, speakers, and OLED displays.

The project is aimed at beginners who want short, focused examples they can run directly on a K230 board and then combine into larger embedded experiments.

## What this repository includes

- Introductory REPL and Python learning materials for K230 users
- Simple FPIOA and pin-configuration examples
- Peripheral demos for RGB LEDs, buzzers, buttons, speakers, UART, and OLED
- Incremental exercises that build from single-device control to small combined systems
- Topic-based folders with matching markdown explanations and runnable `.py` files

## Repository structure

The main content lives under `examples`.

| Folder | Topic |
|------|------|
| `01` | REPL basics and Python onboarding for K230 |
| `02/01` | FPIOA, GPIO, UART, and I2C pin-mapping basics |
| `03` | RGB LED examples |
| `04` | Buzzer and melody examples |
| `05` | Button, LED, RGB, and speaker interaction |
| `06` | UART communication examples |
| `07` | I2C and OLED display examples |
| `08` | PWM examples |
| `09` | Watchdog timer examples |
| `10` | Timer-based examples |

## How to use it

1. Prepare a Yahboom K230 board with a compatible MicroPython or CanMV environment.
2. Open the chapter that matches the topic you want to learn.
3. Read the local `README.md` or `README_en.md` in that folder for wiring notes and context.
4. Copy a `.py` example to the board and run it.
5. Modify the example and combine it with others once the basic version works.

If you are completely new to the platform, start with `examples/01` and then continue through the numbered folders in order.

## Learning approach

The examples are intentionally small and progressive. Most folders start with a minimal hardware test and then add interaction between modules, such as:

- button to LED control
- UART to RGB control
- buzzer and RGB synchronization
- OLED status display driven by inputs or serial data

This makes the repository useful both as a tutorial and as a reference when building your own K230 projects.

## Notes

- The examples are hardware-oriented and assume access to the relevant K230 pins and peripherals.
- Some folders include both local-language and English documentation files.
- Wiring and available pins can vary by board revision, so always verify the pinout before connecting external modules.

## License

This repository is distributed under the terms of the `LICENSE` file in the project root.

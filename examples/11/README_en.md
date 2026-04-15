# FFT for K230

## 📚 What is Fourier Transform

**Fourier Transform (FT)** is a mathematical method to convert a signal from the time domain to the frequency domain. In other words, it shows what frequencies make up your signal.

**FFT (Fast Fourier Transform)** is a fast algorithm for computing the Fourier Transform, allowing real-time calculations on microcontrollers.

## 💡 Simple Explanation

Imagine you're listening to a guitar chord. Your ear automatically distinguishes individual notes in that chord. FFT does the same thing with any signal:

- **Input**: A signal changing over time (like a sound wave)
- **Output**: A list of frequencies with their amplitudes (which "notes" are present and how loud they are)

Any complex signal can be broken down into a set of simple sine waves. FFT shows which frequencies are in the signal and their intensity.

## 🔧 FFT Applications

- **Audio Analysis** — note recognition, music frequency analysis
- **Noise Filtering** — extracting useful signals from noise
- **Signal Processing** — medical equipment, radio communications
- **Spectral Analysis** — visualizing frequency spectrum
- **Vibration Analysis** — machinery diagnostics
- **Speech Recognition** — extracting characteristic frequencies

## 📁 Examples Structure

| File | Description | Used Modules |
|------|----------|---------------------|
| `01_fft_basic.py` | Basic FFT example. Generates test signal and outputs frequency amplitudes | FFT, ulab.numpy |
| `02_fft_uart.py` | Receives data via UART and performs FFT analysis | YbUart, FFT, ulab.numpy |
| `03_fft_rgb.py` | Controls RGB LED based on FFT results | YbRGB, FFT, ulab.numpy |
| `04_fft_buzzer.py` | Sound indication via buzzer when amplitude threshold is exceeded | YbBuzzer, FFT, ulab.numpy |

## 🚀 Quick Start

### Running the Basic Example

```python
# Connect to K230 board and run:
python 01_fft_basic.py
```

You will see an array of amplitudes for each frequency in the signal.

### Understanding Results

FFT result is an array of numbers where each element corresponds to a specific frequency amplitude:
- First element (index 0) — DC offset (constant component)
- Remaining elements — amplitudes of increasing frequencies

## ⚙️ FFT Parameters

When creating an FFT object, three parameters are specified:

```python
fft = FFT(arr, N, 0x555)
```

- **arr** — signal data array (uint16 type)
- **N** — sample size (must be a power of two: 64, 128, 256...)
- **0x555** — Hamming window parameter for improved analysis accuracy

## 📝 Tips for Beginners

1. **Sample Size**: Use powers of two (64, 128, 256) for correct FFT operation
2. **Sampling Rate**: Higher sampling rate allows analyzing higher frequencies
3. **Threshold Values**: Adjust experimentally for your specific task
4. **Hamming Window**: Parameter 0x555 reduces frequency "leakage" and improves accuracy

## 🔗 Additional Resources

- [FFT Documentation](https://docs.k230.com/)
- [Wikipedia: Fourier Transform](https://en.wikipedia.org/wiki/Fourier_transform)
- [GitHub Repository](https://github.com/AIDevelopersMonster/K230)

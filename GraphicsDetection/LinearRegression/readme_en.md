# Linear Regression (K230)

## 📌 Description

This module demonstrates the use of the linear regression function `img.get_regression()` for detecting and tracking lines in camera images. This is the foundation for building line-following robots.

📖 Based on the K230 documentation example (line patrol) — the camera looks at a black line on a white background.

---

## 🚀 Quick Start

### Requirements
- Yahboom K230 board
- Camera connected to K230
- ST7701 display (optional, for visualization)

### Installation
1. Copy the `.py` files to the SD card or internal memory of K230
2. Connect the camera to the board
3. Run the desired script via IDE or directly on the device

---

## 🧪 Examples

| File | Description | For Whom |
|------|----------|----------|
| `01_linear_regression_camera.py` | Basic line detection from camera | Beginners |
| `02_linear_regression_binary.py` | Line detection with binary thresholding | Advanced |
| `03_line_following_pid.py` | Error calculation for robot control | Robotics |

### Script Descriptions

#### 01_linear_regression_camera.py
Basic example:
- Captures grayscale image from camera
- Searches for dark line using linear regression
- Draws detected line on screen
- Shows "magnitude" (detection quality)

**What is magnitude?**  
The higher the value, the better the line is visible and more pixels are detected in the area.

#### 02_linear_regression_binary.py
Improved version:
- Applies binary thresholding before line detection
- All pixels are divided into black (0) and white (255)
- Improves stability in poor lighting
- Removes noise and unnecessary details

**Why binary thresholding?**  
It simplifies the image, keeping only important contours. Like making a photocopy — only black and white remain.

#### 03_line_following_pid.py
For robotics:
- Finds the line and calculates its center
- Compares with screen center
- Outputs error (deviation from center)
- Ready for use in PID controller

**How to use error?**
- `error > 0` — line is to the right, turn right
- `error < 0` — line is to the left, turn left
- `error = 0` — line is centered, go straight

---

## 🧠 How Linear Regression Works

### Algorithm

1. **Image Capture**  
   Camera captures a grayscale frame (640x480 pixels)

2. **Threshold Filtering**  
   Select pixels in brightness range (e.g., 0-100 for dark pixels)

3. **Region Detection**  
   Find connected region of matching pixels

4. **Least Squares Method**  
   Build a straight line that best fits through the detected pixels

5. **Result**  
   Get coordinates of line start (x1, y1) and end (x2, y2)

### Visualization

```
Camera → [Image] → [Threshold] → [Binary] → [Regression] → Line
                                                      ↓
                                            (x1,y1) ─────── (x2,y2)
```

---

## ⚙️ Parameter Configuration

### Threshold (THRESHOLD)

```python
THRESHOLD = (0, 100)    # For black line on white background
THRESHOLD = (150, 255)  # For white line on black background
```

**How to adjust threshold:**
1. Run the script
2. Look at the camera image
3. If line is not detected — increase the range
4. If too much noise — decrease the range

### Resolution

```python
sensor.set_framesize(width=640, height=480)  # VGA
sensor.set_framesize(width=320, height=240)  # QVGA (faster)
```

**Resolution impact:**
- Higher resolution → better accuracy, slower processing
- Lower resolution → lower accuracy, higher FPS

---

## 🤖 Robot Application

### Simple Control Logic

```python
if line:
    x_center = (line.x1() + line.x2()) / 2
    error = x_center - 320  # 320 = half screen width
    
    if error > 20:
        turn_right()    # Line is right
    elif error < -20:
        turn_left()     # Line is left
    else:
        go_forward()    # Line is centered
```

### PID Controller (Advanced)

```python
Kp = 0.5  # Proportional gain
Ki = 0.01 # Integral gain
Kd = 0.1  # Derivative gain

integral = 0
previous_error = 0

while True:
    error = get_error()  # Get error from line detection
    
    integral += error
    derivative = error - previous_error
    
    output = Kp * error + Ki * integral + Kd * derivative
    
    set_motor_speed(output)
    previous_error = error
```

---

## 🔧 Troubleshooting

### Line Not Detected
- Check lighting (should be even)
- Adjust THRESHOLD for your conditions
- Ensure line has good contrast

### Low FPS
- Reduce camera resolution
- Disable display (if not needed)
- Use binary thresholding (faster processing)

### Line "Jitters"
- Add averaging over multiple frames
- Use PID controller instead of simple logic
- Check camera mount (should be rigid)

---

## 📂 Working with Files (Additional)

### Reading a File

```python
with open("/sdcard/data.txt", "r") as f:
    print(f.read())
```

### Writing a File

```python
with open("/sdcard/data.txt", "w") as f:
    f.write("test data\n")
    f.write("line 2\n")
```

### Logging Data

```python
# Save line detection statistics
with open("/sdcard/line_log.txt", "a") as f:
    f.write(f"FPS: {clock.fps()}, Error: {error}\n")
```

---

## 📚 Additional Resources

- [K230 Documentation](https://github.com/AIDevelopersMonster/K230)
- [OpenMV Documentation](https://docs.openmv.io/) (similar API)
- [PID Controllers for Beginners](https://en.wikipedia.org/wiki/PID_controller)

---

## 📝 License

Examples provided for educational purposes. Feel free to use in your projects.

**Author:** AIDevelopersMonster  
**Board:** Yahboom K230  
**GitHub:** https://github.com/AIDevelopersMonster/K230

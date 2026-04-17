# Multithreading on K230

## What is Multithreading

Multithreading is the ability to execute multiple tasks "simultaneously" within a single program.

On the **Yahboom K230** board, the built-in `_thread` module is used for working with threads.

## Key Concepts

- **Thread** — a separate path of code execution within a program
- **Main thread** — the primary thread where the program starts
- **Child threads** — additional threads created by the main thread
- **Scheduler** — the part of the system that decides which thread runs at any given moment

## How It Works

1. Each thread executes its own function independently
2. Threads run concurrently (logically, not necessarily physically)
3. Output messages in the terminal may be interleaved
4. For proper operation, you need to give the scheduler a chance to switch between threads

## Important Rules

### 1. Use Delays (sleep)

```python
time.sleep(0.5)      # 0.5 seconds delay
time.sleep_ms(500)   # 500 milliseconds delay
```

Without delays, a thread can consume 100% of the CPU and other threads won't be able to run.

### 2. Synchronize Access to Shared Data

If multiple threads work with the same variable, use a **lock**:

```python
lock = _thread.allocate_lock()  # create a lock
lock.acquire()                   # acquire the lock
# ... work with shared data ...
lock.release()                   # release the lock
```

## Main Functions of _thread Module

| Function | Description |
|----------|-------------|
| `_thread.start_new_thread(func, args)` | Starts a new thread with function `func` and arguments `args` |
| `_thread.get_ident()` | Returns the unique identifier of the current thread |
| `_thread.allocate_lock()` | Creates a lock object for synchronization |

## Examples in This Folder

| File | Description | What You Learn |
|------|-------------|----------------|
| `01_thread_basic.py` | Two threads printing messages alternately | Basic thread launching |
| `02_thread_ident.py` | Displaying thread IDs and counters | Unique thread IDs |
| `03_thread_lock_demo.py` | Synchronization via lock with shared counter | Protecting shared data |

## What the Examples Demonstrate

1. **Threads run concurrently** — you see output from both threads
2. **Output is interleaved** — messages from different threads are mixed
3. **Synchronization is needed** — without lock, data can be corrupted

## Common Beginner Mistakes

❌ **Forgot sleep()** — thread consumes 100% CPU  
❌ **No lock when accessing shared data** — race conditions possible  
❌ **Main thread exited** — program crashed, child threads stopped  

## Summary

**Multithreading** = ability to solve multiple tasks simultaneously

**But remember:**
- You need delays (`sleep`) for thread switching
- You need synchronization (`lock`) for shared data
- The main thread must keep running while child threads are needed

## Additional Resources

- MicroPython Documentation: https://docs.micropython.org/
- Source Code on GitHub: https://github.com/AIDevelopersMonster/K230

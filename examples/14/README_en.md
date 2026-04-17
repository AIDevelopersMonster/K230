# Multithreading on K230

## What is multithreading

Multithreading allows running multiple tasks "at the same time".

On K230, the `_thread` module is used.

## Key ideas

- Each thread runs its own function
- Threads execute concurrently
- Output is interleaved

## Important

- You must use `sleep()` or `sleep_ms()`
- Otherwise one thread may block CPU

## Main functions

- `_thread.start_new_thread(func, args)` — start thread
- `_thread.get_ident()` — get thread ID
- `_thread.allocate_lock()` — create lock

## Examples

| File | Description |
|------|------------|
| 01_thread_basic.py | two threads printing |
| 02_thread_ident.py | thread IDs demo |
| 03_thread_lock_demo.py | lock synchronization |

## What you learn

1. Threads run concurrently
2. Output is mixed
3. Synchronization is required

## Summary

Multithreading = multiple tasks at once

But requires control (sleep, lock)

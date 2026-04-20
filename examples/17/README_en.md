# Touch Display on K230

## What is it

Touch display allows interaction using finger input.

Use cases:
- UI controls
- interactive apps
- device control

## Concept

finger → coordinates → logic → action

## Steps

1. Init touch
2. Read touch
3. Process
4. Display

## Functions

- Touch.init()
- Touch.read()

## Examples

| File | Description |
|------|------------|
| 01 | basic touch |
| 02 | drawing |
| 03 | button |

## Notes

- Touch.read() returns (x,y)
- must run in loop
- update display continuously

## Summary

Touch enables interactive UI like smartphone

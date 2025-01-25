import keyboard

print("Press 'Esc' to stop.")

# This function will be called every time a key is pressed
def on_key_event(event):
    print(f"Key '{event.name}' pressed")

# Start listening to key events
keyboard.on_press(on_key_event)

# Block the program and keep it running
keyboard.wait('esc')

print("Program terminated.")

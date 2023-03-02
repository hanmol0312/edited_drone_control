from pynput.keyboard import Key, Listener

def on(key: Key):
    
    if str(key)=='w':
        print("w is pressed")

print(type(Key))
listener = Listener(on_press=on)
listener.start()
listener.join()
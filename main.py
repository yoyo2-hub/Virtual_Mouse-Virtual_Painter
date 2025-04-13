import subprocess
import keyboard
import time

def run_file(filename):
    return subprocess.Popen(["python", filename])

if __name__ == "__main__":
    print("Starting Virtual Mouse by default...")
    process = run_file("AiVirtualMouseProject.py")  # Start mouse mode by default

    while True:
        if keyboard.is_pressed('s'):
            print("Switching to Painter...")
            process.terminate()  # Stop current process
            time.sleep(1)
            process = run_file("painter.py")  # Run painter
            while not keyboard.is_pressed('e') and not keyboard.is_pressed('q'):
                time.sleep(0.1)

        elif keyboard.is_pressed('e'):
            print("Switching to Virtual Mouse...")
            process.terminate()
            time.sleep(1)
            process = run_file("AiVirtualMouseProject.py")  # Run mouse
            while not keyboard.is_pressed('s') and not keyboard.is_pressed('q'):
                time.sleep(0.1)

        elif keyboard.is_pressed('q'):
            print("Exiting...")
            process.terminate()
            break

        time.sleep(0.1)

import RPi.GPIO as GPIO
import time

RESTART_BUTTON_PIN = 5   # GPIO5 for the restart button (blue)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(RESTART_BUTTON_PIN, GPIO.OUT)

GPIO.output(RESTART_BUTTON_PIN, GPIO.HIGH)  # Relay off = HIGH for normally open

def restart_node():
    try:
        GPIO.output(RESTART_BUTTON_PIN, GPIO.LOW)  # Press restart button (activate relay)
        print("Restart button pressed.")
        
        time.sleep(1)  # Hold for 1 second
        
        GPIO.output(RESTART_BUTTON_PIN, GPIO.HIGH)  # Release restart button
        print("Restart button released.")

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    restart_node()

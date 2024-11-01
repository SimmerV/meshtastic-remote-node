## This script requires the splicing of wires from the Station G2 button traces to a relay

import RPi.GPIO as GPIO
import time

# Define GPIO pins for the relay channels
FIRMWARE_BUTTON_PIN = 6  # GPIO06 for the firmware button (green)
RESTART_BUTTON_PIN = 5   # GPIO05 for the restart button (blue)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(FIRMWARE_BUTTON_PIN, GPIO.OUT)
GPIO.setup(RESTART_BUTTON_PIN, GPIO.OUT)

GPIO.output(FIRMWARE_BUTTON_PIN, GPIO.HIGH)  # Relay off = HIGH for normally open
GPIO.output(RESTART_BUTTON_PIN, GPIO.HIGH)   # Relay off = HIGH for normally open

def flash_firmware():
    try:
        GPIO.output(FIRMWARE_BUTTON_PIN, GPIO.LOW)  # Press firmware button (activate relay)
        print("Firmware button pressed and held.")
        
        time.sleep(0.5)  # Wait a moment before pressing restart
        GPIO.output(RESTART_BUTTON_PIN, GPIO.LOW)  # Press restart button
        print("Restart button pressed.")

        time.sleep(1)  # Hold restart button for 1 second
        GPIO.output(RESTART_BUTTON_PIN, GPIO.HIGH)  # Release restart button
        print("Restart button released.")
        
        print("Holding firmware button for 5 seconds.")  # Hold firmware button 5 additional seconds
        time.sleep(5)
        
        GPIO.output(FIRMWARE_BUTTON_PIN, GPIO.HIGH)  # Release firmware button
        print("Firmware button released. Radio should be in firmware flashing mode.")

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    flash_firmware()

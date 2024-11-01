## This script uses PWM to control two Noctua 60mm fans via Raspberry Pi4 GPIO pins based on sensor data from a DHT22
## Requires adafruit_dht and RPi.GPIO libs installed, recommend using venv
## NOTE - at this time, I was unable to use the actual PWM RPM sensor to obtain real time RPM data. Instead, I printed <expected> RPM data calculated off duty cycle

import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# Define GPIO pins
PWM_PIN = 18  # PWM pin for fan control
RPM_PIN = 17  # RPM sensor pin

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(RPM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM
fan_pwm = GPIO.PWM(PWM_PIN, 25000)  # 25 kHz PWM frequency
fan_pwm.start(0)  # Start with fan off (0% duty cycle)

# Initialize DHT22 sensor
dht_device = adafruit_dht.DHT22(board.D4)

def calculate_rpm_from_duty_cycle(duty_cycle):
    return (duty_cycle / 100) * 3000  # Convert duty cycle to RPM

def set_fan_speed(speed_percentage):
    duty_cycle = max(0, min(100, speed_percentage))  # Set min/max of fan
    fan_pwm.ChangeDutyCycle(duty_cycle)
    return duty_cycle

try:
    while True:
        try:
            # Try to read temperature and humidity
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                print(f"Humidity: {humidity:.1f}% | Temperature: {temperature_c:.1f}°C / {temperature_c * 9 / 5 + 32:.1f}°F")

                # Fan curve: 
                if temperature_c >= 30:  # 30°C and above: full speed (100%)
                    duty_cycle = set_fan_speed(100)
                elif temperature_c >= 28:  # Between 28°C and 30°C: 90% speed
                    duty_cycle = set_fan_speed(90)
                elif temperature_c >= 26:  # Between 26°C and 28°C: 80% speed
                    duty_cycle = set_fan_speed(80)
                elif temperature_c >= 24:  # Between 24°C and 26°C: 70% speed
                    duty_cycle = set_fan_speed(70)
                elif temperature_c >= 22:  # Between 22°C and 24°C: 60% speed
                    duty_cycle = set_fan_speed(60)
                elif temperature_c >= 20:  # Between 20°C and 22°C: 50% speed
                    duty_cycle = set_fan_speed(50)
                elif temperature_c >= 18:  # Between 18°C and 20°C: 40% speed
                    duty_cycle = set_fan_speed(40)
                elif temperature_c >= 16:  # Between 16°C and 18°C: 30% speed
                    duty_cycle = set_fan_speed(30)
                elif temperature_c >= 14:  # Between 14°C and 16°C: 20% speed
                    duty_cycle = set_fan_speed(20)
                else:  # Below 14°C: turn off the fan
                    duty_cycle = set_fan_speed(0)

                rpm = calculate_rpm_from_duty_cycle(duty_cycle)  # Calculate and print RPM based on duty cycle
                print(f"Fan RPM: {rpm:.0f}")

            else:
                print("Failed to retrieve data from sensor")

        except RuntimeError as e:  # Handle checksum or other sensor reading errors
            print(f"Sensor error: {e}")
            time.sleep(2.0)  # Wait before retrying

        time.sleep(2.0)  # Wait a bit before the next reading

except KeyboardInterrupt: # Clean up GPIO and stop PWM on exit
    print("Cleanup done.")
    fan_pwm.stop()
    GPIO.cleanup()

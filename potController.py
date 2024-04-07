import serial
import time

class PotController:
    def __init__(self, port, baud_rate=9600, num_samples=10):
        self.ser = serial.Serial(port, baud_rate)
        self.num_samples = num_samples
        self.readings_buffer = []  # Buffer to store recent readings
        self.buffer_size = 10  # Size of the buffer
        self.max_reasonable_value = 1023  # Maximum reasonable value for readings

        # State flags and variables
        self.last_average = None
        self.initial_baseline_set = False
        self.significant_movement_occurred = False
        self.stabilization_start_time = None

    def reset(self):
        # Resets the controller's state and buffer
        self.readings_buffer.clear()
        self.initial_baseline_set = False
        self.significant_movement_occurred = False
        self.stabilization_start_time = None
        self.last_average = None

    def read_average_potentiometer(self):
        # Reads and averages potentiometer values, filters anomalies
        total = 0
        valid_samples = 0
        for _ in range(self.num_samples):
            try:
                ser_bytes = self.ser.readline()
                decoded = ser_bytes.strip().decode('utf-8')
                if decoded.isdigit():
                    value = int(decoded)
                    if value <= self.max_reasonable_value:  # Filter anomaly
                        total += value
                        valid_samples += 1
                        # Update readings buffer
                        self.readings_buffer.append(value)
                        if len(self.readings_buffer) > self.buffer_size:
                            self.readings_buffer.pop(0)
            except (ValueError, UnicodeDecodeError) as e:
                print(f"Invalid data received: {e}")
        return total // valid_samples if valid_samples > 0 else None

    def update(self):
        # Main update function to determine if the potentiometer has stabilized
        current_average = self.read_average_potentiometer()
        if current_average is None: return False

        print(current_average)  # Debugging: print current average reading

        if not self.initial_baseline_set:
            self.last_average = current_average
            self.initial_baseline_set = True
            return False

        if self.is_significant_change(current_average):
            self.significant_movement_occurred = True
            self.stabilization_start_time = time.time()

        elif self.significant_movement_occurred:
            if time.time() - self.stabilization_start_time >= 1.5:  # 1.5 seconds to re-rotate
                self.significant_movement_occurred = False
                return True

        self.last_average = current_average
        return False

    def is_significant_change(self, current_average):
        # Determines if there's a significant change in the readings
        if self.last_average is None:
            return False
        return abs(current_average - self.last_average) > 20  # Threshold for significant change

    def get_game_level(self):
        # Determines game level based on the current potentiometer average
        current_average = self.read_average_potentiometer()
        if current_average is not None:
            if current_average >= 682: return 3
            elif current_average >= 341: return 2
            else: return 1
        return None

    def close(self):
        # Closes the serial connection
        self.ser.close()
import smbus2
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
import pyttsx3  # For audio notifications

# Initialize Text-to-Speech Engine for audio feedback
engine = pyttsx3.init()

# I2C Bus Initialization
I2C_BUS = 1  # Use the appropriate I2C bus (e.g., 1 for Raspberry Pi)
bus = smbus2.SMBus(I2C_BUS)

# Sensor I2C Addresses
MPU6050_ADDR = 0x68
BME280_ADDR = 0x76
VLX351X_ADDR = 0x29

# MPU6050 Initialization
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0x00)  # Wake up MPU6050

# Read MPU6050 sensor data (IMU)
def read_imu_sensor():
    accel_data = [bus.read_byte_data(MPU6050_ADDR, reg) for reg in range(0x3B, 0x41)]
    gyro_data = [bus.read_byte_data(MPU6050_ADDR, reg) for reg in range(0x43, 0x49)]

    # Convert data to readable format
    accel = [int.from_bytes(accel_data[i:i + 2], 'big', signed=True) / 16384.0 for i in range(0, 6, 2)]
    gyro = [int.from_bytes(gyro_data[i:i + 2], 'big', signed=True) / 131.0 for i in range(0, 6, 2)]
    return accel + gyro

# Read BME280 sensor data (Temperature, Humidity)
def read_ambient_sensor():
    bme280_data = [bus.read_byte_data(BME280_ADDR, reg) for reg in range(0xF7, 0xFF)]
    temp_raw = (bme280_data[0] << 12) | (bme280_data[1] << 4) | (bme280_data[2] >> 4)
    humidity_raw = (bme280_data[6] << 8) | bme280_data[7]

    # Convert data (calibration needed)
    temperature = temp_raw / 100.0
    humidity = humidity_raw / 1024.0
    return [temperature, humidity]

# Read VLX351X sensor data (Distance)
def read_lidar_sensor():
    bus.write_byte_data(VLX351X_ADDR, 0x00, 0x01)  # Start ranging
    time.sleep(0.1)
    distance_data = [bus.read_byte_data(VLX351X_ADDR, reg) for reg in range(0x14, 0x16)]
    distance = (distance_data[0] << 8) | distance_data[1]
    return distance / 100.0  # Convert to meters

# Simulated function to read heart rate and HRV (use MAX30100 if available)
def read_heart_rate_sensor():
    heart_rate = np.random.randint(60, 100)  # Replace with actual sensor reading
    spo2 = np.random.randint(95, 99)  # Replace with actual sensor reading
    return heart_rate, spo2

# HRV calculation (simulated)
def read_hrv_sensor():
    rr_intervals = [0.8, 0.81, 0.79, 0.80, 0.82]  # Replace with actual RR intervals
    hrv = np.sqrt(np.mean(np.diff(rr_intervals) ** 2))  # RMSSD
    return hrv

# Gait analysis using MPU6050
def read_gait_sensor():
    imu_data = read_imu_sensor()
    step_time = np.random.uniform(0.7, 1.0)  # Simulated step time
    gait_cycle = np.random.uniform(1.0, 1.5)  # Simulated gait cycle
    gait_speed = np.random.uniform(1.0, 1.5)  # Simulated gait speed
    swing_time = step_time / 2  # Simplified calculation
    return [step_time, gait_cycle, gait_speed, swing_time]

# Data collection from sensors
def collect_sensor_data():
    imu_data = read_imu_sensor()
    ambient_data = read_ambient_sensor()
    lidar_distance = read_lidar_sensor()
    heart_rate, spo2 = read_heart_rate_sensor()
    hrv = read_hrv_sensor()
    gait_data = read_gait_sensor()
    return np.concatenate([imu_data, ambient_data, [lidar_distance, heart_rate, spo2, hrv], gait_data])

# Random Forest model for fall risk prediction
data = [collect_sensor_data() for _ in range(100)]  # Simulated data
labels = [np.random.randint(0, 3) for _ in range(100)]  # Simulated labels (0: Low, 1: Moderate, 2: High)
model = RandomForestClassifier(n_estimators=100)
model.fit(data, labels)

# Proactive audio alerts
def audio_alert(fall_risk):
    messages = ["Your fall risk is low. Stay safe!", "Moderate fall risk detected. Be cautious!", 
                "High fall risk detected! Take immediate action!"]
    engine.say(messages[fall_risk])
    engine.runAndWait()

# Main loop for data collection and prediction
while True:
    features = collect_sensor_data()
    fall_risk = model.predict([features])[0]
    audio_alert(fall_risk)
    print(f"Fall Risk: {fall_risk}")
    time.sleep(5)

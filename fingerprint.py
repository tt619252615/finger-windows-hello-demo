import serial
import adafruit_fingerprint

# 配置串口
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
    if finger.get_image() != adafruit_fingerprint.OK:
        return False
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def enroll_finger(location):
    # Get first image
    if finger.get_image() != adafruit_fingerprint.OK:
        return False
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    # Wait for finger to be removed
    while finger.get_image() != adafruit_fingerprint.NOFINGER:
        pass
    # Get second image
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        return False
    if finger.create_model() != adafruit_fingerprint.OK:
        return False
    if finger.store_model(location) != adafruit_fingerprint.OK:
        return False
    return True

def delete_finger(location):
    if finger.delete_model(location) != adafruit_fingerprint.OK:
        return False
    return True

def get_fingerprint_templates():
    templates = []
    for page in range(0, 4):
        template = finger.read_templates(page)
        if template[0] == adafruit_fingerprint.OK:
            templates.extend(template[1])
    return templates

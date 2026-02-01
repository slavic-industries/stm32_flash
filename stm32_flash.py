#!/usr/bin/env python3

import glob
import sys
import time
import subprocess
import os
from gpiozero import DigitalOutputDevice

# ================= CONFIG =================

BOOT0_GPIO = 17
NRST_GPIO  = 27

FLASH_ADDRESS = "0x08000000"

# ==========================================

boot0 = DigitalOutputDevice(BOOT0_GPIO, active_high=True, initial_value=False)
nrst  = DigitalOutputDevice(NRST_GPIO,  active_high=False, initial_value=True)

def enter_bootloader():
    print("Entering STM32 bootloader...")
    boot0.on()          # Activate BOOT1
    nrst.on()           # Activate Reset
    time.sleep(0.2)
    nrst.off()          # Release Reset
    time.sleep(0.2)

def exit_bootloader():
    print("Exiting bootloader, running firmware...")
    boot0.off()         # Release BOOT1
    nrst.on()		    # Activate Reset
    time.sleep(0.05)
    nrst.off()		    # Release Reset

def compile_firmware(firmware_location):
    print("Compiling firmware...")
    cmd = [
        "arduino-cli",
        "compile",
        "-v",
        "-b", "STMicroelectronics:stm32:GenF4:pnum=BLACKPILL_F411CE ",
        "--output-dir", f"{firmware_location}/build",
        firmware_location
    ]
    subprocess.check_call(cmd)

def flash_firmware(serial_port, firmware_location):
    firmware = glob.glob(f"{firmware_location}/build/*.bin")[0]
    print("Flashing firmware...")
    print(f"File: {firmware}")
    cmd = [
        "stm32flash",
        "-w", firmware,
        "-v",
        "-g", FLASH_ADDRESS,
        serial_port
    ]
    subprocess.check_call(cmd)

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <serial_port>  <arduino_sketch_location>")
        sys.exit(1)

    serial_port = sys.argv[1]
    firmware_location = sys.argv[2]

    if not os.path.exists(firmware_location):
        print(f"Error: firmware location does not exist")
        sys.exit(1)

    if not os.path.exists(serial_port):
        print(f"Serial port not found: {serial_port}")
        sys.exit(1)

    try:
        enter_bootloader()
        compile_firmware(firmware_location)
        flash_firmware(serial_port, firmware_location)
        exit_bootloader()
        print("Flashing successful")
    except subprocess.CalledProcessError:
        print("Flashing failed")
        exit(1)

if __name__ == "__main__":
    main()


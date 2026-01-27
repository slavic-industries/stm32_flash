#!/usr/bin/env python3

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
    nrst.off()           # Release Reset
    time.sleep(0.2)

def exit_bootloader():
    print("Exiting bootloader, running firmware...")
    boot0.off()         # Release BOOT1
    nrst.on()		# Activate Reset
    time.sleep(0.05)
    nrst.off()		# Release Reset

def flash_firmware(serial_port, firmware):
    print("Flashing firmware...")
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
        print(f"Usage: {sys.argv[0]} <serial_port>  <firmware_file.bin>")
        sys.exit(1)

    serial_port = sys.argv[1]
    firmware = sys.argv[2]

    if not os.path.isfile(firmware):
        print(f"Error: file not found: {firmware}")
        sys.exit(1)

    if not os.path.exists(serial_port):
        print(f"Serial port not found: {serial_port}")
        sys.exit(1)

    try:
        enter_bootloader()
        flash_firmware(serial_port, firmware)
        exit_bootloader()
        print("Flashing successful")
    except subprocess.CalledProcessError:
        print("Flashing failed")
        exit(1)

if __name__ == "__main__":
    main()


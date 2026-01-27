# stm32_flash
Flashing an STM32 microcontroller using a Raspberry PI over UART

---

THis repository contains a simple script that allows an STM32 microcontroller to be flashed with new frimware through a Raspberry PI using UART.

## Requirements

- An STM32 controler that can be flashed through UART (check STM32 application note AN2606)
  - Tested on STM32F401RE (Nucleo board)
- A Raspberry PI
  - Tested on RPI CM4
- Free pins on the RPI 40 pin connector
  - GPIO 14 (TXD0)
  - GPIO 15 (RXD0)
  - GPIO 17 (GPIO_GEN0)
  - GPIO 27 (GPIO_GEN2)
- Female-Female jumper wires


## How To

### Connecting the hardware

Connect the signal pins as in the table below

| RPI GPIO | Signal | STM32     |
| -------  | ------ | --------- |
| GPIO 14  | TXD    | USARTx_RX |
| GPIO 15  | RXD    | USARTx_TX |
| GPIO 17  | I/O    | BOOT0     |
| GPIO 27  | I/O    | NRST      |

Additionally connect GND from the RPI to the STM and supply power to the STM.

### Runnign the script

1. Download repo and unzip the files in a known directory. For example `~/temp`.
2. Open a new terminal and go to that directory.
3. Type `sudo chmod +x stm32_flash.py` to make the script an executable file.
4. Run the script with `./stm32_flash.py <serial_port> <firmware_file.bin>`



## Tips

- The serial port on the RPI  needs to be activated.
  - Activate the serial port on Raspberry PI OS by writing `sudo raspi-config` in the terminal
- Some STM32 microcontrollers have two boot pins (BOOT0 and BOOT1). In this case another pin on the RPI 40 pin connector will need to be used and the scrip modified.



 

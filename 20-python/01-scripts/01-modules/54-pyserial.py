import time

import serial


# device = '/dev/ttyS1'
device = 'COM5'
action_code = {
    'on': b'\xa0\x01\x01\xa2',
    'off': b'\xa0\x01\x00\xa1'
}


def scan():
    import serial.tools.list_ports
    port_list = list(serial.tools.list_ports.comports())
    return port_list


def send(content: bytes):
    with serial.Serial(device, 9600, timeout=5) as ser:
        reponse = ser.write(content)
        print(reponse)


if __name__ == '__main__':
    send(action_code['on'])
    time.sleep(5)
    send(action_code['off'])

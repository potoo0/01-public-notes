#!/bin/env python
import os
os.environ["BLEAK_LOGGING"] = "1"  # export BLEAK_LOGGING=1

import asyncio
import traceback
from typing import List

from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

from loguru import logger


loop = asyncio.get_event_loop()


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    logger.info(f"--- notification_handler {sender}: {data}")


async def notify_char(address: str, notify_uuid: str, write_list: List):
    print(f'{address=}, {notify_uuid=}, {write_list=}')
    async with BleakClient(address) as client:
        try:
            logger.info(f"Device Connected: {client.is_connected}")

            # await client.start_notify(char_uuid, notification_handler)
            # print("started notify")

            for data in write_list:
                encode_data = bytes.fromhex(data['data'])
                resp = await client.write_gatt_char(data['uuid'], encode_data)
                logger.info(f"request: {data}, response: {resp}")
                await asyncio.sleep(0.5)

            # await asyncio.sleep(5.0)
            # await client.stop_notify(char_uuid)
        except Exception as e:
            logger.error(f'error: {e}')
            traceback.print_exc()
            return False
    return True


if __name__ == "__main__":
    ble_address = 'BA:33:DC:F6:46:6D'
    notify_uuid = '10e2fde2-d7fe-4845-b3f3-a32010ebb095'
    write_list = [{
        'uuid': 'b02eaeaa-f6bc-4a7e-bc94-f7b7fc8ded0b',
        'data': 'fe010006320101807f12'
    }]

    task_write_char = loop.run_until_complete(notify_char(ble_address, notify_uuid, write_list))
    print(f'res: {task_write_char}')

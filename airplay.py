#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import logging
import os
import sys
import signal
import asyncio
import tello

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"),
                    format="%(asctime)s;%(levelname)s;%(message)s")
logger = logging.getLogger(sys.argv[0])


async def log_telemetry(t):
    while True:
        logger.info("BAT: {} SPD: {} T: {}".format(
            t.get_battery(), t.get_speed(), t.get_flight_time()))
        await asyncio.sleep(1)


async def fly_around(t):
    t.takeoff()
    await asyncio.sleep(10)
    t.land()


def sigint_handler(t):
    logger.info('You pressed Ctrl+C, calling failsafe()')
    t.land()
    sys.exit()
    logger.warning('Shutting down.')


if __name__ == "__main__":
    t = tello.Tello("192.168.10.2", 8889, imperial=False)

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, sigint_handler, t)
    loop.run_until_complete(asyncio.gather(
        log_telemetry(t),
        fly_around(t)
    ))


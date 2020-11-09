#!/usr/bin/python3
#
# Remote Controlled Home Light
#
# MIT License
# Copyright (c) 2019 SrdjanStankovic

import os
import sys
import time
import logging
from typing import Optional
from typing import Tuple
from typing import Union

module_path = os.sep + ".." + os.sep + ".." + os.sep
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + module_path)
import wolk  # noqa

logging.basicConfig(level=logging.DEBUG)

from sonoff_control import SWITCH1_REF
from sonoff_control import SWITCH2_REF
from sonoff_control import SWITCH1_ADD
from sonoff_control import SWITCH2_ADD
from sonoff_control import sonoff_switch


def main():
    """
    Demonstrate all functionality of wolk module.

    Create actuation handler and actuator status provider
    for switch and slider actuators.

    Pass all of these to a WolkConnect class
    and start a loop to send different types of random readings.
    """
    # Insert the device credentials received
    # from WolkAbout IoT Platform when creating the device
    # List actuator references included on your device
    actuator_references = [SWITCH1_REF, SWITCH2_REF]
    device = wolk.Device(
        key="852c335e-e278-416f-a3ac-6350edbeda39",
        password="JJJZMYTP7N",
        actuator_references=actuator_references,
    )

    class Actuator:
        def __init__(
            self, inital_value: Optional[Union[bool, int, float, str]]
        ):
            self.value = inital_value

    switch1 = Actuator(False)
    switch2 = Actuator(False)

    # Provide a way to read actuator status if your device has actuators
    def actuator_status_provider(
        reference: str,
    ) -> Tuple[wolk.State, Optional[Union[bool, int, float, str]]]:
        if reference == actuator_references[0]:
            return wolk.State.READY, switch1.value
        elif reference == actuator_references[1]:
            return wolk.State.READY, switch2.value

        return wolk.State.ERROR, None

    # Provide an actuation handler if your device has actuators
    def actuation_handler(
        reference: str, value: Union[bool, int, float, str]
    ) -> None:
        logging.info(f"Setting actuator '{reference}' to value: {value}")
        if reference == actuator_references[0]:
            if sonoff_switch(SWITCH1_ADD, value):
                switch1.value = value
            else:
                # Set switch in inactive state
                switch1.value = 0

        elif reference == actuator_references[1]:
            if sonoff_switch(SWITCH2_ADD, value):
                switch2.value = value
            else:
                # Set switch in inactive state
                switch2.value = 0

    # Pass device and optionally connection details
    # Provided connection details are the default value
    # Provide actuation handler and actuator status provider via with_actuators
    wolk_device = (
        wolk.WolkConnect(
            device=device,
            host="api-demo.wolkabout.com",
            port=8883,
            ca_cert="utility/ca.crt",
        )
        .with_actuators(
            actuation_handler=actuation_handler,
            actuator_status_provider=actuator_status_provider,
        )        
    )

    # Establish a connection to the WolkAbout IoT Platform
    logging.info("Connecting to WolkAbout IoT Platform")
    try:
        wolk_device.connect()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)

    # Successfully connecting to the platform will publish actuator status
    wolk_device.publish_actuator_status(SWITCH1_REF)
    wolk_device.publish_actuator_status(SWITCH2_REF)

if __name__ == "__main__":
    main()


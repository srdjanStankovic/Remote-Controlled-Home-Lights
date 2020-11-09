"""Example that covers all the functionality of WolkConnect-Python."""
#   Copyright 2020 WolkAbout Technology s.r.o.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import json
import os
import random
import sys
import time
import logging
import requests
import xml.etree.ElementTree as ET
from traceback import print_exc
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

module_path = os.sep + ".." + os.sep + ".." + os.sep
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + module_path)
import wolk  # noqa

logging.basicConfig(level=logging.DEBUG)

firmware_version = "1.0"

# Read switches from file
tree = ET.parse("Sonoff-Switch-Control/config.xml")
root = tree.getroot()
number_of_children = len(root.getchildren())
# Switch1
SWITCH1_REF = "SW1"
SWITCH1_ADD = root[0][1].text
# Switch2
SWITCH2_REF = "SW2"
SWITCH2_ADD = root[1][1].text


def sonoff_switch(ip_add, value):
    base_url = "http://" + ip_add + "/control?cmd=event,Turn"
    if value == 1 or value == "true":
        base_url = base_url + "On"
    else:
        base_url = base_url + "Off"

    logging.debug(base_url)
    payload = {}
    try:
        response = requests.post(base_url, data=payload)
    except:
        logging.error("Couldn't change switch state.")
        return False

    logging.info(response.text)  # TEXT/HTML
    logging.info(str(response.status_code) + str(response.reason))  # HTTP

    return True


def main():
    """
    Demonstrate all functionality of wolk module.

    Create actuation handler and actuator status provider
    for switch and slider actuators.

    Create configuration handler and configuration provider
    for 4 types of configuration options.

    Create a firmware installer and handler
    for enabling firmware update.

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

    # Extend this class to handle the installing of the firmware file
    class MyFirmwareHandler(wolk.FirmwareHandler):
        def install_firmware(self, firmware_file_path: str) -> None:
            """Handle the installing of the firmware file here."""
            logging.info(f"Installing firmware from path: {firmware_file_path}")
            time.sleep(5)
            sys.exit()

        def get_current_version(self) -> str:
            """Return current firmware version."""
            return firmware_version

    # Pass device and optionally connection details
    # Provided connection details are the default value
    # Provide actuation handler and actuator status provider via with_actuators
    # Provide configuration provider/handler via with_configuration
    # Enable file management and firmware update via their respective methods
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
        .with_file_management(
            preferred_package_size=1000 * 1000,
            max_file_size=100 * 1000 * 1000,
            file_directory="files",
        )
        .with_firmware_update(firmware_handler=MyFirmwareHandler())
        # Possibility to provide custom implementations for some features
        # .with_custom_protocol(message_factory, message_deserializer)
        # .with_custom_connectivity(connectivity_service)
        # .with_custom_message_queue(message_queue)
    )

    # Establish a connection to the WolkAbout IoT Platform
    logging.info("Connecting to WolkAbout IoT Platform")
    logging.info("Connecting to WolkAbout IoT Platform")
    try:
        wolk_device.connect()
    except RuntimeError as e:
        logging.error(str(e))
        sys.exit(1)

    # Successfully connecting to the platform will publish device configuration
    # all actuator statuses, files present on device, current firmware version
    # and the result of a firmware update if it occurred
    wolk_device.publish_actuator_status(SWITCH1_REF)
    wolk_device.publish_actuator_status(SWITCH2_REF)

if __name__ == "__main__":
    main()


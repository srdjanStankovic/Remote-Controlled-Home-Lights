#!/usr/bin/python

import math
import os
import random
import sys
import time

import requests
import logging

import xml.etree.ElementTree as ET

from persistent_queue import PersistentQueue
import wolk  # noqa


logging.basicConfig(level=logging.DEBUG)
#Read switches from file
tree = ET.parse('Sonoff-Switch-Control/config.xml')
root = tree.getroot()
number_of_children = len(root.getchildren())
#Switch1
SWITCH1_REF = "SW1"
SWITCH1_ADD = root[0][1].text
#Switch2
SWITCH2_REF = "SW2"
SWITCH2_ADD = root[1][1].text


def sonoff_switch(ip_add, value):
	base_url="http://"+ ip_add + "/control?cmd=event,Turn"
	if value==1 or value=='true':
		base_url=base_url+"On"
	else:
		base_url=base_url+"Off"

	payload = {}
	try:
		response = requests.post(base_url, data=payload)
	except:
                print("Couldn't change switch state")
                return False

	print(response.text) #TEXT/HTML
	print(response.status_code, response.reason) #HTTP

	return True


def main():
    device = wolk.Device(
        key="some-key", #change this
        password="some-password", #change this
        actuator_references=[SWITCH1_REF, SWITCH2_REF],
    )

    class ActuatorSimulator:
        def __init__(self, inital_value):
            self.value = inital_value

    switch1 = ActuatorSimulator(False)
    switch2 = ActuatorSimulator(False)

    # Provide a way to read actuator status if your device has actuators
    class ActuatorStatusProviderImpl(wolk.ActuatorStatusProvider):
        def get_actuator_status(self, reference):
            if reference == SWITCH1_REF:
                return wolk.ActuatorState.READY, switch1.value
            elif reference == SWITCH2_REF:
                return wolk.ActuatorState.READY, switch2.value

    # Provide an actuation handler if your device has actuators
    class ActuationHandlerImpl(wolk.ActuationHandler):
        def handle_actuation(self, reference, value):
            print("Setting actuator " + reference + " to value: " + str(value))
            if reference == SWITCH1_REF:
                if sonoff_switch(SWITCH1_ADD, value):
                    switch1.value = value
                else:
                    logging.error("Actuation Fialed. Set switch in inactive state")
                    switch1.value = 0

            elif reference == SWITCH2_REF:
                if sonoff_switch(SWITCH2_ADD, value):
                    switch2.value = value
                else:
                    logging.error("Actuation Failed. Set switch in inactive state")
                    switch2.value = 0

    # Custom queue example
    class FilesystemOutboundMessageQueue(wolk.OutboundMessageQueue):
        def __init__(self, path="."):
            if path == ".":
                self.queue = PersistentQueue("FileOutboundMessageQueue")
            else:
                self.queue = PersistentQueue("FileOutboundMessageQueue", path)

        def put(self, message):
            self.queue.push(message)

        def get(self):
            message = self.queue.pop()
            self.queue.flush()
            return message

        def peek(self):
            if not self.queue.peek():
                self.queue.clear()
                return None
            else:
                return self.queue.peek()

    filesystemOutboundMessageQueue = FilesystemOutboundMessageQueue()

    try:
        wolk_device = wolk.WolkConnect(
            device=device,
            actuation_handler=ActuationHandlerImpl(),
            actuator_status_provider=ActuatorStatusProviderImpl(),
            outbound_message_queue=filesystemOutboundMessageQueue,
            host="api-demo.wolkabout.com",
            port=8883,
            ca_cert="utility/ca.crt"
        )
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)

    # Establish a connection to the WolkAbout IoT Platform
    print("Connecting to WolkAbout IoT Platform")
    try:
        wolk_device.connect()
    except RuntimeError as e:
        print(str(e))
        sys.exit(1)

    wolk_device.publish_actuator_status(SWITCH1_REF)
    wolk_device.publish_actuator_status(SWITCH2_REF)


if __name__ == "__main__":
    main()

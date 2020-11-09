#!/usr/bin/python3
import logging
import requests
import xml.etree.ElementTree as ET

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


# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 13:30:03 2018

@author: Kyounghun Yoo

Connect GRAPHIX IOC
"""

from epics import ca
from command_calculation import *
import time

DEVICE_NAME = "GRAPHIX3:"

SEND_READ_CMD = "readCMD"     # Sending Read Command in .db
SEND_WRITE_CMD = "writeCMD"   # Sending Write Command in .db
GET_VERSION_CMD = "getVersion"    # Get Version Command in .db
GET_SN_CMD = "getSN"              # Get Serial Number Command in .db
GET_PN_CMD = "getPN"              # Get Part Number Command in .db
GET_UNIT_CMD = "getUnit"            # Get Pressure Unit Command in .db
GET_PRES1_CMD = "getPres1"           # Get Pressure in Ch.1 Command in .db

chSendRead = ca.create_channel(DEVICE_NAME+SEND_READ_CMD+".VAL")
chSendWrite = ca.create_channel(DEVICE_NAME+SEND_WRITE_CMD+".VAL")
chGetVersion = ca.create_channel(DEVICE_NAME+GET_VERSION_CMD+".VAL")
chGetSN = ca.create_channel(DEVICE_NAME+GET_SN_CMD+".VAL")
chGetPN = ca.create_channel(DEVICE_NAME+GET_PN_CMD+".VAL")
chGetUnit = ca.create_channel(DEVICE_NAME+GET_UNIT_CMD+".VAL")
chGetPres1 = ca.create_channel(DEVICE_NAME+GET_PRES1_CMD+".VAL")

def get_version_CMD():
    """
    Get Hardware and Software Version
    """
    getVersionCMD = calculate_send_read_CMD(5, 1)
    ca.put(chGetVersion, getVersionCMD)
    time.sleep(0.1)
    versionArr = ca.get(chGetVersion)
    versionGotten = convert_receive_read_value(versionArr)
    return versionGotten

    
def get_sn_CMD():
    """
    Get Serial Number
    """
    getSNCMD = calculate_send_read_CMD(5, 2)
    ca.put(chGetSN, getSNCMD)
    time.sleep(0.1)
    snArr = ca.get(chGetSN)
    snGotten = convert_receive_read_value(snArr)
    return snGotten
    
 
def get_pn_CMD():
    """
    Get Part Number
    """
    getPNCMD = calculate_send_read_CMD(5, 3)
    ca.put(chGetPN, getPNCMD)
    time.sleep(0.1)
    pnArr = ca.get(chGetPN)
    pnGotten = convert_receive_read_value(pnArr)
    return pnGotten
    
    
def get_unit_CMD():
    """
    Get Pressure Unit
    """
    getUnitCMD = calculate_send_read_CMD(5, 4)
    ca.put(chGetUnit, getUnitCMD)
    time.sleep(0.1)
    unitArr = ca.get(chGetUnit)
    unitGotten = convert_receive_read_value(unitArr)
    return unitGotten
    
    
def get_pres1_CMD():
    """
    Get Pressure Data in CH.1
    """
    getPresCMD1 = calculate_send_read_CMD(1, 29)
    ca.put(chGetPres1, getPresCMD1)
    time.sleep(0.1)
    presArr1 = ca.get(chGetPres1)
    presGotten1 = convert_receive_read_value(presArr1)
    return presGotten1


def send_read_CMD(parameterGroup=None, parameterNumber=None):
    """
    Send Read CMD
    """
    sendReadCMD = calculate_send_read_CMD(parameterGroup, parameterNumber)
    ca.put(chSendRead, sendReadCMD)
    return None

def get_read_CMD():
    """
    Receive Value for Read CMD
    """
    getReadCMD = ca.get(chSendRead)
    valGotten = convert_receive_read_value(getReadCMD)
    return valGotten

def send_write_CMD(parameterGroup=None, parameterNumber=None, value=None):
    """
    Send Write CMD
    """
    sendWriteCMD = calculate_send_write_CMD(parameterGroup, parameterNumber, value)
    ca.put(chSendWrite, sendWriteCMD)
    return None

def get_write_CMD():
    """
    Receive Value for Write CMD
    """
    getWriteCMD = ca.get(chSendWrite)
    valGotten = convert_receive_write_value(getWriteCMD)
    return valGotten


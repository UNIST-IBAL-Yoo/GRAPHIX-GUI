# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 13:30:03 2018

@author: Kyounghun Yoo

Command Calculation for GRAPHIX Gauge Controller
"""

SEPARATE_CH = 59        # Sparating Character (Decimal)
SPACE_CH = 32           # Space Character (Decimal)
TERM_CH = 4             # End (Terminate) Character (Decimal)
ACK_CH = 6              # Parameter value is accepted (Decimal)
NACK_CH = 21            # Parameter value is not accepted (Decimal)
READ_CH = 15            # Read Detection Character (Decimal)
WRITE_CH = 14           # Write Detection Character (Decimal)

# Error Explanation
# ----------------------------------------------------------------------------

ERR_6 = "CRC sum error"
ERR_8 = "Format error"
ERR_9 = "Group not available"
ERR_10 = "Parameter not available for sensor type"
ERR_11 = "Parameter read-only"
ERR_12 = "Parameter value incorrect"
ERR_13 = "Number of parameter values wrong"
ERR_14 = "Value currently not changeable"
ERR_15 = "Parameter generally not available"
ERR_16 = "Error data handling with USB"

ERR_NO_LIST = [-6, -8, -9, -10, -11, -12, -13, -14, -15, -16]
ERR_LIST = [
            ERR_6, ERR_8, ERR_9, ERR_10, ERR_11, ERR_12, ERR_13,
            ERR_14, ERR_15, ERR_16
            ]

# ----------------------------------------------------------------------------


# Convert Send Read Command Calculating CRC
# ----------------------------------------------------------------------------


def calculate_send_read_CMD(parameterGroup=None, parameterNumber=None):
    """
    Calculate CRC from parameter group & parameter number 
    to read command to be sent to GRAPHIX
    and make full string command
    """
    # Calculate Checksum Value (CRC)
    # 255 - [(Byte sum of all preceding characters) mod 256]
    # (byte = decimal)
    assert parameterGroup is not None, ValueError(
            'Parameter Group is not defined')
    assert parameterNumber is not None, ValueError(
            'Parameter Number is not defined')
    assert isinstance(parameterGroup, int), ValueError(
            'Parameter Group should be integer')
    assert isinstance(parameterNumber, int), ValueError(
            'Parameter Number should be integer')
    
    pnString = str(parameterNumber)
    sumPNString = 0
    for i in range(len(pnString)):
        sumPNString += ord(pnString[i])
    
    byteSum = (READ_CH + ord(str(parameterGroup))
                + SEPARATE_CH + sumPNString)
    
    checksum = 255 - (byteSum % 256)
    
    if checksum < 32:   # If CRC < 32, 32 should be added to CRC
        checksum += 32
    
    # Make Command with CRC
    sendReadCMD = (chr(READ_CH) + str(parameterGroup)
                        + chr(SEPARATE_CH) + pnString
                        + chr(checksum))
   
    return sendReadCMD
        
            
# ----------------------------------------------------------------------------


# Convert Send Write Command Calculating CRC
# ----------------------------------------------------------------------------


def calculate_send_write_CMD(
                        parameterGroup=None, 
                        parameterNumber=None, 
                        inputValue=None
                        ):
    """
    Calculating from parameter group, parameter number and input value
    to write command to be sent to GRAPHIX
    and make full string command
    """
    # Calculate Checksum Value (CRC)
    # 255 - [(Byte sum of all preceding characters) mod 256]
    # (byte = decimal)
    assert parameterGroup is not None, ValueError(
            'Parameter Group is not defined')
    assert parameterNumber is not None, ValueError(
            'Parameter Number is not defined')
    assert inputValue is not None, ValueError(
            'Input value is not defined')
    assert isinstance(parameterGroup, int), ValueError(
            'Parameter Group should be integer')
    assert isinstance(parameterNumber, int), ValueError(
            'Parameter Number should be integer')
    
    pnString = str(parameterNumber)
    sumPNString = 0
    for i in range(len(pnString)):
        sumPNString += ord(pnString[i])
        
    valString = str(inputValue)
    sumValString = 0
    for i in range(len(valString)):
        sumValString += ord(valString[i])
        
    byteSum = (WRITE_CH + ord(str(parameterGroup))
                + SEPARATE_CH + sumPNString + SEPARATE_CH
                + sumValString + SPACE_CH)
    
    checksum = 255 - (byteSum % 256)
    
    if checksum < 32:   # If CRC < 32, 32 should be added to CRC
        checksum += 32
    
    # Make Command with CRC
    sendWriteCMD = (chr(WRITE_CH) + str(parameterGroup)
                    + chr(SEPARATE_CH) + str(parameterNumber)
                    + chr(SEPARATE_CH) + str(inputValue)
                    + chr(SPACE_CH) + chr(checksum))

    return sendWriteCMD

# ----------------------------------------------------------------------------


# Convert Recieve Value for Read Command
# ----------------------------------------------------------------------------


def convert_receive_read_value(receiveArray):
    """
    Converting from received array to output value
    from GRAPHIX
    """
    receivedChecksum = receiveArray[-2]
    
    if int(receiveArray[0]) == ACK_CH:
        # Check ACK Chracter
        arrayForChecksum = receiveArray[:-2]
        sumForChecksum = sum(arrayForChecksum)
        calChecksum = 255 - (sumForChecksum % 256)
        
        if calChecksum < 32:
            calChecksum += 32
        
        if calChecksum != receivedChecksum:
            # Checksum Error
            return "Error! : CRC is not correct"
            
        else:
            # Return Received Value
            receivedString = ''
            for i in range(len(arrayForChecksum)-1):
                receivedString += chr(arrayForChecksum[i+1])
            return receivedString
    
    elif int(receiveArray[0]) == NACK_CH:
        # Check NACK Chracter
        receiveErrorNumber = int(chr(receiveArray[1]) + chr(receiveArray[2]))
        if receiveErrorNumber == -1:
            receiveErrorNumber = int(chr(receiveArray[1])
                                   + chr(receiveArray[2])
                                   + chr(receiveArray[3]))
        
        if receiveErrorNumber in ERR_NO_LIST:
            # Print Error Message
            indexErr = ERR_NO_LIST.index(receiveErrorNumber)
            return ERR_LIST[indexErr]
            
        else:
            return "Cannot find error matched error number"
            
    else:
        return "Invalid Value Error"
            
# ----------------------------------------------------------------------------


# Convert Receive Value for Write Command
# ----------------------------------------------------------------------------


def convert_receive_write_value(receiveArray):
    """
    Check reaction for sending write command
    """
    receivedChecksum = receiveArray[-2]
    
    if int(receiveArray[0]) == ACK_CH:
        # Check ACK Chracter
        arrayForChecksum = receiveArray[:-2]
        sumForChecksum = sum(arrayForChecksum)
        calChecksum = 255 - (sumForChecksum % 256)
        
        if calChecksum < 32:
            calChecksum += 32
        
        if calChecksum != receivedChecksum:
            # Checksum Error
            return "Error! : CRC is not correct"
            
        else:
            # Print OK Message
            return "OK"
    
    elif int(receiveArray[0]) == NACK_CH:
        # Check NACK Chracter
        receiveErrorNumber = int(chr(receiveArray[1]) + chr(receiveArray[2]))
        if receiveErrorNumber == -1:
            receiveErrorNumber = int(chr(receiveArray[1])
                                   + chr(receiveArray[2])
                                   + chr(receiveArray[3]))
        
        if receiveErrorNumber in ERR_NO_LIST:
            # Print Error Message
            indexErr = ERR_NO_LIST.index(receiveErrorNumber)
            return ERR_LIST[indexErr]
            
        else:
            return "Cannot find error matched error number"
            
    else:
        return "Invalid Value Error"
            
# ----------------------------------------------------------------------------

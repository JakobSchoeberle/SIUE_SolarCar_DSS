def CellDecoder(Frame):
    InstantVoltageH = Frame['data'][1]
    InstantVoltageL = Frame['data'][2]
    InternalResistanceH = Frame['data'][3]
    InternalResistanceL = Frame['data'][4]
    OpenVoltageH = Frame['data'][5]
    OpenVoltageL = Frame['data'][6]

    CellOutput = {
        'Cell ID': Frame['data'][0],
        'InstantVoltage': (int(f'0x{InstantVoltageH:x}{InstantVoltageL:x}', 16))*0.0001,
        'InternalResistance': (int(f'0x{InternalResistanceH:x}{InternalResistanceL:x}', 16))*0.01,
        'OpenVoltage': (int(f'0x{OpenVoltageH:x}{OpenVoltageL:x}', 16))*0.0001,
        'Checksum': Checksum(Frame)
    }
    return CellOutput

def Checksum(Frame):
    BroadcastID = Frame['id']
    checksum = (BroadcastID + 0x8) + Frame['data'][0] + Frame['data'][1] + Frame['data'][2] + Frame['data'][3] + Frame['data'][4] + Frame['data'][5] + Frame['data'][6]
    hex_string = hex(checksum)
    checksum = hex_string[-2:]
    check = f'0x{checksum}'
    #print(check)
    #print(hex(Frame['data'][7]))
    if (int(check, 16) == Frame['data'][7]):
        valid = True
    else:
        valid = False
    return valid
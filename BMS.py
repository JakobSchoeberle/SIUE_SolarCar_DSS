def CellDecoder(Frame):
    BroadcastID = 0x36
    InstantVoltageH = Frame['data'][1]
    InstantVoltageL = Frame['data'][2]
    InternalResistanceH = Frame['data'][3]
    InternalResistanceL = Frame['data'][4]
    OpenVoltageH = Frame['data'][5]
    OpenVoltageL = Frame['data'][6]

    #checksum = hex(BroadcastID, 8)

    #hex(Frame['data'][0]), hex(Frame['data'][1]), hex(Frame['data'][2]), hex(Frame['data'][3]), hex(Frame['data'][4]), hex(Frame['data'][5]), hex(Frame['data'][6]), hex(Frame['data'][7])
    InstantVoltage_strings = [hex(Frame['data'][1]), hex(Frame['data'][2])]
    InstantVoltage = ''.join(InstantVoltage_string[2:].zfill(2) for InstantVoltage_string in InstantVoltage_strings)
    CellOutput = {
        'Cell ID': Frame['data'][0],
        'InstantVoltage': (int(f'0x{InstantVoltageH:x}{InstantVoltageL:x}', 16))*0.0001,
        'InternalResistance': (int(f'0x{InternalResistanceH:x}{InternalResistanceL:x}', 16))*0.01,
        'OpenVoltage': (int(f'0x{OpenVoltageH:x}{OpenVoltageL:x}', 16))*0.0001,
        #'hex0': hex(Frame['data'][0]),
        #'hex1': hex(Frame['data'][1]),
        #'hex2': hex(Frame['data'][2]),
        #'hex3': hex(Frame['data'][3]),
        #'hex4': hex(Frame['data'][4]),
        #'hex5': hex(Frame['data'][5]),
        #'hex6': hex(Frame['data'][6]),
        #'hex7': hex(Frame['data'][7])
    }
    return CellOutput

import json
'''
def SerialDecoder(Str):
    DecodedArray = []
    for x in Str.split(" "):
        if x != '':
            value = int(x)
            DecodedArray.append(value)
    return DecodedArray
'''
def SerialDecoder(byte_string):
    # Remove the leading "b'" and trailing "'"
    string = str(byte_string, encoding='utf-8')
    #print(string)
    # Split the string into an array based on tabs
    data_array = string.split('\t')
    #print(data_array)
    # Convert the string values to integers if needed
    data_array = [int(value) for value in data_array]

    return data_array

def BitDecoder(Int, bit):
    binary_string = bin(Int)

    # Extract binary part without "0b" prefix
    binary_part = binary_string[2:]

    binary_part = binary_part.zfill(16)

    #Flips the string so that it's most-significant bit is in the 15th postion 
    binary_part = binary_part[::-1]

    return int(binary_part[bit])

def Q8Decoder(Int):
    Int = Int / 256
    return Int

def DriveState(Int):
    binary_string = bin(Int)
    binary_part = binary_string[2:]
    binary_part = binary_part.zfill(16)

    # Specify the starting position and length
    start_position = (14-15)*-1
    length = 7

    # Use string slicing to extract the desired part
    result_string = binary_part[start_position:start_position + length]

    return hex(int(result_string, 2))
    '''
    match hex(int(result_string, 2)):
        case "0x10":
            return "DS_startup"
        case "0x51":
            return "DS_standby"
        case "0x50":
            return "DS_nomotor"
        case "0x71":
            return "DS_charging"
        case "0x70":
            return "DS_charging2"
        case "0x40":
            return "DS_shutdown"
        case "0x48":
            return "DS_interlock"
        case "0x44":
            return "DS_enabled"
        case "0x46":
            return "DS_active"
        case "0x468":
            return "DS_transition"
        case _:
            return "ERROR"
    '''

def CurrentLimit(Int):
    '''
    match Int:
        case 0:
            return "FA4_motorT"
        case 1:
            return "FA4_baseplateT"
        case 2:
            return "FA4_undervolt"
        case 3:
            return "FA4_overvolt"
        case 4:
            return "FA4_abslim"
        case 5:
            return "FA4_softlimit"
        case 6:
            return "FA4_thrdisabled"
        case 7:
            return "FA4_rgnphaseIlimit"
        case 8:
            return "FA4_spdgovernor"
        case 9:
            return "FA4_batIlimit"
        case 10:
            return "FA4_batIsoftlimit"
        case 11:
            return "FA4_limphomebatI"
        case 12:
            return "FA4_limphomephaseI"
        case 13:
            return "FA4_vehsoftlimit"
        case 14:
            return "FA4_lowspdregen"
        case 15:
            return "FA4_clutch"
        case 16:
            return "FA4_revgovernor"
        case 17:
            return "FA4_dirlatcherror"
        case _:
            return "ERROR"
    '''
    return "Python is bad"

def ControlPageDecode(String):

    Array = SerialDecoder(String)

    x = {
    'SI_desiredphaseI': (Array[0]*0.1),
    'SI_desiredspd': Array[1],
    'SI_phIramp': Array[2],
    'SI_spdramp': Array[3],
    'SI_thrphaseIlimit': (Array[4]*0.1),
    'SI_rgnphaseIlimit': (Array[5]*0.1),
    'SI_dischargeIlimit': (Array[6]*0.1),
    'SI_chargeIlimit': (Array[7]*0.1),
    'SI_writeenable': Array[8],
    }

    return x

def  InstrumentationPageDecode(String):

    Array = SerialDecoder(String)

    x = {
    'AM_velocity': Array[0],
    'AM_supplyV': (Array[1]*0.1),
    'AM_supplyI': (Array[2]*0.1),
    'AM_baseplateT': (Array[3]*0.1),
    'AM_ambientT': (Array[4]*0.1),
    'AM_motorT': (Array[5]*0.1),
    'AM_SOC': Q8Decoder(Array[6]),
    'AM_thr': Q8Decoder(Array[7]),
    'AM_rgn': Q8Decoder(Array[8]),
    'SV_desiredphaseI': (Array[9]*0.1),
    'SV_desiredspd': Array[10],
    'SV_targetphaseI': (Array[11]*0.1),
    'SV_drivestate': {
        'BIT_initialized': BitDecoder(Array[12], 14),
        'BIT_charging': BitDecoder(Array[12], 13),
        'BIT_motornotready': BitDecoder(Array[12], 12),
        'BIT_interlock': BitDecoder(Array[12], 11),
        'BIT_enabled': BitDecoder(Array[12], 10),
        'BIT_active': BitDecoder(Array[12], 9),
        'BIT_standby': BitDecoder(Array[12], 8),
        'BIT_transition': BitDecoder(Array[12], 7),
        'BIT_INdisable': BitDecoder(Array[12], 3),
        'BIT_limiting': BitDecoder(Array[12], 2),
        'BIT_spdctrl': BitDecoder(Array[12], 1),
        'BIT_reverse': BitDecoder(Array[12], 1),
        'DriveState': DriveState(Array[12])
    },
    'SV_fault1latch': bin(Array[13]),
    'SV_fault1': {
        'FA1_stuckthr': BitDecoder(Array[14], 9),
        'FA1_PDPINT': BitDecoder(Array[14], 6),
        'FA1_lostcomm': BitDecoder(Array[14], 5),
        'FA1_SCItimeoutzero': BitDecoder(Array[14], 4)
    },
    'SV_fault2': {
        'FA2_rgnexcite': BitDecoder(Array[15], 13),
        'FA2_threxcite': BitDecoder(Array[15], 12),
        'FA2_SOClost': BitDecoder(Array[15], 5),
        'FA2_SCInoise': BitDecoder(Array[15], 4),
        'FA2_supplyI': BitDecoder(Array[15], 2),
    }, 
    'SV_fault3': bin(Array[16]), 
    'SV_thrlimit': CurrentLimit(Array[17]), 
    'SV_rgnlimit': CurrentLimit(Array[18]) 
    }

    return x

def DevelopmentPageDecode(String):

    Array = SerialDecoder(String)

    x = {
        'DV_motorTest': (Array[0]*0.1),
        'DV_baseplateTest': (Array[1]*0.1),
        'IN_rgnphaseIlimit': (Array[2]*0.1),
        'IN_status': {
            'IN_disable': BitDecoder(Array[3], 14),
            'IN_noignition': BitDecoder(Array[3], 11),
            'IN_nocbl': BitDecoder(Array[3], 10),
            'IN_pdfault': BitDecoder(Array[3], 9),
            'IN_spdctrl': BitDecoder(Array[3], 6),
            'IN_neutral': BitDecoder(Array[3], 5),
            'IN_thrdisable': BitDecoder(Array[3], 4),
            'IN_reverse': BitDecoder(Array[3], 3),
            'IN_forward': BitDecoder(Array[3], 2),
            'IN_charger': BitDecoder(Array[3], 1),
            'IN_clutch': BitDecoder(Array[3], 0),
        },
        'DV_DIstatus': {
            'DI_noignition': BitDecoder(Array[4], 11),
            'DI_nocbl': BitDecoder(Array[4], 10),
            'DI_pdfault': BitDecoder(Array[4], 9),
            'DI_thrdisable': BitDecoder(Array[4], 4),
            'DI_reverse ': BitDecoder(Array[4], 3),
        },
        'DV_SIstatus': {
            'SI_spdctrl': BitDecoder(Array[5], 6),
            'SI_disable': BitDecoder(Array[5], 5),
            'SI_thrdisable': BitDecoder(Array[5], 4),
            'SI_reverse': BitDecoder(Array[5], 3),
            'SI_forward': BitDecoder(Array[5], 2),
            'SI_charger': BitDecoder(Array[5], 1),
            'SI_clutch': BitDecoder(Array[5], 0)
        },
        'DV_thermallimitmtr': (Array[6]*0.1),
        'DV_baseplateTderating': Q8Decoder(Array[7]),
        'DV_maxphaseIthr': (Array[8]*0.1),
        'DV_maxphaseIrgn': (Array[9]*0.1),
        'DV_batmaxphIthr': (Array[10]*0.1),
        'DV_batmaxphIrgn': (Array[11]*0.1)
    }

    return x

def VehicleConfigurationPageDecode(String):
    Array = SerialDecoder(String)

    x = {
        'VC_SCsupplyI': Array[0],
        'VC_OFsupplyI': (Array[1]*0.1),
        'VC_discrete': {
            'BIT_defaultspdctrl': BitDecoder(Array[2], 13),
            'BIT_invertdir': BitDecoder(Array[2], 12),
            'EN_discreteignition': BitDecoder(Array[2], 11),
            'EN_discretethr': BitDecoder(Array[2], 7),
            'EN_discretethrdisable': BitDecoder(Array[2], 4),
            'EN_discretereverse': BitDecoder(Array[2], 3)
        },
        'VC_invert': {
            'BIT_strictwrongdir': BitDecoder(Array[3], 10),
            'BIT_softstuckthr': BitDecoder(Array[3], 9),
            'INV_discretethrdisable': BitDecoder(Array[3], 4),
            'INV_discretereverse': BitDecoder(Array[3], 3)
        },
        'VC_thringain': Q8Decoder(Array[4]),
        'VC_rgningain': Q8Decoder(Array[5]),
        'VC_thrdeadband': Q8Decoder(Array[6]),
        'VC_rgndeadband': Q8Decoder(Array[7]),
        'VC_thrfilter': Array[8],
        'VC_rgnfilter': Array[9],
        'VC_Xt': Q8Decoder(Array[10]),
        'VC_enginedamping0': Q8Decoder(Array[11]),
        'VC_ enginedamping1': Q8Decoder(Array[12]),
        'VC_Yt0': Q8Decoder(Array[13]),
        'VC_Yt1': Q8Decoder(Array[14]),
        'VC_spd0': Array[15],
        'VC_spd1': Array[15],
        # There is more
    }

    return x
'''
#Page 1: Instrumentation
print("1**?\r") 
Output = "0       1044    0       215     326     201     256     -13     0       0      0                                                                                                             0       20744   0       0       8196    0       6       13"

print(json.dumps(InstrumentationPageDecode(Output)))


#Page 2: Development
print("2**?\r")
Output = "201     215     32767   3604    3607    0       1450    256     0       188     1000    968     5       0"

print(json.dumps(DevelopmentPageDecode(Output)))


#Page 3: Vehicle Configuration
print("3**?\r")
Output = "0       0       7836    520     270     270     -13     -13     84      219     131     0       0       88      163     0       1      9                                                     53      446     481     4088    100     0       0       2000    1058    188     32767   446     627     866     1095    1450    1450   1                                                     450     1450    700     800     900     0       800     1000    850     950     1250    2000    1000    900     0       118     1200   1                                                     000     0       3       150     510     0       0       480     1       150     255     725     737"

print(json.dumps(VehicleConfigurationPageDecode(Output)))


#Page 6: Motor Configuration
print("6**?\r")
Output = "252     0       0"

new_array = SerialDecoder(Output)
print(new_array)

#Page 7: Motor Calibration
print("7**?\r")
Output = "2500    5000    15000   30000   200     400     5316    -611    1       1       -1      -1      341     2048    2650    1100    0      5                                                     0       145"

new_array = SerialDecoder(Output)
print(new_array)

#Page 8: Motor Factory Settings
print("8**?\r")
Output = "1450    920     700     820     920     1000    256     182     105     0       6       423     1024    8000    3000    -21555  0      0"

new_array = SerialDecoder(Output)
print(new_array)

#Page 9: Controller Configuration
print("9**?\r")
Output = "0       0       252     252     252     974     867"

new_array = SerialDecoder(Output)
print(new_array)

'''
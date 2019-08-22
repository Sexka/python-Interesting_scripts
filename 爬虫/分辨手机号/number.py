cnmobile = [134,135,136,137,138,139,150,151,152,157,158,159,182,183,184,187,188,147,178,1705]
cnunion = [130,131,132,155,156,185,186,145,176,1709]
cntelecom = [133,153,180,181,189,177,1700]
 
def num():
    num = input('enter your number:')
    while len(num) != 11:
        if num.startswith(str(cnmobile[:])):
            print('operator : China mobile')
            print('we are sending verification code via text to your phone:',num)
        elif num.startswith(str(cnunion[:])):
            print('operator : China union')
            print('we are sending verification code via text to your phone:',num)
        elif num.startswith(str(cntelecom[:])):
            print('operator : China telecom')
            print('we are sending verification code via text to your phone:',num)
        elif num not in (cnmobile,cnunion,cntelecom):
            print('no such a operator')
            break
    print('invalid length,your number should be in 11 digits')
num()
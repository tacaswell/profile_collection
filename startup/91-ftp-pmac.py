import sys
import subprocess
import os
import time as ttime
import pexpect
from pexpect import pxssh
from ftplib import FTP

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def send_motion_file(orig_file_name, new_file_name = '', orig_file_path = '/GPFS/xf08id/pizza_box_data/', new_file_path = '10', ip = '10.8.2.86'):
    
    # Get number of lines in file
    file_size = file_len(orig_file_path + orig_file_name)
    print('Number of lines in file:', file_size)

    # Create ftp connection with default credential
    ftp = FTP(ip)
    ftp.login()
    s = pxssh.pxssh()
    s.login (ip, 'root', 'deltatau')

    # Check if the directory exists in '/usrflash/lut/. If it does not, create it.'
    if new_file_path != '':
        ftp.cwd('/usrflash/lut/')
        dir_list = ftp.nlst()
        dir_exists = 0
        for dir_name in dir_list:
            if dir_name == new_file_path:
                dir_exists = 1
        if not dir_exists:
            print('mkdir:', '/usrflash/lut/' + new_file_path)
            ftp.mkd('/usrflash/lut/' + new_file_path)
            s.sendline ('chown ftp:root /var/ftp/usrflash/lut/' + new_file_path)
            s.sendline ('chmod a+wrx /var/ftp/usrflash/lut/' + new_file_path)

    # Check if the file already exists in the controller 
    ftp.cwd('/usrflash/lut/' + new_file_path + '/')
    file_list = ftp.nlst()
    file_exists = 0
    if new_file_name == '':
        new_file_name = orig_file_name
    for file_name in file_list:
        if file_name == new_file_name:
            file_exists = 1
    if file_exists == 1:
        if query_yes_no('File "' + new_file_name +'" already exists in the controller. Would you like to replace it?'):
            ftp.delete(new_file_name)
        else:
            print('File already exists, try other name or directory.')
            ftp.close()
            return False

    ftp_file_path = '/var/ftp/usrflash/lut/' + new_file_path + '/' + new_file_name 
    # Open file and transfer to the power pmac
    f = open(orig_file_path + str(orig_file_name), 'rb')
    if(f.readable()):
        result = ftp.storbinary('STOR ' + '/usrflash/lut/' + new_file_path + '/' + new_file_name, f)
        if(result == '226 File receive OK.'):
            s.sendline ('chown ftp:root /var/ftp/usrflash/lut/' + new_file_path + '/' + new_file_name)
            s.sendline ('chmod a+wrx /var/ftp/usrflash/lut/' + new_file_path + '/' + new_file_name)
            sleep(0.001)
            ftp.close()

#    s.prompt(timeout=4)
#    s.sendline('cd /opt/ppmac/usrflash/lut/')
#    s.prompt(timeout=4)
#    s.prompt(timeout=4)
#    s.sendline('ls -l')
#    s.prompt(timeout=4)
#    lsresult = s.before.splitlines()
#    lsresult.pop(0)
#    lsresult.pop(0)
#    dir_exists = 0
#    for x in range(0, len(lsresult)):
#        lsresult[x] = str(lsresult[x])[50:len(str(lsresult[x]))-1]
#        if lsresult[x] == new_file_path:
#            dir_exists = 1
#    if not dir_exists:
#        s.sendline('mkdir ' + new_file_path)
#        s.prompt(timeout=4)

#    s.sendline('cd ' + new_file_path)
#    s.prompt(timeout=10)
#    s.sendline('ls -l')
#    sleep(0.5)
#    s.prompt(timeout=10)
#    lsresult = s.before.splitlines()
#    lsresult.pop(0)
#    lsresult.pop(0)
#    file_exists = 0
#    print(lsresult)
#    for x in range(0, len(lsresult)):
#        lsresult[x] = str(lsresult[x])[str(lsresult[x]).index(":") + 4 : len(str(lsresult[x])) - 1]
#        print(lsresult[x])
#        if lsresult[x] == new_file_name:
#            file_exists = 1
#    if file_exists == 1:
#        if query_yes_no('File "' + new_file_name +'" already exists in the controller. Would you like to replace it?'):
            #print('uai')
#            #s.sendline('rm ' + new_file_name)
#            sleep(0.1)
#        else:
#            print('File already exists, try other name or directory.')
#            ftp.close()
#            return False
            
#    sleep(0.2)
    #print('cp ' + ftp_file_path + ' /opt/ppmac/usrflash/lut/' + new_file_path)
#    s.sendline('cp ' + ftp_file_path + ' /opt/ppmac/usrflash/lut/' + new_file_path)
#    s.prompt(timeout=10)
    #print(s.before)

    print('File sent successfully')
    return True


def transfer_lut(lut_number, ip = '10.8.2.86', filename = 'hhm.txt'):

	class Reader:
		def __init__(self):
			self.rows = 0
		def __call__(self,s):
			self.rows += 1

	hhm.lut_number.put(lut_number)

	ttime.sleep(0.2)
	while (hhm.lut_number_rbv.value != lut_number):
		ttime.sleep(.1)

	hhm.lut_start_transfer.put("1")	
	while (hhm.lut_transfering.value == 0):
		ttime.sleep(.1)
	while (hhm.lut_transfering.value == 1):
		ttime.sleep(.1)

	ftp = FTP(ip)
	ftp.login()
	ftp.cwd('/usrflash/lut/' + str(lut_number))

	file_list = ftp.nlst()
	file_exists = 0
	for file_name in file_list:
		if file_name == filename:
			file_exists = 1
	if file_exists == 0:
		print('File not found. :(\nAre you sure this is the correct lut number?')
	else:
		r = Reader()
		ftp.retrlines('RETR ' + filename, r)
		hhm.cycle_limit.put(r.rows)
		while (hhm.cycle_limit_rbv.value != r.rows):
			ttime.sleep(.1)
		print('Transfer completed!\nNew lut number: ' + str(lut_number) + '\nNumber of points: ' + str(r.rows))
		







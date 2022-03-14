import sys, os
import json
import csv
from datetime import datetime

# my variables in vars.py
## adminuser = "adminuser"
## domain = "domain.lan"
import vars

sys.path.append(os.path.expanduser('../python-common')) # or give the full path
from myutils import chkAlivefping,winrmConnexion,writeToFile,chkEmptyFile,isOpen,search_in_file

def check_is_localadmin(user,host,session):
    command = """$user = \""""+user+"""\";
            $group = "Administrateurs";
            $groupObj =[ADSI]"WinNT://./$group,group" 
            $membersObj = @($groupObj.psbase.Invoke("Members")) 
            $members = ($membersObj | foreach {$_.GetType().InvokeMember("Name", 'GetProperty', $null, $_, $null)})
            If ($members -contains $user) {
                #Write-Host "$user exists in the group $group"
                exit 2
            } Else {
                #Write-Host "$user not exists in the group $group"
                exit 3
            }"""
    
    try:
        print("[*] Testing if : " + user + " is admin on " + host)
        result = session.run_ps(command)
        #print(result.status_code)
        # Si le code de sortie = 2, le compte est admin (exit 2 dans le script powershell),
        # si le code de sortie = 3, le compte n'est pas admin (exit 3)
        return result.status_code

    except Exception as e:
        print("[!] Error ", e.__class__, "occurred.")
        print("[!] Error:" + str(e))
        print("[!] Next entry.")
        now = datetime.now()
        now = now.strftime("%d.%m.%Y %H:%M:%S")
        writeToFile("log.txt",str(now) + " " + host + "Check_is_localadmin erreur\n")
        print()

def remove_admin_account(host,domain,user,session):
    now = ""
    command = "net localgroup Administrateurs "+domain+"\\"+user+" /delete"
    try:
        print("[*] Removing: " + user + " admin priv on " + host)
        result = session.run_ps(command)
        #print(result.std_out)
        #print(result.status_code)

        if result.status_code != 0:
            print("[!] Error, exit code !=0")
            now = datetime.now()
            now = now.strftime("%d.%m.%Y %H:%M:%S")
            writeToFile("log.txt",str(now) + " " + host + " : Erreur"+"\n")
        
        else:
            now = datetime.now()
            now = now.strftime("%d.%m.%Y %H:%M:%S")
            print("[+] Removed " + user + " admin priv on " + host)
            writeToFile("log.txt",str(now) + " " + host + " Removed " + user + " admin priv on " + host + "\n")
            writeToFile("done.txt",host+"\n")

    except Exception as e:
        print("[!] Error ", e.__class__, "occurred.")
        print("[!] Error:"+ e)
        print("[!] Next entry.")
        now = datetime.now()
        now = now.strftime("%d.%m.%Y %H:%M:%S")
        writeToFile("log.txt",str(now) + " " + host + "Remove_admin_account erreur\n")
        print()


def main():
    csvfile = "inventaire.txt"
    # pour chaque ligne du fichier d'inventaire csv
    with open(csvfile, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print("[-] -------------------------------------")
                #print(f'\t{row[0]} | {row[1]} | {row[2]}.')
                line_count += 1
                host = row[0]
                user = row[1]
                domain = row[2]
                # je vérifie si la machine n'est pas déjà traitée
                if not search_in_file(host,"done.txt"):
                    # la machine est-elle reachable ?
                    reachable = chkAlivefping(host)
                    #print(reachable)
                    if reachable:
                        print("[*] Host is reachable: " + host)
                        # test si le port WinRM est accessible
                        if isOpen(host,5985):
                            print("[*] WinRM port isOpen on: " + host)
                            # Etablir la session WinRM
                            session = winrmConnexion(host,vars.domain,vars.adminuser)
                            isAdmin = check_is_localadmin(user,host,session)
                            if isAdmin == 2:
                                print("[*] "+user+" is admin on "+host)
                                remove_admin_account(host,domain,user,session)
                            if isAdmin == 3:
                                print("[*] "+user+" is **not** admin on "+host)
                                now = datetime.now()
                                now = now.strftime("%d.%m.%Y %H:%M:%S")
                                writeToFile("log.txt",str(now) + " " + host + " [!] "+user+" is **not** admin on "+host+"\n")
                                writeToFile("done.txt",host+"\n")
                    else:
                        print("[*] Host is NOT reachable: " + host)

                else:
                    print("[*] Already done: " + host)

if __name__ == "__main__":
    while(True):
        main()
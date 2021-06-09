from update_check import isUpToDate, update
from colorama import Fore, init; init()
import os, requests


class Console:
    def PrintLogo(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'''
     _____                         
    /  ___|                        
    \ `--.  ___ ______ _ _ __ ___  
     `--. \/ _ \_  / _` | '_ ` _ \ 
    /\__/ /  __// / (_| | | | | | |  {Fore.RED}https://github.com/Its-Vichy{Fore.RESET}
    \____/ \___/___\__,_|_| |_| |_| DISCORD TOKEN GRABBER REVERSER
    
    ''')

    def Printer(self, color, past, text):
        print(f'{Fore.WHITE}[{color}{past}{Fore.WHITE}] {text}.')

class Extractor:
    def __init__(self):
        self.ExecutableName = input(f'{Fore.WHITE}[{Fore.CYAN}?{Fore.WHITE}] File name: ') + '.exe'
        self.DeletedHook    = (input(f'{Fore.WHITE}[{Fore.CYAN}?{Fore.WHITE}] Delete hook (y/n): ').lower())[:1]
        self.SpamHook       = (input(f'{Fore.WHITE}[{Fore.CYAN}?{Fore.WHITE}] Spam hook (y/n): ').lower())[:1]
        self.Console = Console()
        self.Hook = [ ]

    def Uncompile(self):
        os.system(f'cd ./dist/input/ && python ../../Modules/pyinstxtractor.py "{self.ExecutableName}"')
        self.Console.PrintLogo()

    def CheckUpdate(self):
        if isUpToDate('./Sezam.py', 'https://raw.githubusercontent.com/Its-Vichy/Sezam/main/Sezam.py') == False:
            self.Console.Printer(Fore.YELLOW, '*', 'New update was found, downloading...')
            update('./Sezam.py', 'https://raw.githubusercontent.com/Its-Vichy/Sezam/main/Sezam.py')

    def GetHooks(self):
        base  = ''
        try:
            for file in os.listdir(f'./dist/input/{self.ExecutableName}_extracted/'):
                if '.exe.manifest' in file:
                    base = file.split('.exe.manifest')[0]

                    if 'pyi-windows-manifest-filename' not in base:
                        with open(f'./dist/input/{self.ExecutableName}_extracted/{base}', 'r+', encoding= 'utf-8', errors= 'ignore') as input_file:
                            for line in input_file:
                                if 'PYARMOR' in line:
                                    self.Console.Printer(Fore.RED, '*', 'Pyarmor was detected')

                                if '/api/webhooks/' in line:
                                    hook = (line.split('/api/webhooks/')[1])[:87].split(')')[0]
                                    self.Hook.append(f'https://discord.com/api/webhooks/{hook}')

                                if 'https://pastebin.com/raw/' in line:
                                    hook = f'https://pastebin.com/raw/{(line.split("https://pastebin.com/raw/")[1])[:8]}'
                                    resp = requests.get(hook).text
                                    
                                    if '/api/webhooks/' in resp:
                                        splithook = (resp.split('/api/webhooks/')[1])[:87]
                                        self.Hook.append(f'https://discord.com/api/webhooks/{splithook}')
                                        self.Console.Printer(Fore.GREEN, '*', f'Found pastebin with webhook: {hook}')
                                    else:
                                        self.Console.Printer(Fore.GREEN, '*', f'Found pastebin but no webhook: {hook}')
                                    
                                    if 'https://discord.gg/' in resp:
                                        invite = (resp.split("https://discord.gg/")[1])[:10]
                                        resp = requests.get(f'https://discord.com/api/v6/invite/{invite}').json()

                                        if 'Unknown Invite' in resp:
                                            self.Console.Printer(Fore.RED, '*', f'Found Invalid Discord invite in pastebin: https://discord.gg/{invite}')
                                        else:
                                            self.Console.Printer(Fore.GREEN, '*', f'Invite from {resp["guild"]["name"]} found in pastebin, invited by {resp["inviter"]["username"]}#{resp["inviter"]["discriminator"]} https://discord.gg/{invite}')

                                if 'https://discord.gg/' in line:
                                    invite = (line.split("https://discord.gg/")[1])[:10]
                                    resp = requests.get(f'https://discord.com/api/v6/invite/{invite}').json()
                                    
                                    if 'Unknown Invite' in resp:
                                        self.Console.Printer(Fore.RED, '*', f'Found Invalid Discord invite in pastebin: https://discord.gg/{invite}')
                                    else:
                                        self.Console.Printer(Fore.GREEN, '*', f'Invite from {resp["guild"]["name"]} found in pastebin, invited by {resp["inviter"]["username"]}#{resp["inviter"]["discriminator"]} https://discord.gg/{invite}')

        except Exception as err:
            self.Console.Printer(Fore.RED, '-', f'Error: {err}')

    def Show(self):
        for hook in self.Hook:
            self.Console.Printer(Fore.GREEN, '+', hook)

    def Fuck(self):
        for hook in self.Hook:
            try:
                resp = requests.get(hook)
                if 'Unknown Webhook' not in resp.text:
                    self.Console.Printer(Fore.YELLOW, '*', f'Hook name: {resp.json()["name"]}, spamming webhook')
                    
                    if self.SpamHook == 'y':
                        for _ in range(15):
                            requests.post(hook, json={'content': '> ||@everyone|| Sezam was here - https://github.com/Its-Vichy/Sezam'})
                    
                    if self.DeletedHook == 'y':
                        requests.delete(hook)

                        self.Console.Printer(Fore.CYAN, '+', 'Webhook deleted')
                else:
                    self.Console.Printer(Fore.CYAN, '*', 'Webhook was dead')
            except Exception as err:
                self.Console.Printer(Fore.RED, '-', f'Error, can\'t use this webhook')

        self.Console.Printer(Fore.CYAN, '+', 'Finished')

Console().PrintLogo()
Ex = Extractor()
Ex.CheckUpdate()
Ex.Uncompile()
Ex.GetHooks()
Ex.Show()
Ex.Fuck()

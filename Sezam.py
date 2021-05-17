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
        self.Console = Console()
        self.Hook = [ ]

    def Uncompile(self):
        os.system(f'cd ./dist/input/ && python ../../Modules/pyinstxtractor.py "{self.ExecutableName}"')
        self.Console.PrintLogo()

    def GetHooks(self):
        base  = ''
        try:
            for file in os.listdir(f'./dist/input/{self.ExecutableName}_extracted/'):
                if '.exe.manifest' in file:
                    base = file.split('.exe.manifest')[0]

                    if 'pyi-windows-manifest-filename' in base:
                        continue

                    with open(f'./dist/input/{self.ExecutableName}_extracted/{base}', 'r+', encoding= 'utf-8', errors= 'ignore') as input_file:
                        for line in input_file:
                            if 'https://discord.com/api/webhooks/' in line:
                                hook = (line.split('https://discord.com/api/webhooks/')[1])[:87]
                                self.Hook.append(f'https://discord.com/api/webhooks/{hook}')

                            if 'https://pastebin.com/raw/' in line:
                                hook = f'https://pastebin.com/raw/{(line.split("https://pastebin.com/raw/")[1])[:8]}'
                                resp = requests.get(hook).text
                                
                                if 'https://discord.com/api/webhooks/' in resp:
                                    splithook = (resp.split('https://discord.com/api/webhooks/')[1])[:87]
                                    self.Hook.append(f'https://discord.com/api/webhooks/{splithook}')
                                    self.Console.Printer(Fore.GREEN, '*', f'Found pastebin with webhook: {hook}')
                                else:
                                    self.Console.Printer(Fore.GREEN, '*', f'Found pastebin but no webhook: {hook}')
                                
                                if 'https://discord.gg/' in line:
                                    invite = (line.split("https://discord.gg/")[1])[:10]
                                    resp = requests.get('https://discord.com/api/v6/invite/{invite}').json()

                                    if resp['message'] != 'Unknown Invite':
                                        self.Console.Printer(Fore.GREEN, '*',f'Invite from {resp["guild"]["name"]} found in pastebin, invited by {resp["inviter"]["username"]}#{resp["inviter"]["discriminator"]} https://discord.gg/{invite}')
                                    else:
                                        self.Console.Printer(Fore.RED, '*', f'Found Invalid Discord invite in pastebin: https://discord.gg/{invite}')

                            if 'https://discord.gg/' in line:
                                invite = (line.split("https://discord.gg/")[1])[:10]
                                resp = requests.get('https://discord.com/api/v6/invite/{invite}').json()

                                if resp['message'] != 'Unknown Invite':
                                    self.Console.Printer(Fore.GREEN, '*', f'Invite from {resp["guild"]["name"]} found, invited by {resp["inviter"]["username"]}#{resp["inviter"]["discriminator"]} https://discord.gg/{invite}')
                                else:
                                    self.Console.Printer(Fore.RED, '*', f'Found Invalid Discord invite: https://discord.gg/{invite}')
        except Exception as err:
            self.Console.Printer(Fore.RED, '-', f'Error, not a python exe')

    def Show(self):
        for hook in self.Hook:
            self.Console.Printer(Fore.GREEN, '+', hook)

    def Fuck(self):
        for hook in self.Hook:
            try:
                resp = requests.get(hook)
                if 'Unknown Webhook' not in resp.text:
                    self.Console.Printer(Fore.YELLOW, '*', f'Hook name: {resp.json()["name"]}, spamming webhook')
                    for _ in range(15):
                        requests.post(hook, json={'content': '> ||@everyone|| Sezam was here - https://github.com/Its-Vichy'})
                    requests.delete(hook)

                    self.Console.Printer(Fore.CYAN, '+', 'Webhook deleted')
                else:
                    self.Console.Printer(Fore.CYAN, '*', 'Webhook was dead')
            except Exception as err:
                self.Console.Printer(Fore.RED, '-', f'Error, can\'t use this webhook')

Console().PrintLogo()
Ex = Extractor()
Ex.Uncompile()
Ex.GetHooks()
Ex.Show()
Ex.Fuck()

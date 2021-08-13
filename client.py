import socket
import threading

nickname = input("Choose a nickname: ")

if nickname.lower() == 'admin':
   password = input("Password for Admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1' #localhost
port = 55555
client.connect((host, port))

stop_thread = False

def receive():
   while True:
      global(stop_thread)
      if stop_thread:
         break

      try:
         message = client.recv(1024).decode('ascii')
         if message == 'NICK':
            client.send(nickname.encode('ascii'))
            next_message = client.recv(1024).decode('ascii')

            if next_message == 'PASSWORD':
               client.send(password.encode('ascii'))

               if client.recv(1024).decode('ascii') == 'REFUSED':
                  print("Connection was refused! Wrong admin password.")
                  stop_thread = True

         else:
            print(message)

      except:
         print("An error occurred!")
         client.close()
         break

def write():
   while True:
      if stop_thread:
         break

      message = f'{nickname}: {input("")}'
      if message[len(nickname)+2:].startswith('/'):
         if nickname == 'admin':
            if message[len(nickname)+2:].startswith('/kick'):
               client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
            
            elif message[len(nickname)+2:].startswith('/ban'):
               client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))

         else:
            print("Commands can only be executed by the admin.")

      else:
         client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
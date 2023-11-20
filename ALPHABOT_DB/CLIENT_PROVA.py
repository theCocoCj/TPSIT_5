import socket as sck
import time
from threading import Thread

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

CLIENT_TUPLA_IP_PORTA = ('127.0.0.1',5000)
SEPARATOR = ';'

class ThreadMex(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        
        while True:
        
            command = input("Inserisci la ricerca che si vuole effettuare: ")
            
            if ((command.upper()=='FF') or (command.upper()=='NF') or (command.upper()=='FHS') or (command.upper()=='FH')):
                file_name = input("Inserisci il nome del file")
                mex = f'{command};{file_name};{-1}'
                
                if (command.upper()=='FH'):
                    fragment_id = input("Inserisci il numero del frammento")
                    mex = f'{command};{file_name};{fragment_id}'
            
            #EXIT del programma      
            elif (command.upper()=='E'):
                break 
            
            else:
                print("COMANDO INSERITO ERRATO O NON PRESENTE")
            
            s.sendall(mex.encode())
            
        s.close()
        
class ThreadMexrecv(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            request = s.recv(4096).decode().split(SEPARATOR)
            print(f'request: {request[0]}, returning: {request[1]}')


"""
-chiedere al server se un certo nome file è presente;
-chiedere al server il numero di frammenti di un file a partire dal suo nome file;
-chiedere al server l'IP dell'host che ospita un frammento a partire nome file e dal numero del frammento;
-chiedere al server tutti gli IP degli host sui quali sono salvati i frammenti di un file a partire dal nome file.

"""

# presenza file-->nome file
#FF-->FIND FILE

# numero frammenti-->nome file
#NF-->NUMBER OF FRAGMENTS

# IP dell' host con frammento x-->nome file e x
#FH--> FIND HOST

# IP degli host con frammenti di file--> nome file
#FHS-->FIND HOSTS

def main():
    s.connect(CLIENT_TUPLA_IP_PORTA)
    t = ThreadMex()
    t.start()
    

    

if __name__ == '__main__':
    main()



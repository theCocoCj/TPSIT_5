import sqlite3
import socket as sck
import time
from threading import Thread

SEPARATOR = ';'

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

class ThreadSend(Thread):
    def __init__(self, connesione):
        super().__init__()
        self.connessione = connesione

    def run(self):
        
        while True:
            mex = self.connessione.recv(4096).decode()
        
            mexSplitted = mex.split(SEPARATOR)
            
            request = mexSplitted[0]
            file_name = mexSplitted[1]
            fragment_id = int(mexSplitted[2])
            
            list = find_function(request, file_name, fragment_id)
            
            if (request.upper()=='FF'):
                if list[0] == file_name[0]:
                    mex_send = f'Il file esiste'
            elif (request.upper()=='NF'):
                mex_send = f'n: {list[0]} fragments'
            elif (request.upper()=='FHS'):
                mex_send = f'hosts: {list}'
            elif (request.upper()=='FH'):
                mex_send = f'hosts: {list[0]}'
            else:
                print("Invalid request")
                
            mex_send.encode()
            s.sendall(mex_send)


def find_function(request, file_name, fragment_id):
    con=sqlite3.connect("file.db")
    cur=con.cursor()
    
    if (request.upper()=='FF'):
        res=cur.execute(f"SELECT nome FROM files WHERE files.nome = '{file_name}'") #ritorna nome file 
         
    elif (request.upper()=='NF'):
        res=cur.execute(f"SELECT tot_frammenti FROM files WHERE files.nome = '{file_name}'") #ritorna numero frammenti

    elif (request.upper()=='FHS'):
        res=cur.execute(f"SELECT host FROM frammenti, files WHERE files.nome = '{file_name}' AND files.id_file = frammenti.id_file'") #ritorna lista host

    elif (request.upper()=='FH'):
        res=cur.execute(f"SELECT host FROM frammenti, files WHERE files.nome = '{file_name}' AND files.id_file = frammenti.id_file AND frammenti.id_frammento = '{fragment_id}'")  #ritorna host
    else:
        print("Invalid request")
        
    lista = res.fetchall()
    return lista
        

def main():
    SERVER_TUPLA_IP_PORTA = ('0.0.0.0', 5000)
    s.bind(SERVER_TUPLA_IP_PORTA)
    s.listen()

    connesione, clientAddress = s.accept()
    thread = ThreadSend(connesione)
    thread.start()
        
if __name__ == '__main__':
    main()
       
            

                
    
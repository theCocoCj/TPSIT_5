import socket as sck
from threading import Thread
import sqlite3 as sql

SERVER_IP = ("127.0.0.1", 8000)


class Client(Thread):
    """
    La classe client serve per gestire le operazione del client
    """
    def __init__(self, connection : sck.socket, address_client):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        while True:
            message = self.connection.recv(4096).decode()            
            liv_fiume = int(message.split(";")[0])
            data = message.split(";")[1]
            identificativo = int(message.split(";")[2])
            
            dati = self.controllo_db(liv_fiume, data, identificativo)
            #livello misurato < 30% -->messaggio di ricezione al client
            #livello misurato >= 30% AND < 70%--> messaggio di ricezione al client e stampa ALLARME su server
            #livello misurato >= 70%--> messaggio-->messaggio di ALLARME al client e stampa ALLARME su server
            #su server fiume, località, data_ora
            
            #livello del client / livello db *100
            id_stazione_db = dati[0]
            fiume_db = dati[1]
            loc_db = dati[2]
            liv_db = dati[3]
            
            #calcolo percentuale livello fiume rispetto al livello di guardia
            perc = liv_fiume / liv_db * 100
            print(f"percentuale: {perc}") 
            
            #gestione delle casistiche ed invio messaggio al client
            if perc > 30 :
                self.connection.sendall(b"messaggio ricevuto correttamente")
            elif perc >= 30 and perc < 70:
                self.connection.sendall(b"messaggio ricevuto correttamente")
                print(f"ALLARME {fiume_db} nella località di {loc_db}, il {data} ")
            else:
                self.connection.sendall(b"ALLARME")
                print(f"ALLARME alla stazione: {id_stazione_db}, fiume: {fiume_db} nella località di {loc_db}, il {data} ")
            
            
    def controllo_db(self, liv_fiume, data, identificativo):
        #connessione al db
        con=sql.connect("fiumi.db")
        cur=con.cursor()
        #esecuzione query nel db
        res=cur.execute(f"SELECT * FROM livelli WHERE id_stazione = '{identificativo}'")
        dati=res.fetchall()
        
        con.close()#chiusura connessione con il db
        print(dati[0])
        return dati[0]
                 
def main():
    #creazione del client
    server = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    
    #Associa al socket del server una tupla contenente ip e porta 
    server.bind(SERVER_IP)

    #abilita alla ricezione delle connessioni
    server.listen()

    while True:
        #accettazione messaggio da parte del client
        connection, address_client = server.accept()
        
        #Creazione di un thread per ogni client che si connette
        client = Client(connection, address_client)
        client.start()
        

if __name__ == "__main__":
    main()
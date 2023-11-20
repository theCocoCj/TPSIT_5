import socket as sck #libreria socket
import time
import random
import datetime

SERVER_IP = ("127.0.0.1", 8000)


def main():
    client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)#creazione del client
    client.connect(SERVER_IP)#connessione al server
    
    #ogni quanto tempo il client invia i dati
    tempo_invio = input("Inserisci ogni quanti secondi vuoi inviare il messaggio al server:")
    #identifica il client che invia i dati
    identificativo = input("Inserisci l'dentificativo del client: ")

    
    while True:
        """
        Messaggio inviato al server = livello_fiume;data_ora;identificativo
        ogni 15 secondi
        """
        messaggio = f"{random.randint(1,15)};{str(datetime.datetime.now())};{identificativo}".encode() 
        client.sendall(messaggio)
        
        messaggio_recv = client.recv(4096).decode()
        
        print(messaggio_recv)
        time.sleep(int(tempo_invio))

    client.close()

if __name__ == "__main__":
    main()
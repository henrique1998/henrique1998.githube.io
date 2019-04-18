#importa biblioteca socket 
from socket import *

#cria o socket TCP
ss = socket(AF_INET, SOCK_STREAM)

#conecta o socket ss ao endereco da porta 
ss.bind(('', 8080))
#coloca o socket do  servidor em modo de escuta (modo passivo)
ss.listen(1)

while True:
    print ('Pronto para receber...')
    connectionSocket, addr = ss.accept()
#o socket aceita uma nova conexao retornando uma tupla com a conexão realizada (o novo objeto socket e o endereco que o socket esta comunicando)
    print ('Conectado por ', addr)
    try:
#lê os bytes recebidos, retornando-os em uma string, até o limite de buffer
        message = connectionSocket.recv(1024)
        print (message)
        metodo = message.split()[0] # para saber o metodo
        print (metodo)
        if metodo == b'GET':
	        filename = message.split()[1]
	        tipoarq = filename.split(b'.')[1]  # para saber o tipo do arquivo sendo solicitado
	        print (tipoarq)
	        print (filename)
	        f = open(filename[1:])
	        # metodo read le todo o conteudo do arquivo
	        if tipoarq == b'html':
	          outputdata = f.read()
	          print (outputdata)
	          f.close()
	          #envia ao socket a linha de status e as linhas de cabecalho de resposta HTTP 
	          connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
	          connectionSocket.send(b'Server: Meu server/1.0\r\n')
	          connectionSocket.send(b'Date: Sun, 14 Apr 2019 14:00:00 GMT\r\n')
	          connectionSocket.send(b'Content-Type: text/html\r\n\r\n')
	          #envia o conteudo do arquivo solicitado pelo GET ao cliente
	          for i in range(0, len(outputdata)):
	           connectionSocket.send(outputdata[i].encode('utf-8'))
	        if tipoarq == b'jpg': 
	          with open(filename.split(b'/')[1],'rb') as f:
	              connectionSocket.send(f.read())
	              l = f.read
	              f.close()

        if metodo == b'POST':
	        filename = message.split()[1]
	        tipoarq = filename.split(b'.')[1]  #para saber o tipo do arquivo sendo solicitado
	        print (tipoarq)
	        print (filename)
	        #envia ao socket a linha de status e as linhas de cabecalho de resposta HTTP 
	        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n')
	        connectionSocket.send(b'Server: Meu server/1.0\r\n')
	        connectionSocket.send(b'Date: Sun, 14 Apr 2019 14:00:00 GMT\r\n')
	        connectionSocket.send(b'Content-Type: text/html\r\n\r\n')
	        if tipoarq == b'php':
	          conteudo_post = message.split(b'\r\n\r\n')[1] 
	          print (conteudo_post)
        connectionSocket.close()

    except IOError:
        #Envia mensagem de response  file not found
        connectionSocket.send(b'HTTP/1/1 404 Not Found\r\n\r\n')
        #connectionSocket.send(b'404 Not Found')
        #Fecha client socket
        connectionSocket.close()
ss.close() 



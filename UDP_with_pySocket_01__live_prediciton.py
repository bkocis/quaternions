import socket
import time
import select
from sklearn.neighbors import KNeighborsClassifier 
import numpy as np
import pandas as pa
from sklearn.model_selection import train_test_split 

"""
https://www.binarytides.com/programming-udp-sockets-in-python/
https://docs.python.org/3/howto/sockets.html
https://stackoverflow.com/questions/18743962/python-send-udp-packet


good advice on the case of blocking sockets / socket read

https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method


"""


def read_data_stream(knn):
	#IP = "192.168.7.36"	# test in DA_stream
	IP = "192.168.0.113"	# on demolink
	port = 8000 #2390

	while time.time() <time.time()+1:    
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(bytes('give_me_my_data',"utf-8"), (IP, port))

		sock.setblocking(0)
		ready = select.select([sock], [], [], 0.5)
		if ready[0]:
			b = sock.recvfrom(120)

		if b!=():
			pass
		else:
			print('empty b')
		data = b[0]
		clm = "{}".format(data)
		time.sleep(0.01)
		#print(clm)
		l = clm.split()
		x = np.array([[l[-5],l[-4],l[-3]]])
		print(x)

		# The prediction is provided live in the stdout 
		print(knn.predict(x))


if __name__=="__main__":
	# read in data and add label column
#	df_LL = pa.read_csv('./data_labeled/day_3/test_data_LL_2_.txt', sep=' ')
#	df_LR = pa.read_csv('./data_labeled/day_3/test_data_LR_2_.txt', sep=' ')
#	df_UL = pa.read_csv('./data_labeled/day_3/test_data_UL_2_.txt', sep=' ')
#	df_UR = pa.read_csv('./data_labeled/day_3/test_data_UR_2_.txt', sep=' ')
	df_LL = pa.read_csv('test_data_LL_2_.txt', sep=' ')
	df_LR = pa.read_csv('test_data_LR_2_.txt', sep=' ')
	df_UL = pa.read_csv('test_data_UL_2_.txt', sep=' ')
	df_UR = pa.read_csv('test_data_UR_2_.txt', sep=' ')
	df_LL['label'] = 'LL'
	df_LR['label'] = 'LR'
	df_UL['label'] = 'UL'
	df_UR['label'] = 'UR'
	# merge all labeled sets 
	df_labeled = df_LL.append(df_LR)
	df_labeled = df_labeled.append(df_UL)
	df_labeled = df_labeled.append(df_UR)


	X=df_labeled[['qx','qy','qz']] # ; X = np.array(X)
	y=df_labeled.label


	# dividing X, y into train and test data 
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0) 

	# training a KNN classifier  - 4 classes [LowerLeft, LowerRight, UpperRight, UpperLeft]
	knn = KNeighborsClassifier(n_neighbors = 4 ).fit(X_train, y_train) 
	
	# forward the model to the data stream, where the prediction will be executed
	read_data_stream(knn)



######
"""
references: 
https://pythontic.com/modules/socket/udp-client-server-example


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")
# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)


"""

# !/usr/bin/env python
# nutclient.py
# Just the pimpest nutclient in the world
# Logan Graba
# July 02, 2017

import socket
import sys
import time
import transaction
import re

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
host, port = server_address
print("Connecting to {}:{}...".format(host, port))
sock.connect(server_address)

try:
	txs = []
	# Get and Send Data
	print("Please enter your transactions, one line at a time:\n")
	while True:
		line = input()
		if line:
			# Transaction
			tx = transaction.Transaction(line)

			txs.append(tx)
		else:
			break
	
	total_length = 0
	# Send Transactions
	for tx in txs:
		print("Sending {} to {} from {}".format(tx.amount, tx.receiver, tx.sender))
		# print(tx)
		
		# Send raw data (in bytes)
		tx_bytes = tx.byte_representation()
		sock.sendall(tx_bytes)
		total_length += len(tx_bytes)

	# Gather Response
	amount_received = 0
	amount_expected = total_length
	data = b''

	# Get raw data
	while amount_received < amount_expected:
		data += sock.recv(4096)
		amount_received += len(data)

	# Split and De-serialize transaction bytes
	split_data = data.split(b'\x80\x03')
	print("Received: ")
	for tx_data in split_data:
		if tx_data:
			received_tx = transaction.Transaction(None, tx_data)
			print(received_tx)

finally:
	print("Closing Socket... ")
	sock.close()
	print("Complete!\n")
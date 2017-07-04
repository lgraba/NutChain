# !/usr/bin/env python
# nutclient.py
# Just the pimpest nutclient in the world
# Logan Graba
# July 02, 2017

import os
import socket
import sys
import time
import transaction
import re
import account

# Server Details
host = 'localhost'
port = 10000
accounts_dir = 'accounts'
accounts_ext = '.pk'

class NutClient:

	def __init__(self, host, port):
		# Create TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the socket to the port where the server is listening
		server_address = (host, port)
		# server_address = ('localhost', 10000)
		print("Connecting to {}:{}...".format(host, port))
		self.sock.connect(server_address)

		# Read Accounts file: accounts.data
		# { 'logan': [[privateKey PEM], [publivKey PEM]] }
		print("Reading Accounts...")
		self.accounts = self.readAccounts(accounts_ext)
		if (not self.accounts):
			print("Could not find any local Accounts. Make sure you have private and public PEM files in {}".format(accounts_dir))
			# sys.exit()

	def clientLoop(self):
		try:
			txs = []
			# Get and Send Data
			print("Please enter your commands, one line at a time:\n")
			while True:
				line = input()
				if line:
					# Check the initial command word
					send_array = ['Give', 'give', 'Send', 'send', 'Shoot', 'shoot', 'Slide', 'slide']
					create_account_array = ['Create', 'create', 'Spawn', 'spawn', 'Stake', 'stake']
					account_array = ['Account', 'account', 'Address', 'address']
					words = line.split()
					if (words[0] in send_array):
						# It's a Transaction
						tx = transaction.Transaction(line)
						txs.append(tx)
					elif (words[0] in create_account_array):
						# It's an Account Creation
						if (words[1] in account_array):
							new_account = account.Account(words[2])
						else:
							new_account = account.Account(words[1])
				else:
					break
			
			total_length = 0
			# Send Transactions
			for tx in txs:
				print("Sending {} to {} from {}".format(tx.amount, tx.receiver, tx.sender))
				# print(tx)
				
				# Send raw data (in bytes)
				tx_bytes = tx.byte_representation()
				self.sock.sendall(tx_bytes)
				total_length += len(tx_bytes)

			# Gather Response
			amount_received = 0
			amount_expected = total_length
			data = b''

			# Get raw data
			while amount_received < amount_expected:
				data += self.sock.recv(4096)
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
			self.sock.close()
			print("Complete!\n")

	def readAccounts(self, filename):
		accounts = [] # Array of dirty dicts
		try:
			for file in os.listdir(accounts_dir):
				if file.endswith(accounts_ext):
					name = file.split('.')[0]
					# print("Reading Account: {}".format(name))
					read_account = account.Account(name, True)
					accounts.append(read_account)
		except IOError as err:
			print("I/O error: {0}".format(err))
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

		return accounts

	def instructions(self):
		print("Commands:\n\t>> Create/Spawn/Stake [account_name]\n\t>> Send/Give/Shoot/Slide [recipient_account] [amount] from [sender_account]")


# MAIN
if __name__ == "__main__":
	client = NutClient(host, port)
	client.instructions()
	client.clientLoop()
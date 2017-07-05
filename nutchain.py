# !/usr/bin/env python
# nutchain.py
# Just the pimpest nutchain in the world
# Logan Graba
# July 02, 2017

import os
import hashlib
import configparser
import time
import nutserver
import transaction
import pickle
import account

class NutChain:
	"""NutChain: A super-sexy NutChain"""

	# Bytes
	leaf_byte = bytes(0)
	node_byte = bytes(1)
	version = '.01'
	difficulty = 1
	nonce = 0

	def __init__(self):
		self._linelength = 40
		# Start Server
		self.server = nutserver.NutServer()
		# Start Merkle Tree from Genesis Nut
		self.__MT__()

	# __MT__()
	# Create and print Merkel Sack from Config File
	def __MT__(self):
		# Initialize with Genesis Nut
		genesis_nut = self.readconfig()
		previous_nut = genesis_nut

		# Make a new Nut for each set of transactions received via Server
		while True:
			txs = self.server.startListening()
			if (txs):
				previous_nut = self.newNut(previous_nut, txs)
				print(previous_nut)

	# readconfig()
	# Read a configuration file which represents the Genesis Nut
	def readconfig(self):
		self.Config = configparser.ConfigParser()
		self.Config.read("genesis.nut")
		header = self.configSectionMap('Header')
		transactions = self.configSectionMap('Transactions')
		accounts = self.configAccountMap('Accounts')

		data = {}
		data['header'] = header
		data['transactions'] = transactions
		data['accounts'] = accounts

		print("Genesis block read")
		self.line()

		return data

	# configSectionMap()
	# Break out each section from the configuration file (Genesis Nut) into a Dictionary
	def configSectionMap(self, section):
		data = {}
		options = self.Config.options(section)
		for option in options:
			try:
				data[option] = self.Config.get(section, option)
				if data[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("Header/Txs; exception on %s!" % option)
				data[option] = None
		return data

	# configAccountMap()
	# Break out the Accounts section from the configuration file (Genesis Nut) into a NamedTuple
	def configAccountMap(self, section):
		accounts = {}
		options = self.Config.options(section)
		for option in options:
			try:
				pair = self.Config.get(section, option)
				strip_pair = pair.strip("()")
				split_pair = strip_pair.split(",")
				name = split_pair[0].strip()
				value = float(split_pair[1].strip())

				# data[option] = account.Acc(name, value)
				server_dict = {option:value}
				accounts[option] = account.Account(name, False, server_dict)

				if accounts[option] == -1:
					DebugPrint("skip: %s" % option)

			except Exception as err:
				print("Accounts; exception on %s!" % option)
				print(err)
				accounts[option] = None
		return accounts

	# newNut()
	# Create a new Nut with the given Transactions
	def newNut(self, prev, new_transactions):
		self.line()
		print("We're going to make a new Nut with the following shit:")
		print("Previous Block: ")
		print(prev)
		print("New Transactions: ")

		# Unpack prev
		previous_header = prev['header']
		previous_transactions = prev['transactions']
		previous_accounts = prev['accounts']

		# New Transactions to add to New Nut
		transactions = {}

		# Loop through new transactions array
		for transaction in new_transactions:
			# Balance Accounts
			try:
				result = self.balanceAccounts(previous_accounts, transaction)
				if result:
					raise Exception(result)
			except Exception as e:
				print("Could not balance accounts for transaction: " + transaction.sender + " [" + str(transaction.amount) + "] => " + transaction.receiver + "; ERROR: ")
				print(e)
				continue

			# TODO: VERIFY TRANSACTION

			# Convert to bytes, hash
			m = hashlib.md5()
			m.update(transaction.byte_representation())
			tx_hash = m.hexdigest()

			# Add transactions from array to transactions dictionary -> (eventually) Transactions Section
			transactions[tx_hash] = transaction

		self.line()

		# Hash each tx_hash (keys of transactions dictionary)
		mh = hashlib.md5()
		for tx_hash, transaction in transactions.items():
			mh.update(tx_hash.encode('utf-8'))
		
		crush = mh.hexdigest()

		# Make pre_header
		pre_header = {
			'version':self.version,
			'previous':previous_header['hash'],
			'crush':crush,
			'time':time.time(),
			'difficulty':self.difficulty,
			'nonce':self.nonce
		}

		# Hash pre_header to get Nut Crush (Hash)
		ph = hashlib.md5()
		for element in pre_header:
			# print("Adding " + str(element) + " to Preheader hash")
			ph.update(element.encode('utf-8'))
		nut_hash = ph.hexdigest()

		# Header
		header = {
			'hash': nut_hash,
			'version':self.version,
			'previous':previous_header['hash'],
			'crush':crush,
			'time':time.time(),
			'difficulty':self.difficulty,
			'nonce':self.nonce
		}
		# print(header)

		# Balance Accounts
		accounts = previous_accounts

		# Make Nut
		nut = {}
		nut['header'] = header
		nut['transactions'] = transactions
		nut['accounts'] = accounts
		
		return nut # New nut

	# balanceAccounts()
	# Check validity of all transactions based on Accounts and update Accounts
	def balanceAccounts(self, prev_accounts, transaction):
		print(transaction)

		# Transaction specifics
		sender = transaction.sender
		amount = transaction.amount
		receiver = transaction.receiver

		# Balance each Account by publicKey or Name
		inNotFound = True
		outNotFound = True
		for account in prev_accounts.items():
			# Subtract Inputs from Accounts
			if (account.publicKey == sender or account.name == sender):
				# Make sure account has enough in it
				if (account.amount < amount):
					print("ERROR; Not enough in '" + sender + "' account to send " + str(amount) + " to " + receiver + "!")
					return 'INSUFFICIENT_FUNDS_ya_broke_aamf'
				else:
					account.amount -= amount
					notFound = False

			# Add outputs to Previous Accounts and New Accounts
			if (account.publicKey == receiver or account.name == receiver):
				account.amount += amount
				outNotFound = False

		if (inNotFound):
			print("Input Accounts not found: {}".format(sender))
			return 'SENDING_ACCOUNT_DNE'

		if (outNotFound):
			print("Output Accounts not found: {}".format(receiver))
			return 'SENDING_ACCOUNT_DNE'

		# Subtract inputs from Previous Accounts
		# if sender in prev_accounts:
		# 	# Make sure account has enough in it
		# 	if (prev_accounts[sender].amount < amount):
		# 		print("ERROR; Not enough in '" + sender + "' account to send " + str(amount) + " to " + receiver + "!")
		# 		return 'INSUFFICIENT_FUNDS_ya_broke_aamf'
		# 	else:
		# 		prev_accounts[sender] -= amount
		# else:
		# 	print("ERROR; No '" + sender + "' account to pull " + str(amount) + " from to transfer to " + receiver + "!")
		# 	return 'ACCOUNT_DONT_EXIST'
		# # Add outputs to Previous Accounts and New Accounts
		# if receiver in prev_accounts:
		# 	prev_accounts[receiver] += amount
		# else:
		# 	prev_accounts[receiver] = amount
		# 	print("Created '" + receiver + "' account to receive " + str(amount) + " from " + sender + "!")

		return False

	# line()
	# Just a visual demarcation for CLI output
	def line(self):
		print(self._linelength*'-' + '>>')

# MAIN
if __name__ == "__main__":
	logan = NutChain()
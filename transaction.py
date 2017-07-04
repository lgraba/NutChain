# transaction.py
# Just the pimpest transaction class, supporting Nutchain
# Logan Graba
# July 02, 2017

import time
import hashlib
import pickle
from collections import namedtuple

Tx = namedtuple("Tx", "input, output, time, version, comment")

class Transaction():
	""" Transaction: A class to parse and represent NutSwings (transactions) """

	version = '.01'

	# Initialize a new Transaction object from whatever string the user shit into the client or a bytes representation
	def __init__(self, line, tx_bytes = None):
		if (tx_bytes):
			# De-serialize into namedTuple and set self.transaction
			self.transaction = pickle.loads(tx_bytes)
			tx_input = self.transaction.input
			(self.sender, self.amount), = tx_input.items()
			tx_output = self.transaction.output
			(self.receiver, crap), = tx_output.items()
			self.time = self.transaction.time
			self.version = self.transaction.version
			# print(tx_output)
		else:
			comment_part = None
			# Split on semicolon, if present
			if ";" in line:
				# Break up line by ; and get comment
				parts = line.split(';')
				tx_part = parts[0]
				comment_part = parts[1].strip()
			else:
				tx_part = line


			words = tx_part.split()
			send_array = ['Give', 'give', 'Send', 'send', 'Shoot', 'shoot', 'Slide', 'slide']
			from_array = ['From', 'from']

			# Construct Transaction
			if (words[0] in send_array):
				self.receiver = words[1]
			if (words[2]):
				self.amount = float(words[2])
			if (words[3] in from_array):
				self.sender = words[4]

			self.time = time.time()

			# Only one transfer per transaction right now, although we could have more complex input/output dicts
			self.transaction = Tx({self.sender:self.amount}, {self.receiver:self.amount}, self.time, self.version, comment_part)

	# Return Printable on special function repr
	def __repr__(self):
		return str(self.transaction)

	# Return string
	def __str__(self):
		return str(self.transaction)

	def crush(self):
		c = hashlib.md5()
		for element in transaction.items():
			c.update(element.encode('utf-8'))
		return c.hexdigest()

	def byte_representation(self):
		tx = self.transaction
		serialized_tx = pickle.dumps(tx)
		return serialized_tx

	def unpickle_bytes(self, tx_bytes):
		return pickle.loads(tx_bytes)
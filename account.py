# account.py
# Just the pimpest account class, supporting Nutchain
# Logan Graba
# July 03, 2017

import os
import sys
import time
import hashlib
import pickle
from collections import namedtuple
from ecdsa import NIST192p, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain

accounts_dir = 'accounts'

class Account():
	"""Account: A class to represent each NutChain Account"""

	# Seed - unique per Account
	seed = os.urandom(NIST192p.baselen) # This is the sexiest seed I could think of (ohhh bb)

	def __init__(self, name, pK_file = False):
		# Filenames
		pK_filename = name + ".pk"
		pubK_filename = name + ".pubk"

		# Create new account
		if (name and not pK_file):
			print("Let's try to make an account...")
			self.name = name
			# Create ECDSA NIST192p KeyPair
			self.privateKey, self.publicKey = self.createKeyPair()
			string_pK = self.privateKey.to_string().hex()
			string_pubK = self.publicKey.to_string().hex()
			print("Name: {}".format(self.name))
			print("privateKey: {}".format(self.privateKey.to_string()))
			print("publicKey: {}".format(self.publicKey.to_string()))

			# Write Keys to [name]_[private/public].pem
			pK_path = os.path.join(accounts_dir, pK_filename)
			pubK_path = os.path.join(accounts_dir, pubK_filename)
			# print(str(pem_pK))
			# print(str(pem_pubK))
			# Write both PEM keys in binary mode (bytes)
			open(pK_path,"w").write(string_pK)
			open(pubK_path,"w").write(string_pubK)

			# Exit for now...
			sys.exit()
		# Loaded Existing from File
		elif (pK_file):
			self.name = name
			temp_privateKey = open(os.path.join(accounts_dir, pK_filename)).read()
			temp_publicKey = open(os.path.join(accounts_dir, pubK_filename)).read()
			self.privateKey = bytes.fromhex(temp_privateKey)
			self.publicKey = bytes.fromhex(temp_publicKey)
			print("Loaded Account: {}; privateKey[{}], publicKey[{}]".format(self.name, self.privateKey, self.publicKey))

	def createKeyPair(self):
		sk = self.generate192Key(self.seed)
		# sk = SigningKey.generate() # NIST192p Default
		vk = sk.get_verifying_key()
		# Uh ok, we'll test it...
		signature = sk.sign("message".encode('utf-8'))
		assert vk.verify(signature, "message".encode('utf-8'))
		return (sk, vk)

	# make_key()
	# Makes a privateKey from a give seed, using NIST192p standard curve
	def generate192Key(self, seed):
		secexp = randrange_from_seed__trytryagain(seed, NIST192p.order)
		return SigningKey.from_secret_exponent(secexp, curve=NIST192p)
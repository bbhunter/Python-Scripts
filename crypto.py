#!/usr/bin/env python3

import os, argparse
from getpass import getpass
# sudo pip3 install pycryptodome     // 3.21.0
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


green = "\033[32m"
blue = "\033[34m"
red = "\033[31m"
bold = "\033[1m"
end = "\033[0m"

print(red+"""
              |
              |
          ----+----          ---------
              |                                   
              |
   )                                           (
   \ \                                       / /
    \ |\                                   / |/
     \|  \           hack1lab            /   /
      \   |\         --------          / |  /
       \  |  \_______________________/   | /
        \ |    |      |      |      |    |/
         \|    |      |      |      |    /
          \____|______|______|______|___/

                 Files Encryption
            fb.me/hack1lab, @hack1lab
"""+end)

def encrypt(key, filename, ig):
	chunksize = 64*1024
	outputFile = filename+".hacklab"
	size = os.path.getsize(filename) #+ 16
	filesize = str(size).zfill(16)
	IV = Random.new().read(16)
	secret = "0000hack1lab0000".encode("utf-8")

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)
			if ig != 'True':
				outfile.write(encryptor.encrypt(secret))

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += b' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64 * 1024
	outputFile = filename.split('.hacklab')[0]


	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				#chunk = str(decryptor.decrypt(chunk))
				chunk = decryptor.decrypt(chunk)
				chunk = chunk.replace("0000hack1lab0000".encode("utf-8"), "".encode("utf-8"))
				outfile.write(chunk)
			outfile.truncate(filesize)


def check(key, filename):
	chunksize = 64# * 1024
	secret = "0000hack1lab0000".encode("utf-8")
	
	with open(filename, 'rb') as infile:
		IV = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, IV)

		chunk = infile.read(chunksize)
		test = decryptor.decrypt(chunk)
		if secret not in test:
			exit(red+bold+"[!] Wrong Password!"+end)




def getkey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-e", "--crypt", help="File Encryption", type=str)
	parser.add_argument("-d", "--dcrypt", help="File Decryption", type=str)
	parser.add_argument("-p", "--password", help="Password To Encrypt/Decrypt a File", type=str)
	parser.add_argument("-x", "--delete", help="Delete The Original File", action='store_true')
	parser.add_argument("-i", "--ignore", help="Ignore The Check For The Password.", action='store_true')
	args = parser.parse_args()

	enc = str(args.crypt)
	dec = str(args.dcrypt)
	password = str(args.password)
	dd = str(args.delete)
	ig = str(args.ignore)

	if enc == "None" and dec == "None":
		parser.print_help()
		exit(1)

	if password == "None":
		password = getpass()

	if enc != "None":
		print(blue+"[+] Encrypt: "+end+"[ "+enc+" ]")
		encrypt(getkey(password), enc, ig)
		print(blue+"[+] Output: "+end+"[ "+enc+".hacklab"+" ]")
		if dd == "True":
			print(red+"[!] Remove: "+end+"[ "+enc+" ]")
			os.remove(enc)
		print(green+bold+"[*] Done!"+end)

	elif dec != "None":
		print(blue+"[+] Decrypt: "+end+"[ "+dec+" ]")
		if ig != 'True':
			check(getkey(password), dec)
		decrypt(getkey(password), dec)
		name = dec.split(".hacklab")[0]
		print(blue+"[+] Output: "+end+"[ "+name+" ]")
		if dd == "True":
			print(red+"[!] Remove: "+end+"[ "+dec+" ]")
			os.remove(dec)
		print(green+bold+"[*] Done!"+end)



if __name__ == '__main__':
	main()

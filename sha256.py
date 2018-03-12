#attempt to implement sha-256
#something is wrong .-. help me!

import binascii

def text_to_bit(text, encoding= 'utf-8', errors= 'surrogatepass'):
	text_encoded = text.encode(encoding, errors)
	text_hex = binascii.hexlify(text_encoded)
	binary = bin(int(text_hex, 16))[2:]
	return binary

message = 'aaa'

binary = text_to_bit(message) + '1'


def padding(binary):
	quotient, reminder = divmod(len(binary), 512)

	if reminder > 448:
		pad_448 = binary + '0' * (960 - reminder)

	if reminder <= 448:
		pad_448 = binary + '0' * (448 - reminder)

	bin_size = bin(len(binary))[2:]

	quotient_size, reminder_size = divmod(len(bin_size), 64)

	if reminder_size > 0:
		size_64 = '0' * (64 - reminder_size) + bin_size
	else:
		size_64 = bin_size

	return pad_448 + size_64


def blocks(pack):
	blocks = []
	for n in range( int(len(pack)/512) ):
		blocks.append([])
		for m in range(16):
			part = pack[(512 * n) + m * 32 : (512 * n) + (m+1) * 32 ]
			blocks[n].append(part)
	return blocks

blocks = blocks(padding(binary))

def ADD(a1, a2, w=32):
	i1 = int(a1,2)
	i2 = int(a2,2)
	quotient, reminder = divmod(i1 + i2, 2 ** w)

	result = bin( reminder)[2:]

	return pad(result, 32)

def AND(a1,a2):
	i1 = int(a1,2)
	i2 = int(a2,2)
	result = bin( i1 & i2)[2:]

	return pad(result, 32)

def XOR(a1,a2):
	i1 = int(a1,2)
	i2 = int(a2,2)
	result = bin( i1 ^ i2)[2:]

	return pad(result, 32)


def bin_rotate_right(a1, n, w= 32):
	i1 = int(a1)
	return bin( (i1 >> n)| (i1 << (w-n)) )[2:]
	#some error here

def rotate_right(string, n):
	return string[-n:] + string[:-n]

def shift_right(string, n):
	return "0" * n + string[:-n]


def CH(a1, a2, a3):
	flipper = '1' * 32
	a1_flip = XOR(a1, flipper)
	a1_compl = ADD(a1_flip, '1')
	result = XOR (AND(a1, a2), AND(a1_compl, a3))

	return pad(result, 32)

def MAJ(a1, a2, a3):
	o1 = AND(a1, a2)
	o2 = AND(a1, a3)
	result =  XOR(XOR(o1,o2),AND(a2,a3))

	return pad(result, 32)

def SIGMA_0(x):
	o1 = rotate_right(x,2) 		 #bin str
	o2 = rotate_right(x,13)		 #bin str
	o3 = rotate_right(x,22)		 #bin str
	result = XOR(XOR(o1, o2), o3)
	return pad(result, 32)

def SIGMA_1(x): #x (str)
	o1 = rotate_right(x,6)		 #bin str
	o2 = rotate_right(x,11)		 #bin str
	o3 = rotate_right(x,25) 		 #bin str
	result = XOR(XOR(o1, o2), o3)
	return pad(result, 32)

def sigma_0(x): #x (str)
	o1 = rotate_right(x,7)		 #bin str
	o2 = rotate_right(x,18)		 #bin str
	o3 = shift_right(x,3)
	result = XOR( XOR(o1, o2), o3)
	return pad(result, 32)

def sigma_1(x): #x (str)
	o1 = rotate_right(x,17)		 #bin str
	o2 = rotate_right(x,19)		 #bin str
	o3 = shift_right(x, 10)
	result = XOR(XOR(o1, o2), o3)
	
	return pad(result, 32)

#guaranteed that each op returns a 32bit word

def pad(result, n):
	quotient, reminder = divmod(len(result), n)

	if reminder == 0:
		return result

	else:
		return '0' * (n - reminder) + result

def k():
	K_hex = [['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',],
			 ['d807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',],
			 ['e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',],
			 ['983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',],
			 ['27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',],
			 ['a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',],
			 ['19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',],
			 ['748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2',] ]
	k_bin = []
	for i in range(len(K_hex)):
		k_bin.append([])
		for n in range(len(K_hex[i])):
			k_int = int(K_hex[i][n], 16)
			k_2	  = bin(k_int)[2:]
			quotient, reminder = divmod(len(k_2), 32)
			if reminder == 0:
				k_32 = k_2
			else:
				k_32 = '0' * (32 - reminder) + k_2
			
			k_bin[i].append(k_32)

	return k_bin

def k_econ(t):
	K_hex = ['428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5', '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
			 'd807aa98', '12835b01', '243185be', '550c7dc3', '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
			 'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc', '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
			 '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7', 'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
			 '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13', '650a7354', '766a0abb', '81c2c92e', '92722c85',
			 'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3', 'd192e819', 'd6990624', 'f40e3585', '106aa070',
			 '19a4c116', '1e376c08', '2748774c', '34b0bcb5', '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
			 '748f82ee', '78a5636f', '84c87814', '8cc70208', '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2' ]
	k_int = int(K_hex[t], 16)
	k_2 = bin(k_int)[2:]
	quotient, reminder = divmod(len(k_2), 32)
	if reminder == 0:
		k_32 = k_2
	else:
		k_32 = '0' * (32 - reminder) + k_2
	return k_32


def H():
	H_hex = [ '6a09e667', 'bb67ae85', '3c6ef372',
			  'a54ff53a', '510e527f', '9b05688c',
			  '1f83d9ab', '5be0cd19' ]
	H_bin = [[]]
	for i in range(len(H_hex)):
		H_int = int(H_hex[i], 16)
		H_2	  = bin(H_int)[2:]
		quotient, reminder = divmod(len(H_2), 32)
		if reminder == 0:
			H_32 = H_2
		else:
			H_32 = '0' * (32 - reminder) + H_2
		
		H_bin[0].append(H_32)

	return H_bin

H= H()

for i in range(len(blocks)):

	for t in range(15, 63):
		o1 = sigma_1(blocks[i][t-2])
		o2 = sigma_0(blocks[i][t-15])
		o3 = ADD(blocks[i][t-7], blocks[i][t-16])
		new_word = ADD (ADD(o1,o2), o3)

		blocks[i].append(new_word)

	a = H[i][0]
	b = H[i][1]
	c = H[i][2]
	d = H[i][3]
	e = H[i][4]
	f = H[i][5]
	g = H[i][6]
	h = H[i][7]

	for t in range(0, 63):
		o1 = ADD(h, SIGMA_1(e))
		o2 = ADD(CH(e,f,g), k_econ(t))
		o3 = ADD(o1, o2)
		T1 = ADD(o3, blocks[i][t])
		T2 = ADD(SIGMA_0(a), MAJ(a,b,c))
		h  = g
		g  = f
		f  = e
		e  = ADD(d, T1)
		d  = c
		c  = b
		b  = a
		a  = ADD(T1, T2)

	H.append([])
	H[i+1].append(ADD(a, H[i][0]))
	H[i+1].append(ADD(b, H[i][1]))
	H[i+1].append(ADD(c, H[i][2]))
	H[i+1].append(ADD(d, H[i][3]))
	H[i+1].append(ADD(e, H[i][4]))
	H[i+1].append(ADD(f, H[i][5]))
	H[i+1].append(ADD(g, H[i][6]))
	H[i+1].append(ADD(h, H[i][7]))

hash_bin = ''

for i in range(len(H[len(H)-1])):
	hash_bin += H[len(H)-1][i]
	print('length of the word H ', i, ' :', len(H[len(H)-1][i]))

hash_hex = hex(int(hash_bin,2))[2:]

hash_hex_2=''

for i in range(len(H[len(H)-1])):
	i_int = int(H[len(H)-1][i], 2)
	i_hex = hex(i_int)[2:]
	i_pad = pad(i_hex, 8)
	hash_hex_2 += i_pad


print("hash length: ", len(hash_bin))
print("hash result: ", hash_bin , ":(")

print("hash made at once length: ", len(hash_hex))
print("hash made at once result: ", hash_hex , ":(")

print("hash made by parts length: ", len(hash_hex_2))
print("hash made by parts result: ", hash_hex_2 , ":(")
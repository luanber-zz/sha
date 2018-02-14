# attempt to implement SHA-1, based on
# the Nist instructions and some material
# you can use this if you want, as "as is".

import binascii

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
	# text_encoded = text.encode(encoding, errors)
	# text_hex = binascii.hexlify(text_encoded)
	# text_int = int(text_hex, 16)
	# bits = bin(text_int)[2:]
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


message = "crypto"
print('original message:', message, '\n')
#1.1 - converting ASCII to binary:
#1.2 - add 1 to the end

binary = text_to_bits(message) + "1"

#print('converted to binary:', binary, '\n')

def add_zeros(binary):
	quotient, reminder = divmod(len(binary), 512)

	if reminder <= 448:
		binary_0 = binary + "0" * (448 - reminder)
	else:
	#	binary_0 = binary + "0" * (448 + ( 512 - reminder) )
		binary_0 = binary + "0" * (960 - reminder)
	return binary_0

binary_0 = add_zeros(binary)

#2 - add message size
#assure that the size is in 64-bit:
# 80 = 000....0  0  0  1  1  0  0  0  0
# 80 = 000....0  0  0  64+16+0  0  0  0

print('length of the binary with zeros:', len(binary_0), '\n')

#now i have the message in binary, added "1" to the end and "0's"
#until it is 448 mod 512....
#now i have to add a 64bit number with the size of the message pre-pad

def add_size(binary_0):
	print('binary length:', bin(len(binary)), '\n')
	size = bin(len(binary))[2:]
	print('size:', size, '\n')
	#print(size <= ('1' + '0' * 63))
	if size > '0' : 
		quotient, reminder = divmod(len(size), 64)
		#print('quotient:', quotient,'\n', 'reminder:', reminder, '\n')
		size_batch = '0' * (64 - reminder) + size
		print('batch size: ', size_batch, '\n')
		print('size_batch length:', len(size_batch), '\n')
		padded = binary_0 + size_batch
		return padded

pad = add_size(binary_0)

print('padded message size:', len(pad), '\n')

#now the message is ( 0 mod 512 ), and is padded correctly....
#tested with a big message: ok!

#3- cutting padded message into 512bit blocks:
#   i have to make the blocks cutted in 32bit words ....

blocks=[]

for n in range(int(len(pad) / 512)) :
	blocks.append([])
	print("block ",n, " size:", len(pad[n * 512 : (n+1) * 512 ]) )
	for m in range(int(512/32)):
		blocks[len(blocks)-1].append(pad[(n * 512) + (m * 32) : (n * 512) + (m+1) *32 ])

# now i have a blocks list, with blocks that contains
# 16 words each, like this:
# blocks = [block1, block2, block3= [word1, ....., word 16] ]
# each word is a "str", with the binary: word2='10010101'


#SHA-1 constants:
#hex
def k_int(t):
	if 0  <= t <= 19:
		return int('5a827999',16)
	elif 20 <= t <= 39:
		return int('6ed9eba1',16)
	elif 40 <= t <= 59:
		return int('8f1bbcdc',16)
	elif 60 <= t <= 79:
		return int('ca62c1d6',16)
	else:
		print('something went wrong with \'k\' definition \n')


#SHA-1 Initial hash values:
#hex
H_0_0 = int('67452301',16)
H_0_1 = int('efcdab89',16)
H_0_2 = int('98badcfe',16)
H_0_3 = int('10325476',16)
H_0_4 = int('c3d2e1f0',16)

H = [[H_0_0, H_0_1, H_0_2, H_0_3, H_0_4]];


#4 - defining left_rotation:
# left_rotation (1010101) = 0101011
#basically just take the most left digit
# and put it in the most right place

def rotate(lista, n):
	return lista[-n:] + lista[:-n] #(str)

# a = 65 (num)
# b = 64 (num)
# bin(a&b)[2:] is what i was expecting .-.
# in the blocks lists, we have words='101011....1010', in string form...

def XOR(l1, l2):
	return bin( l1 ^ l2 )[2:]

def AND(l1, l2):
	return bin( l1 & l2 )[2:]

#now the XOR returns a string with a binary number:
# XOR('1001', '1010') = '1000'

def ft(x,y,z,t):

	x_compl = ~int(x,2)
	
	if 0 <= t <= 19:
		return XOR( AND(x,y), AND(xbin, z) );
	
	if (20 <= t <= 39 or 60 <= t <= 79):
		return XOR( XOR(x,y), z)
	
	if 40 <= t <= 59:
		return XOR( AND(x,y), XOR(AND(x,z), AND(y,z)) )

# now i know how to use xor, let's try
# to iterate:

print('words\' length is: ', len(blocks[0]), '\n')

for i in range(len(blocks)):
	print("starting iteration...\n")
	#initializing variables
	a = H[i][0]
	abin = bin(a)[2:]
	b = H[i][1]
	bbin = bin(b)[2:]
	c = H[i][2]
	d = H[i][3]
	e = H[i][4]

	for t in range(80):

		if t >= 16:
			w_1 = blocks[i][t-3]
			w_2 = blocks[i][t-8]
			w_3 = blocks[i][t-14]
			w_4 = blocks[i][t-16]
			blocks[i].append( rotate ( XOR(XOR(XOR(w_4, w_3), w_2), w_1) , -1 ))
	
	print('words in the block', i, ' :', len(blocks[i]), '\n')


	for t in range(80):
		print('kt in iter ', t, ' : ', k_int(t), '\n')
		ft_bin = ft(b,c,d,t)
		ft_int = int(ft_bin, 2)
		print(len(str(ft_int)))
		aint   = int(rotate(abin, -5), 2)
		Tint   = aint + ft_int + int(e,16) + k_int(t) + int(blocks[i][t],2)
		print('length T: ', len(str(T)))
		e = d
		d = c
		c = int(rotate(bbin, -30),2)
		b = a
		a = T

	H.append([])
	H[i+1].append( a + H[i][0] )
	H[i+1].append( b + H[i][1] )
	H[i+1].append( c + H[i][2] )
	H[i+1].append( d + H[i][3] )
	H[i+1].append( e + H[i][4] )

print(H[len(H)-1])

hash = ''
for i in range( len(H[len(H)-1]) ):
	hexad = hex(int(H[len(H)-1][i], 2) )[2:]
	hash += hexad

print('hash length: ', len(hash))
print("hash result:", hash , ":)")
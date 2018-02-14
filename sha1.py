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


message = "abc"
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
	#print('binary length:', bin(len(binary)), '\n')
	size = bin(len(binary))[2:]
	#print('size:', size, '\n')
	#print(size <= ('1' + '0' * 63))
	if int(size,2) < 2**64 : 
		quotient, reminder = divmod(len(size), 64)
		#print('quotient:', quotient,'\n', 'reminder:', reminder, '\n')
		size_batch = '0' * (64 - reminder) + size
	#	print('batch size: ', size_batch, '\n')
	#	print('size_batch length:', len(size_batch), '\n')
		padded = binary_0 + size_batch
		return padded
	else:
		print("The message is too big .-.")


pad = add_size(binary_0)

print('padded message size:', len(pad), '\n')

#now the message is ( 0 mod 512 ), and is padded correctly....
#tested with a big message: ok!

#3- cutting padded message into 512bit blocks:
#   i have to make the blocks cutted in 32bit words ....

blocks=[]

for n in range(int(len(pad) / 512)) :
	blocks.append([])
	print("block ",n, " size:", len(pad[n * 512 : (n+1) * 512 ]), '\n' )
	for m in range(int(512/32)):
		blocks[len(blocks)-1].append(pad[(n * 512) + (m * 32) : (n * 512) + (m+1) *32 ])

# now i have a blocks list, with blocks that contains
# 16 words each, like this:
# blocks = [block1, block2, block3= [word1, ....., word 16] ]
# each word is a "str", with the binary: word2='10010101'
#print('words\' length is: ', len(blocks[0]), '\n')


#SHA-1 constants:

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

H_0_0 = int('67452301',16)
H_0_1 = int('efcdab89',16)
H_0_2 = int('98badcfe',16)
H_0_3 = int('10325476',16)
H_0_4 = int('c3d2e1f0',16)

H = [[H_0_0, H_0_1, H_0_2, H_0_3, H_0_4]];


#4 - defining rotation:


# left_rotation (1010101) = 0101011
#basically just take the most left digit
# and put it in the most right place

def rotate(lista, n):
	return lista[-n:] + lista[:-n] #(str)

# in the blocks lists, we have words='101011....1010', in string form...

def XOR(l1, l2):
	return int( bin( l1 ^ l2 )[2:], 2)

def AND(l1, l2):
	return int( bin( l1 & l2 )[2:], 2)

# XOR, AND (int, int ) = int

def ft(x,y,z,t):
	
	x_compl = ~x
	if 0 <= t <= 19:
		return XOR( AND(x,y), AND(x_compl, z) );
	
	if (20 <= t <= 39 or 60 <= t <= 79):
		return XOR( XOR(x,y), z)
	
	if 40 <= t <= 59:
		return XOR( AND(x,y), XOR(AND(x,z), AND(y,z)) )

#ft retuns "int"

#modular addition
def ADD(l1, l2, w=32):
	#in SHA-1 w=32 (bits)
	quotient, reminder = divmod(l1+l2, 2**w)
	Z = reminder
	return Z
	#what is this doing?
	#simple: you want to sum numbers lower than 1000
	# but you don't want to get a sum lower to 1000
	#if this sum passes 1000, you want just the reminder
	#so 120+ 430= 650
	# 550+ 930 = 1480-1000 = 480
	#this don't give you the right answer, but
	#mantain a important characterist equal
	# the reminder....

#5- iteration

for i in range(len(blocks)):

	print("starting iteration...\n")

	for t in range(80):

		if t >= 16:
			w_1 = int(blocks[i][t-3] , 2)
			w_2 = int(blocks[i][t-8] , 2)
			w_3 = int(blocks[i][t-14], 2)
			w_4 = int(blocks[i][t-16], 2)
			o1 = XOR(w_4,w_3)
			o2 = XOR(o1, w_2)
			o3 = XOR(o2, w_1)
			blocks[i].append( rotate ( bin(o3)[2:] , -1 ))
	
	print('words in the block', i, ' :', len(blocks[i]), '\n')

	a = H[i][0]  #int
	b = H[i][1]  #int
	c = H[i][2]  #int
	d = H[i][3]  #int
	e = H[i][4]  #int

	abin = bin(a)[2:]	#bin
	bbin = bin(b)[2:]	#bin

	for t in range(80):
		ft_int = ft(b,c,d,t) 		#int
		arot   = int( rotate(abin, -5), 2) 	#int
		Tint   = arot + ft_int + e + k_int(t) + int(blocks[i][t],2)
		quotient, reminder = divmod(Tint, 2**32)
		T = reminder
		e = d
		d = c
		c = int(rotate(bbin, -30),2)
		b = a
		a = T

	H.append([])
	H[i+1].append( ADD(a, H[i][0]) )
	H[i+1].append( ADD(b, H[i][1]) )
	H[i+1].append( ADD(c, H[i][2]) )
	H[i+1].append( ADD(d, H[i][3]) )
	H[i+1].append( ADD(e, H[i][4]) )

print(H[len(H)-1])


hash_bin = ''
hash_hex = ''
for i in range( len(H[len(H)-1]) ):
	word = bin(H[len(H)-1][i])[2:]
	quotient, reminder = divmod(len(str(word)), 32)
	
	if reminder == 0:
		word_32 = str(word)
	else:
		word_32 = "0" * (32-reminder) + str(word)

	hash_bin += word_32
	print("the 32bit word", i, "is:      ", word_32)
	print("the 32bit word", i, "size is: ", len(word_32), '\n')


print("hash length: ", len(hash_bin))
print("hash result: ", hash_bin , ":)")

hash_hex += hex(int(hash_bin,2))[2:]
print("hash length: ", len(hash_hex))
print("hash result: ", hash_hex , ":)")
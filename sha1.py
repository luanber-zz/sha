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


message = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
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

#print('binary with zeros:', '\n', binary_0, '\n')
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

#print('padded message:', '\n', pad, '\n')
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
	#print("block ",n, ":", pad[n * 512 : (n+1) * 512 ] )
#print(type(blocks[1][1]))
#print(len(blocks), '\n')
#print(len(blocks[3][3]), '\n')

# now i have a blocks list, with blocks that contains
# 16 words each, like this:
# blocks = [block1, block2, block3= [word1, ....., word 16] ]
# each word is a "str", with the binary: word2='10010101'


#SHA-1 constants:
#hex
k_0 = '5a827999' # 0  <= t <= 19
k_1 = '6ed9eba1' # 20 <= t <= 39
k_2 = '8f1bbcdc' # 40 <= t <= 59
k_3 = 'ca62c1d6' # 60 <= t <= 79
k = []

#joining into a list

for i in range(3):
	k.append(eval('k_'+str(i)))

print("the k matrix is: ", '\n', k, '\n')

#SHA-1 Initial hash values:
#hex
H_0_0 = '67452301'
H_0_1 = 'efcdab89'
H_0_2 = '98badcfe'
H_0_3 = '10325476'
H_0_4 = 'c3d2e1f0'

H = [[H_0_0, H_0_1, H_0_2, H_0_3, H_0_4]];
print("The hash values matrix is: ", '\n', H, '\n')
#for i in range 4:
#	H[0].append(eval('H_0_', str(i)))
#print(H)


#4 - defining left_rotation:
# left_rotation (1010101) = 0101011
#basically just take the most left digit
# and put it in the most right place

def rotate(lista, n):
	return lista[-n:] + lista[:-n] #(str)

# lr = left rotate
def lr (lista):
	return rotate(lista, -1) #(str)

# a = 65 (num)
# b = 64 (num)
# bin_a = bin(a) = '1b1000001' (str)
# int(bin(a[2:])) = 1000001 (num)
# bin (int(bin_a[2:]) ^ int(bin_b[2:]) ) = '0b1' (str) 
# what a mess!!!! lack of organization

# in the blocks lists, we have words='101011....1010', in string form...
# so to do XOR we have to take them


def XOR(l1, l2):
	return bin( int('0b'+ l1, 2) ^ int('0b'+ l2, 2) )[2:]
#now the XOR returns a string with a binary number:
# XOR('1001', '1010') = '1000'


print(int(blocks[1][1], 2))
print("XOR:", XOR(blocks[1][1], blocks[1][2]))

def ft(x,y,z):
	if 0 <= t <= 19:
		return (XOR(x, y), (int(~x) ^ int(z)) );
	elif (20 <= t <= 39 or 60 <= t <= 79):
		return XOR( XOR(x,y), z)
	elif 40 <= t <= 59:
		return XOR( XOR())
#ft is inconsistent, wrong and incomplete...

# now i know how to use xor, let's try
# to iterate:

print(range(len(blocks)))


for i in range(len(blocks)):
	
	for t in range(79):

		if t >= 15:
			w_1 = blocks[i][t-3]
			w_2 = blocks[i][t-8]
			w_3 = blocks[i][t-14]
			w_4 = blocks[i][t-16]
			blocks[i].append( lr( XOR(XOR(XOR(w_4, w_3), w_2), w_1) ))
			#print("attempt to do:", lr( XOR(XOR(XOR(w_4, w_3), w_2), w_1) ) , "\n\n\n")

	H.append([])
	a = H[i][0]
	b = H[i][1]
	c = H[i][2]
	d = H[i][3]
	e = H[i][4]

	for t in range(79):

		#instead of doing operations in bin directly, I'm
		#transform everything to int, sum and reconvert to
		#binary, what's painfully slow and do many times the same work
		T = bin( int (rotate(a, -5), 2)  + int(e,16) + int(k[t],16) + int(blocks[i][t]) )
		#ft is missing in T eq. 
		e = d
		d = c
		c = rotate(b, -30)
		b = a
		a = T

	H[i+1][0] = a + H[i][0]
	H[i+1][1] = b + H[i][1]
	H[i+1][2] = c + H[i][2]
	H[i+1][3] = d + H[i][3]
	H[i+1][4] = e + H[i][4]

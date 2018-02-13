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
print('padded message size:', len(pad))

#now the message is ( 0 mod 512 ), and is padded correctly....
#tested with a big message: ok!

# cutting padded message into 512bit blocks:

blocks=[]

for n in range(int(len(pad) / 512)) :
	blocks.append(pad[n * 512 : (n+1) * 512 ])
	#print("block ",n, ":", pad[n * 512 : (n+1) * 512 ] )
	print("block ",n, " size:", len(pad[n * 512 : (n+1) * 512 ]) )
#print(blocks)

#SHA-1 constants:
#hex
k_0 = '5a827999' # 0  <= t <= 19
k_1 = '6ed9eba1' # 20 <= t <= 39
k_2 = '8f1bbcdc' # 40 <= t <= 59
k_3 = 'ca62c1d6' # 60 <= t <= 79

#SHA-1 Initial hash values:

H_0_0 = '67452301'
H_0_1 = 'efcdab89'
H_0_2 = '98badcfe'
H_0_3 = '10325476'
H_0_4 = 'c3d2e1f0'


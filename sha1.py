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

print('converted to binary:', binary, '\n')

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

print('binary with zeros:', '\n', binary_0, '\n')
print('length of the binary with zeros:', len(binary_0), '\n')
#now i have the message in binary, added "1" to the end and "0's"
#until it is 448 mod 512....
#now i have to add a 64bit number with the size of the message pre-pad

def add_size(binary_0):
	print('binary length:', bin(len(binary)))
	size = bin(len(binary))[2:]
	print('size:', size, '\n')
	#print(size <= ('1' + '0' * 63))
	if size > '0' : 
		quotient, reminder = divmod(len(size), 64)
		print('quotient:', quotient,'\n', 'reminder:', reminder, '\n')
		size_batch = '0' * (64 - reminder) + size
		print('size_batch length:', len(size_batch), '\n')
		padded = binary_0 + size_batch
		return padded

pad = add_size(binary_0)

print('padded message:', '\n', pad, '\n')
print('padded message size:', len(pad))

#now the message is ( 0 mod 512 ), and is padded correctly....
#tested with a big message: ok!


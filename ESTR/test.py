array = bytearray(0x800)
a = 0x41424344
for i in range(0x800):
	b = a >> 0xc
	a = a ^ b
	b = a
	b = (b << 0x19) & 0xffffffffffffffff
	a = a ^ b
	b = a
	b = b >> 0x1b
	a = a ^ b
	c = a * 0x2545f4914f6cdd1d
	array[i] = c & 0xff

print(array.find(b'z'))
print(array.find(b'h'))
print(array.find(b'3'))
print(array.find(b'r'))
print(array.find(b'0'))
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

text = open("result.txt").read().split("0x4010c2 : cmp rax, 0xffffffffffffffff")
index = []
for t in text:
	index.append(t.count("0x401116"))

for i in index:
	print(chr(array[i-1]),end='')
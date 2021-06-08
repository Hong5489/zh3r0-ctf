text = bytes.fromhex("a4adc0a3fd7fab00e8d5e248dabffd00d140f2c47bbf76008707d5adae82fd00")
flag = [bytearray(8) for i in range(4)]

for part in range(4):
	for j in range(8):
		for index,t in enumerate(text[(part*8):(part*8)+8]):
			t = t >> j
			flag[part][j] |= (t&1) << index

print(b''.join(flag))

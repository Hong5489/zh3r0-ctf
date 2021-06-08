# Eat Sleep Trace Repeat (RE)
## Description

![chal](chal.png)
```
$ ./chall
enter password: zh3r0{xxxxxx...}
search complete
$ # :)
```

## Files
- [trace.txt](public/trace.txt)

Try to run `cat` but there are many lines of assembly and some are repeated, it has 181888 lines

```bash
cat trace.txt 
0x401000 : call 0x401068
0x401068 : mov eax, 0x1
0x40106d : mov rdi, rax
0x401070 : lea rsi, ptr [0x4028d0]
0x401078 : mov edx, 0x10
0x40107d : syscall 
0x40107f : call 0x401005
0x401005 : push rbp
0x401006 : mov rbp, rsp
0x401009 : xor rax, rax
...
...
0x4010c2 : cmp rax, 0xffffffffffffffff
0x4010c6 : jz 0x4010fa
0x4010c8 : mov byte ptr [rsi+0x40286c], al
0x4010ce : inc rsi
0x4010d1 : cmp sil, 0x64
0x4010d5 : jnz 0x4010b6
0x4010d7 : mov eax, 0x1
0x4010dc : mov rdi, rax
0x4010df : lea rsi, ptr [0x4028e1]
0x4010e7 : mov edx, 0x10
0x4010ec : syscall 
0x4010ee : mov eax, 0x3c
0x4010f3 : mov edi, 0x0
0x4010f8 : syscall

wc -l trace.txt 
181888 trace.txt

```
So it decided to run `sort` and `uniq` to sort and filter out the repeated one:
```bash
sort trace.txt | uniq > asm.txt
```
Then we got this clean assembly code:
```asm
0x401000 : call 0x401068
0x401005 : push rbp
0x401006 : mov rbp, rsp
0x401009 : xor rax, rax
0x40100c : xor rdi, rdi
0x40100f : lea rsi, ptr [0x402808]
0x401017 : mov edx, 0x64
0x40101c : syscall 
0x40101e : mov rsp, rbp
0x401021 : pop rbp
0x401022 : ret 
0x401023 : mov rcx, qword ptr [0x402000]
0x40102b : mov rdx, rcx
0x40102e : shr rdx, 0xc
0x401032 : xor rcx, rdx
0x401035 : mov rdx, rcx
0x401038 : shl rdx, 0x19
0x40103c : xor rcx, rdx
0x40103f : mov rdx, rcx
0x401042 : shr rdx, 0x1b
0x401046 : xor rcx, rdx
0x401049 : mov rax, 0x2545f4914f6cdd1d
0x401053 : mul rcx
0x401056 : mov qword ptr [0x402000], rcx
0x40105e : ret 
0x40105f : mov qword ptr [0x402000], rdi
0x401067 : ret 
0x401068 : mov eax, 0x1
0x40106d : mov rdi, rax
0x401070 : lea rsi, ptr [0x4028d0]
0x401078 : mov edx, 0x10
0x40107d : syscall 
0x40107f : call 0x401005
0x401084 : mov edi, 0x41424344
0x401089 : call 0x40105f
0x40108e : mov ecx, 0x800
0x401093 : xor r15, r15
0x401096 : test rcx, rcx
0x401099 : jz 0x4010b1
0x40109b : push rcx
0x40109c : call 0x401023
0x4010a1 : pop rcx
0x4010a2 : mov byte ptr [r15+0x402008], al
0x4010a9 : inc r15
0x4010ac : dec rcx
0x4010af : jmp 0x401096
0x4010b1 : mov esi, 0x0
0x4010b6 : mov dil, byte ptr [rsi+0x402808]
0x4010bd : call 0x401106
0x4010c2 : cmp rax, 0xffffffffffffffff
0x4010c6 : jz 0x4010fa
0x4010c8 : mov byte ptr [rsi+0x40286c], al
0x4010ce : inc rsi
0x4010d1 : cmp sil, 0x64
0x4010d5 : jnz 0x4010b6
0x4010d7 : mov eax, 0x1
0x4010dc : mov rdi, rax
0x4010df : lea rsi, ptr [0x4028e1]
0x4010e7 : mov edx, 0x10
0x4010ec : syscall 
0x4010ee : mov eax, 0x3c
0x4010f3 : mov edi, 0x0
0x4010f8 : syscall 
0x401106 : push rbp
0x401107 : mov rbp, rsp
0x40110a : mov rbx, rdi
0x40110d : xor rdx, rdx
0x401110 : mov al, byte ptr [rdx+0x402008]
0x401116 : inc rdx
0x401119 : cmp rdx, 0x7ff
0x401120 : jz 0x401131
0x401122 : cmp al, bl
0x401124 : jnz 0x401110
0x401126 : dec rdx
0x401129 : mov rax, rdx
0x40112c : mov rsp, rbp
0x40112f : pop rbp
0x401130 : ret 
```
Then I decided to analyse it manually

It look me some hours to analyse this assembly

Here is the summary of this program flow in Python:
```py
print("enter password: ")   # print the string at 0x4028d0
read(0,0x402808,0x64)       # get input from user and store in 0x402808
array = []
a = 0x41424344          # Calculate some weird number and store in array
for i in range(0x800):
	b = a >> 0xc
	a = a ^ b
	b = a
	b = b << 0x19
	a = a ^ b
	b = a
	b = b >> 0x1b
	a = a ^ b
	c = a * 0x2545f4914f6cdd1d
	array.append(c & 0xff)

def find(c):
	for a in array:
		if a == c:
			return array.index(a)
	return False

index = []             # Find the index of input in the array and store 
for c in 0x402808:     # in index (Search each character in our input)
	result = find(c)
	if result:
		index.append(array.index(result))
	else:
		print("search failed")
		return
print("search complete")  # If all character are found search complete
```
After I finish analyse a stuck for awhile, because I don't know how to get the flag just using this code

The flag is in the array but the order seems random:

```py
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

```
Result:
```
261
27
612
9
21
```

## Solving
And then I start to look at the `trace.txt`, and start to think how to get the flag using the trace file

Then I realize **it keep track of the index** when it found the input in the array, so we can solve this by just **counting the specific instruction**!!

When it increase the index is at 0x401116:
```asm
0x401116 : inc rdx
```
After it found the index it will return to 0x4010c2:
```asm
0x4010c2 : cmp rax, 0xffffffffffffffff
```
So I run `grep` command to help me get only these two instruction:
```bash
grep "0x401116\|0x4010c2" trace.txt > result.txt
```
Then I used python to split the instruction 0x4010c2 and count the instruction 0x401116 to get the index:

```py
text = open("result.txt").read().split("0x4010c2 : cmp rax, 0xffffffffffffffff")
index = []
for t in text:
	index.append(t.count("0x401116"))
```
Then just get the flag using the index! *(index minus 1 because it increase before compare)*
```py
flag = ''
for i in index:
	flag += chr(array[i-1])
print(flag)
# zh3r0{d1d_y0u_enjoyed_r3v3rs1ng_w1th0ut_b1n4ry_?}
```
[Full python script](public/solve.py)

Awesome challenge! I think this was my favourite challenge of Zh3r0 CTF

## Flag
```
zh3r0{d1d_y0u_enjoyed_r3v3rs1ng_w1th0ut_b1n4ry_?}
```
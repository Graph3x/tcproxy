from pwn import *

conn = remote("localhost", 9001)

conn.send(b"hello")
a = conn.recvline()
print(a)

conn.send(b"there")
a = conn.recvline()
print(a)

conn.send(b"i like flags: FLAG{probably_not_a_flag}")
a = conn.recvline()
print(a)

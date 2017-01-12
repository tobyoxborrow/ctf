#!/usr/bin/env python


ASCII_START = 32
ASCII_END = 126

for ac in xrange(ASCII_START, ASCII_END + 1):
    # original ascii character
    aco = chr(ac)

    # translated ascii character
    tmp1 = ac
    tmp1 = tmp1 & 0xaa  # 0x804853d:  and    eax,0xaa
    tmp1 = tmp1 >> 1    # 0x8048542:  sar    eax,1

    tmp2 = ac
    tmp2 = tmp2 & 0x55  # 0x804854a:    and    eax,0x55
    tmp2 = tmp2 * 2     # 0x804854d:    add    eax,eax

    act = tmp2 | tmp1   # 0x804854f:    or     eax,edx

    print('%s: %s' % (aco, hex(act)))

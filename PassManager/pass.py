#!/usr/bin/env python
# coding=utf8

from string import digits, lowercase, uppercase
from hashlib import md5
from random import seed, sample
from getpass import getpass
from os import system


Dictionary = digits + lowercase + uppercase + '_/+-'


def myprint(color, mes):
    if color == 'r':
        fore = 31
    elif color == 'g':
        fore = 32
    elif color == 'b':
        fore = 34
    elif color == 'y':
        fore = 33
    else:
        fore = 37
    color = "\x1B[%d;%dm" % (1, fore)
    print "%s%s\x1B[0m" % (color, mes)


def usage():
    print u'这是我自己的密码管理工具\n作为一些地方的密码的管理与生成工具\n'
    print u'跟着程序的提示'
    print u'输入常用的密码或者自己容易记住的密码作为基础密码'
    print u'再输入一个与生成密码有关的信息作为代号'
    print u'随后程序会生成一个由0-9、a-z、A-Z以及其他符号组成的密码\n\n'


def genPass(base_pass, symbol):
    md5_hash = md5(base_pass + symbol).hexdigest()[:16]
    num = int(''.join([x for x in md5_hash if x in digits]))
    seed(num)
    final_pass = ''.join(sample(Dictionary, 32))
    return final_pass


def main():
    usage()
    msg1 = '请输入基础密码：'
    msg2 = '请输入密码代号：'
    msg3 = '不显示密码将密码直接传入剪切板?(y/n)：'

    base_pass = getpass(msg1)
    while not base_pass:
        myprint('r', u'[!] 输入错误！还没有输入基础密码，请重新输入')
        base_pass = getpass(u'请输入基础密码：')

    symbol = getpass(msg2)
    while not symbol:
        myprint('r', u'[!] 输入错误！还没有输入密码代号，请重新输入')
        symbol = getpass(msg2)

    final_pass = genPass(base_pass, symbol)

    display_pass = raw_input(msg3)
    while not display_pass or (display_pass not in ('y', 'Y', 'n', 'N')):
        myprint('r', u'[!]输入错误！请输入(Y/N)或(y/n)')
        display_pass = raw_input(msg3)
    if display_pass in ('y', 'Y'):
        cmd = 'echo "%s" | tr -d "\n" | pbcopy' % final_pass.strip()
        system(cmd)
    elif display_pass in ('n', 'N'):
        myprint('g', u'\n[+] 密码已生成：' + final_pass)


if __name__ == '__main__':
    main()

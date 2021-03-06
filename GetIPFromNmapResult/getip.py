import sys
import re


def splitNmapResult(content):
    ret = []
    buff = ''
    for line in content:
        if 'Nmap scan report for' in line and line not in buff:
            if buff:
                ret.append(buff)
            buff = line
        else:
            buff += line
    return ret


def getIP(content):
    ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content)[0]
    return ip


def findInfo(content, info):
    infolist = content.split('\n')
    if ',' in info:
        info_list = info.split(',')
    else:
        info_list = [info]
    for line in infolist:
        for info in info_list:
            if info.isdigit():
                if line.startswith(info + '/') and 'open' in line:
                    return True
            else:
                if info in line and 'open' in line:
                    return True
    return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:\n\tpython %s filename info' % (sys.argv[0])
        print '\tfilename\tnmap scan result file'
        print '\tinfo\t\tthe info you want to find.(e.g. 22;ssh;telnet;3306)'
        sys.exit(0)

    filename = sys.argv[1]
    info = sys.argv[2]
    iplist = []

    with open(filename, 'r') as f:
        content = f.readlines()

    result_list = splitNmapResult(content)

    for result in result_list:
        if findInfo(result, info):
            iplist.append(getIP(result))

    for ip in iplist:
        print ip

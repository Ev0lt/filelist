import os
import optparse
import re
import binascii
import base64
import shutil
import threading
import sys
import functools
import signal
import copy

stopSignal = True
move = None
M = shutil.move
Dpth=1400
thpool = []
def signal_handler(signal, frame):
    global stopSignal
    print("Catch the Ctrl+C")
    stopSignal=False
    sys.exit("Already exit this program")

def printf(i):
    
    """
    parm i:要输出的字符串
    作用:输出特定编码的字符串
    """
    global move
    try:
        print(i.replace(r'\\', '\\'))
        if move:
            try:
                M(i,move)
            except Exception as e:
                if "into itself" in str(e):
                    pass
    except UnicodeEncodeError:
        i = i.encode('UTF-8', 'ignore').decode('UTF-8')
        print(i.replace(r"\\", '\\'))


class FileSystemError(Exception):
    def __init__(self,msg):
        self.msg=msg
    
    def __str__(self):
        return f"Don't find the {self.msg} path in file system! Please check it!"

def find_file_or_dir(path,dpth=0):
    if dpth > Dpth:
        return  [""]
    try:
        if os.path.isdir(path):
            yield path
            for i in os.listdir(path):
                for j in find_file_or_dir(rf"{path}\{i}",dpth+1):
                    if stopSignal:
                        yield j
        else:
            if stopSignal:
                yield path
    except Exception as e:
        # print(e)
        # print("没有权限访问:"+path+"\\"+i)
        pass


def R(refind,filename,status):
    if refind:
        re_find = re.findall(filename, status)
        if not re_find:
            return False
    else:
        if filename not in status:
            return False
    return True
def find(status,refind, data,filename,Type,DFtype):
    if status != "path":
        status = data
    else:
        status = data.split('\\')[-1]

    if DFtype == True:
        if os.path.isfile(data):
            pass
        else:
            return False
        if not Type or data.split("\\")[-1].lower().split(".")[-1] == Type.lower():
            pass
        else:
            return False
    elif DFtype == False:
        if not os.path.isdir(data):
            return False
    return R(refind,filename,status)

# def find(status, refind, data, filename,Type,DFtype):
#     if status == 'path':
#         return R(refind, data,filename,Type,DFtype)
#     else:
#         data = data.split('\\')[-1]
#         return R(refind, data, filename)

def main():
    global move
    global Dpth
    global thpool
    version = "%prog v3.3"
    usage = "%prog <options> <object>"
    p = optparse.OptionParser(usage=usage, version=version)
    p.add_option("-f", "--file", dest="filename", help="指定查找文件 或者关键词", default="")
    p.add_option('-s', '--status', dest="status", action="store_const", const=['path', 'file'],
                 help="指定查找在文件名或者整体路径中")
    p.add_option('-r', '--refind', dest="refind", action="store_true",
                 help="re寻找开关，开启后可以在filename中添加正则查找的功能")
    p.add_option("-d", "--directory", dest="directory", nargs=1, help="指定查找目录如果没有指定那就是当前目录",
                 default=os.getcwd())
    p.add_option("-n", "--file_num", dest="num", nargs=1, help="指定只要查找几个文件", default=True)

    p.add_option("-m","--move",dest="move",default=None,help="将查找的文件移动到指定目录")
    p.add_option("-R","--Remove",dest="Remove",action="store_true",help="将查找到的文件移除")
    p.add_option("-c",'--copy',help="将查找的文件复制到指定目录",dest="copy")
    p.add_option("-D","--Dpth",help="查找的深度",dest="Dpth",type="int")
    p.add_option("--ftype",help="只输出文件",dest="Ftype",action="store_true")
    p.add_option("--dtype",help="只输出目录",dest="Dtype",action="store_true")
    p.add_option("-t","--type",help="输出文件后缀的类型，使用这个选项会默认开启-ft",dest="Type")
    # p.add_option("-o", "--system", dest="system", nargs=1, help="指定查找的文件系统", action="store_const",
    #              const=["Windows", "Linux"], default=platform.system())
    (option, args) = p.parse_args()
    filename = option.filename
    num = option.num
    status = option.status
    refind = option.refind
    move = option.move
    Remove = option.Remove
    copy = option.copy
    Dpth = option.Dpth if option.Dpth else Dpth
    Type = option.Type
    option.Ftype = True if Type else option.Ftype
    DFtype = True if option.Ftype else (False if option.Dtype else None)
    #True:Ftype False:Dtype None:no used

    # system = option.system
    # if system == "Windows":
    yx_path = r"%s" % option.directory

    if type(num) == type(True):
        s = True
    else:
        s = False

    if move:
        if not Dpth:
            Dpth = 1
        if not os.path.exists(move):
            try:
                os.makedirs(move)
            except:
                raise FileSystemError(move)
    if copy:
        M=shutil.copy
        move = copy
        if not os.path.exists(move):
            os.makedirs(move)

    if Remove:
        move = os.environ['USERPROFILE']+"\\RemoveDir\\"
        if not os.path.exists(move):
            os.makedirs(move)

    n = 0
    for i in find_file_or_dir(yx_path):
        if s or (n < int(num)):
            if find(status=status, refind=refind, data=i, filename=filename,Type=Type,DFtype=DFtype):
                t = threading.Thread(target=printf,args=(i,))
                t.start()
                thpool.append(t)
                n += 1
        else:
            break
    # elif system == "Linux":
    #     pass
    # else:
    #     print("Error System Choose!!!")
    #     sys.exit()


if __name__ == "__main__":
    # system=platform.system()
    signal.signal(signal.SIGINT,signal_handler)
    main()

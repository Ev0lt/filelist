import os
import optparse
import re

def printf(i):
    try:
        print(i)
    except UnicodeEncodeError:
        i=i.encode('UTF-8', 'ignore').decode('UTF-8')
        print(i)


def find_file_or_dir(path):
    for i in os.listdir(path):
        if os.path.isfile(path + "\\" + i):
            yield path + '\\' + i
        else:
            if os.path.isdir(path + '\\' + i):
                for j in find_file_or_dir(path + "\\" + i):
                    yield j
            else:
                yield path + '\\' + i

def find(status,refind,data,filename):
    return True

def main():
    version="%prog v3.0"
    usage="%prog <options> <object>"
    p=optparse.OptionParser(usage=usage,version=version)
    p.add_option("-f","--file",dest="filename",help="指定查找文件 或者关键词")
    p.add_option('-s','--status',dest="status",action="store_const",const=['path','file'],help="指定查找在文件名或者整体路径中")
    p.add_option('-r','--refind',dest="refind",action="store_true",help="re寻找开关，开启后可以在filename中添加正则查找的功能")
    p.add_option("-d","--directory",dest="directory",nargs=1,help="指定查找目录如果没有指定那就是当前目录",default=os.getcwd())
    p.add_option("-n","--file_num",dest="num",nargs=1,help="指定只要查找几个文件",default=True)
    (option,args)=p.parse_args()
    filename=option.filename
    num=option.num
    status=option.status
    refind=option.refind
    yx_path=r"%s"%option.directory

    if type(num) == type(True):
        s=True
    else:
        s=False

    n=0

    for i in find_file_or_dir(yx_path):
        if s or n < num:
            if find(status=status,refind=refind,data=i,filename=filename):
                printf(i)
                n+=1
        else:
            break

if __name__ == "__main__":
    main()

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
    global count
    try:
        if os.path.isdir(path):
            yield path
            for i in os.listdir(path):
                for j in find_file_or_dir(rf"{path}\{i}"):
                    count += 1
                    yield j
        else:
            yield path
            count += 1
    except Exception as e:
        #print("没有权限访问:"+path+"\\"+i)
        pass

def R(refind,filename,data):
    if refind:
        re_find=re.findall(filename,data)
        if re_find == []:
            return False
    else:
        if filename not in data:
            return False
    return True

def find(status,refind,data,filename):
    if status == 'path':
        return R(refind,filename,data)
    else:
        data=data.split('\\')[-1]
        return R(refind,filename,data)

def main():
    version="%prog v3.1"
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
        if s or (n < int(num)):
            if find(status=status,refind=refind,data=i,filename=filename):
                printf(i)
                n+=1
        else:
            break

if __name__ == "__main__":
    count = 1
    main()

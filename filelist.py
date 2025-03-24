import os,optparse,threading
all_file_path=[]

def find_file_or_dir(path):
    global all_file_path
    try:
        for i in os.listdir(path):
            if os.path.isfile(path+"\\"+i):
                all_file_path.append(path+'\\'+i)
            else:
                if os.path.isdir(path+'\\'+i):
                    find_file_or_dir(path+"\\"+i)
                else:
                    all_file_path.append(path+'\\'+i)
    except:
        #print("没有权限访问:"+path+"\\"+i)
        pass


def main():
    global all_file_path
    global error
    global error_str
    threading_list=[]
    version="%prog v1.1"
    usage="%prog <options> <object>"
    p=optparse.OptionParser(usage=usage,version=version)
    p.add_option("-f","--file",dest="filename",help="指定查找文件 或者关键词")
    p.add_option("-d","--directory",dest="directory",help="指定查找目录如果没有指定那就是当前目录",default=os.getcwd())
    p.add_option("-n","--file_num",dest="num",help="指定只要查找几个文件",default="Infinity")
    (option,args)=p.parse_args()
    filename=option.filename
    num=option.num
    yx_path=r"%s"%option.directory
    now_file=os.listdir(yx_path)
    all_file_path=[]
    if num != 'Infinity':
        try:
            num=int(num)
        except:
            exit("The num must number,Please enter the number.")

    for i in now_file:
        try:
            if os.path.isfile(yx_path+'\\'+i):
                all_file_path.append(yx_path+'\\'+i)
            else:
                path=yx_path+"\\"+i
                t=threading.Thread(target=find_file_or_dir,args=(path,))
                t.start()
                threading_list.append(t)
        except Exception as e:
            #print("没有权限访问:"+path+"\\"+i)
            #print(e)
            pass
    for i in threading_list:
        i.join()
    if filename != None:
        all_file_path=list(filter(lambda x:x.find(filename) >=0,all_file_path))
    if num == 'Infinity':
        for i in all_file_path:
            try:
                print(i)
            except UnicodeEncodeError:
                i=i.encode('UTF-8', 'ignore').decode('UTF-8')
                print(i)

    elif len(all_file_path) < num:
        for i in all_file_path:
            try:
                print(i)
            except UnicodeEncodeError:
                i=i.encode('UTF-8', 'ignore').decode('UTF-8')
                print(i)
    else:
        all_file_path=all_file_path[:num]
        for i in all_file_path:
            try:
                print(i)            
            except UnicodeEncodeError:            
                i=i.encode('UTF-8', 'ignore').decode('UTF-8')            
                print(i)         

if __name__ == "__main__":

    t=threading.Thread(target=main)
    t.start()

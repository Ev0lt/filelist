import os,optparse,threading
num="Infinity"
max_file=0
threading_list=[]
def printf(i):
    try:
        print(i)            
    except UnicodeEncodeError:            
        i=i.encode('UTF-8', 'ignore').decode('UTF-8')            
        print(i)  

def max_file_len():
    global num
    global max_file
    if num != "Infinity":
        max_file += 1
        if max_file >= num:
            for i in threading_list:
                i.stop()

def find_file_or_dir(path,filename):
    global num
    global max_file
    if filename != None:
        try:
            for i in os.listdir(path):
                if os.path.isfile(path+"\\"+i):
                    if (path+"\\"+i).find(filename) >=0:
                        printf(path+'\\'+i)
                        max_file_len()
                        
                else:
                    if os.path.isdir(path+'\\'+i):
                        find_file_or_dir(path+"\\"+i,filename)
                    else:
                        if (path+"\\"+i).find(filename) >=0:
                            printf(path+'\\'+i)
                            max_file_len()
        except:
            #print("没有权限访问:"+path+"\\"+i)
            pass
    else:
        try:
            for i in os.listdir(path):
                if os.path.isfile(path+"\\"+i):
                    printf(path+'\\'+i)
                    max_file_len()
                else:
                    if os.path.isdir(path+'\\'+i):
                        find_file_or_dir(path+"\\"+i,filename)
                    else:
                        printf(path+'\\'+i)
                        max_file_len()
        except:
            #print("没有权限访问:"+path+"\\"+i)
            pass

def main():
    global num
    global threading_list
    version="%prog v2.0"
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
                printf(yx_path+"\\"+i)
                max_file_len()
            else:
                path=yx_path+"\\"+i
                t=threading.Thread(target=find_file_or_dir,args=(path,filename,))
                t.start()
                threading_list.append(t)
        except Exception as e:
            #print("没有权限访问:"+path+"\\"+i)
            #print(e)
            pass
    for i in threading_list:
        i.join()         
            
if __name__ == "__main__":

    t=threading.Thread(target=main)
    t.start()

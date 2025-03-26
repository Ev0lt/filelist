# Usage

```
Usage: filelist.py <options> <object>

Options:
  -v, --version         查看版本号
  -h, --help            查看帮助信息
  -f FILENAME, --file=FILENAME
                        指定查找文件 或者关键词
  -s, --status          指定查找在文件名或者整体路径中
  -r, --refind          re寻找开关，开启后可以在filename中添加正则查找的功能
  -d DIRECTORY, --directory=DIRECTORY
                        指定查找目录如果没有指定那就是当前目录
  -n NUM, --file_num=NUM
                        指定只要查找几个文件
  -m MOVE, --move=MOVE  将查找的文件移动到指定目录
  -R, --Remove          将查找到的文件移除
  -c COPY, --copy=COPY  将查找的文件复制到指定目录
  -D DPTH, --Dpth=DPTH  查找的深度
  --ftype               只输出文件
  --dtype               只输出目录
  -t TYPE, --type=TYPE  输出文件后缀的类型，使用这个选项会默认开启-ft
```

# 日志

增加四个功能，只输出文件，只输出目录和更优美的Ctrl+c

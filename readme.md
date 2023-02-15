# SynoAutoDown 

---
## introduction

**SynoAutoDown 是一个我自己写的，调用群晖download station 下载文件的api**

有时候大家会有批量下载文件的需求，群晖的download 虽然通过网页下载很方便，但是不太适合那种脚本自动执行的情况

所以我写了这个脚本来帮助大家调用下载。

里面使用的相关api来自于群晖官网的开发者手册

## usage

**具体使用方法**

在main.py 文件中填入你的用户名和密码（只会在你的本地保留，和我无关）

初始化一个实例对象，比如取名synoauto

```py
snoauto = SnoAuto(account, passwd, path)
```

提示初始化成功后，

然后把需要批量的url链接，放到上面的down_list里面，简单的执行一个for 循环就可以下载了。

## parameter

**相关参数设置**

SynoAuto.py 文件里我设置了两个下载相关的选项

```py
        self.max_down_task = 2
        self.max_error_task = 3
```
分别是同一时刻最多下载任务数量， 最多错误任务数量，一旦多余设置值，或者错误任务过多，任务不会立即添加到 download station，需要等待下载任务减少或者人工删除掉冗余的错误任务。

## TODO

想用PyQt给这个小程序写一个简单的界面

*祝使用愉快*

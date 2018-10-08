import json
import os
import random
total_dict = {}


def compare(a, b):
    keys = list(set(a.keys()).union(set(b.keys())))
    for key in keys:
        #判断该键是否在总记录字典里，如果没有则新建，值为0
        if key not in total_dict.keys():
            total_dict[key] = 0
        if key in list(a.keys()) and key in list(b.keys()):
            if a[key] == b[key]:
                print("%-40s | SAME"%(key))
            else:
                if type(a[key]) is dict:
                    compare(a[key], b[key])
                else:
                    print("%-40s | DIFFERENT    \n     (A :"%(str(key)) + str(a[key]) + ")\n     (B: "+str(b[key])+")")
                    total_dict[key] += 1

        else:
            if key not in a.keys():
                print("%-40s | DIFFERENT    \n     (A NOT EXIST"%(str(key)) + ")\n     (B: " + str(b[key])+")")
            else:
                print("%-40s | DIFFERENT    \n     (A : "%(str(key)) + str(a[key])+")\n     (B NOT EXIST)")
            total_dict[key] += 1



def random_choose(path):
    dl = os.listdir(path)
    which = random.randint(1, len(dl))
    for d in dl:
        which -= 1
        if which == 0:
            #这里有问题。一，无法识别目录，二，如果通过识别目录的方式可能会造成无法随机取样！必须摊平？并不需要全随机
            if os.path.isdir(d):
                random_choose(path+'/'+d)
            return path+'/'+d


def integration(n):
    global total_dict
    for key in total_dict:
        total_dict[key] = n - total_dict[key]
    total_list = sorted(total_dict.items(), key=lambda x: x[1])
    for (key, value) in total_list:
        same_rate = int(value) / n
        print(key + " : %.2f" % same_rate)


#APah 和 BPath为要抽样比较的两个文件夹的路径，N为抽样样本个数
def run(APath, BPath, N):
    global total_dict
    total_dict = {}
    for i in range(1, N+1):
        #去重
        while True:
            APath_T = random_choose(APath)
            BPath_T = random_choose(BPath)
            if APath_T != BPath_T:
                break
        with open(APath_T) as f1:
            json1 = f1.read()
            dict1 = json.loads(json1)
        with open(BPath_T) as f2:
            json2 = f2.read()
            dict2 = json.loads(json2)
        print("\n=============The "+str(i)+" th Pair=============")
        print("A from: "+ APath_T+"\nB from: "+BPath_T+"\n")
        compare(dict1, dict2)

    print('\n=============SIMILARITY=============')
    integration(N)


run('EXAMPLE','EXAMPLE', 3)



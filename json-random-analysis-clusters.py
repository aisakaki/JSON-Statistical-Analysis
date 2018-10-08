import json
import os
import random
#该字典的key为属性值，每有一次value相同 则+1，没有一次value不同 则-1,0为节点
total_dict = {}


#生成目标簇类比较的所有文件路径的列表
#寻找path，从找到的第一个path开始，每找到一个path就加入一个列表中，直到找到第一个不满足条件的行
def generate_path_list(clusters_file, class_no, cluster_no, class_path):
    path_list = []
    with open(clusters_file) as cf:
        for line in cf:
            line = line.split(',')
            if line[0] == 'Id':
                continue
            if int(line[1]) == class_no and int(line[2].strip()) == cluster_no:
                path_list.append(class_path+'/'+line[0])
    return path_list


def compare(a, b):
    keys = list(set(a.keys()).union(set(b.keys())))
    for key in keys:
        #判断该键是否在总记录字典里，如果没有则新建，值为0
        if key not in total_dict.keys():
            total_dict[key] = 0
        if key in list(a.keys()) and key in list(b.keys()):
            if a[key] == b[key]:
                print("%-40s | SAME"%(key))
                total_dict[key] += 1
            else:
                if type(a[key]) is dict:
                    compare(a[key], b[key])
                else:
                    print("%-40s | DIFFERENT    \n     (A :"%(str(key)) + str(a[key]) + ")\n     (B: "+str(b[key])+")")
                    total_dict[key] -= 1

        else:
            if key not in a.keys():
                print("%-40s | DIFFERENT    \n     (A NOT EXIST"%(str(key)) + ")\n     (B: " + str(b[key])+")")
            else:
                print("%-40s | DIFFERENT    \n     (A : "%(str(key)) + str(a[key])+")\n     (B NOT EXIST)")
            total_dict[key] -= 1


def random_choose(path):
    dl = os.listdir(path)
    which = random.randint(1, len(dl))
    for d in dl:
        which -= 1
        if which == 0:
            return path+'/'+d


#在路径列表里随机选择一个返回
def random_choose_cluster(path_list):
    which = random.randint(1, len(path_list))
    for d in path_list:
        which -= 1
        if which == 0:
            return d


def integration(n):
    global total_dict
    total_list = sorted(total_dict.items(), key=lambda x: x[1])
    for (key, value) in total_list:
        same_rate = int(value) / n
        print(key + " : %.2f" % same_rate)


#APah 和 BPath为要抽样比较的两个文件夹的路径，N为抽样样本个数
def run_path(APath, BPath, N):
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


#找到后队列表进行随机，取出随机到的那个APK后到家族目录去查找文件进行一次比较
def run_clusters(clusters_file, class_no1, cluster_no1, class_path1, class_no2, cluster_no2, class_path2,N):
    global total_dict
    total_dict = {}
    l1 = generate_path_list(clusters_file, class_no1, cluster_no1, class_path1)
    l2 = generate_path_list(clusters_file, class_no2, cluster_no2, class_path2)
    for i in range(1, N+1):     #闭合？
        #去重
        while True:
            APath_T = random_choose_cluster(l1)
            BPath_T = random_choose_cluster(l2)
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


#run_path('EXAMPLE', 'EXAMPLE', 3)

#注意这里不需要/ 前面已经处理了
run_clusters('cl.txt', 0, 1, 'EXAMPLE', 1, 2, 'EXAMPLE', 1)


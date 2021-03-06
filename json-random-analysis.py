#黄
import json
import os
import random
import pickle

# 计算每组的不同特征，避免联合特征不完全问题
total_dict = {}
dict_node_list = []
list_node_list = []
connection_dict = {}


def generate_path_list(clusters_file, class_no, cluster_no, class_path):
    path_list = []
    with open(clusters_file) as cf:
        for line in cf:
            line = line.split(',')
            if line[0] == "Id":
                continue
            if int(line[1]) == class_no and int(line[2].strip()) == cluster_no:
                path_list.append(class_path+'/'+line[0])
    return path_list


# 暴力 可优化
def generate_node_list(dic):
    global dict_node_list, list_node_list
    for key in dic:
        if type(dic[key]) is dict:
            if key not in dict_node_list:
                dict_node_list.append(key)
            generate_node_list(dic[key])
        if type(dic[key]) is list:
            if key not in dict_node_list:
                list_node_list.append(key)
            add_list_to_connection_map(dic[key], key)
            for item in dic[key]:
                if type(item) is dict:
                    generate_node_list(item)


def add_list_to_num_dict(a, lis, dic, allFeatureList):
    if lis in a.keys():
        for item in a[lis]:
            if item not in dic and item in allFeatureList:
                if item not in total_dict:
                    total_dict[item] = 0   #错误点
                a[item] = 1
                dic.append(item)
            if item in dic and item in allFeatureList:
                a[item] = 1


def add_list_to_connection_map(lis, key):
    global connection_dict
    for item in lis:
        if item not in connection_dict:
            connection_dict[item] = key


def compare(a, b, allFeatureList):
    keys = list(set(a.keys()).union(set(b.keys())))

    for key in keys:
        # 判断是否在pickle中
        if key not in allFeatureList and key not in dict_node_list and key not in list_node_list:
            continue
        # 判断该键是否在总记录字典里，如果没有则新建，值为0
        if key not in total_dict:
            total_dict[key] = 0
        # 如果key是list，则将a b中的list中的元素全部加入字典和keys里，值为0。这里在遍历中动态改变list
        if key in list_node_list:
            add_list_to_num_dict(a, key, keys, allFeatureList)
            add_list_to_num_dict(b, key, keys, allFeatureList)
            continue
        # 比较核心
        if key in a and key in b:
            if a[key] == b[key]:
                print("%-40s | SAME" % key)
            else:
                if key in dict_node_list:
                    compare(a[key], b[key], allFeatureList)
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
            return path+'/'+d


def integration(n):
    global total_dict
    for key in total_dict:
        total_dict[key] = n - total_dict[key]
    total_list = sorted(total_dict.items(), key=lambda x: x[1])
    for (key, value) in total_list:
        same_rate = int(value) / n
        if key not in dict_node_list and key not in list_node_list:
            if key not in connection_dict:
                print('【'+key + "】 : %.2f" % same_rate)
            else:
                print(connection_dict[key] + '【' + key + "】 : %.2f" % same_rate)


# APah 和 BPath为要抽样比较的两个文件夹的路径，N为抽样样本个数，allFeaturePath为过滤特征文件
# 用于按照家族分析特征
def run_path(APath, BPath, N, allFeaturePath):
    global total_dict, dict_node_list, list_node_list, connection_dict
    total_dict = {}
    dict_node_list = []
    list_node_list = []
    connection_dict = {}
    # pickle处理
    with open(allFeaturePath, 'rb') as f:
        allFeatureList = list(pickle.load(f))
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
            generate_node_list(dict1)
        with open(BPath_T) as f2:
            json2 = f2.read()
            dict2 = json.loads(json2)
            generate_node_list(dict2)
        print("\n=============The "+str(i)+" th Pair=============")
        print("A from: "+ APath_T+"\nB from: "+BPath_T+"\n")
        compare(dict1, dict2, allFeatureList)

    print('\n=============SIMILARITY=============')
    integration(N)




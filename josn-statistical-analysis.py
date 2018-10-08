import json
#该字典的key为属性值，每有一次value相同 则+1，没有一次value不同 则-1
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


with open('EXAMPLE/1') as f1:
    json1 =  f1.read()
    dict1 =  json.loads(json1)

with open('EXAMPLE/2') as f2:
    json2 = f2.read()
    dict2 = json.loads(json2)

print("comparing processing")
compare(dict1, dict2)
compare(dict1, dict2)
print("\n======THE SAME======")
for key in total_dict:
    if total_dict[key] > 0:
        print(key+" ")
print("======DIFFERENT======")
for key in total_dict:
    if total_dict[key] < 0:
        print(key +" ")





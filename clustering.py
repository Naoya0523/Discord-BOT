import numpy as np

def kmeans(clusterNum, data):

    clusterID = np.zeros(len(data)) #クラスタIDの初期化
    center = np.array([data[i] for i in range(0, len(data), int((len(data)-1)/(clusterNum-1)))])
    pcenter = np.zeros((clusterNum, len(data[0])))

    print(f'クラスター数:{clusterNum} 初期中心座標:',end='')
    print(*center)

    while True:
        clusterLen = np.full(len(data), float('inf'))#中心座標との距離の初期化

        for i in range(clusterNum):
            for j in range(len(data)):
                if clusterLen[j] > np.linalg.norm(data[j]-center[i]):
                    clusterLen[j] = np.linalg.norm(data[j]-center[i])
                    clusterID[j] = i


        for i in range(clusterNum):
            tmp = []
            for j in range(len(data)):
                if clusterID[j] == i:
                    tmp.append(data[j])
            if len(tmp)!=0:
                c = np.array(tmp)
                center[i] = c.mean(axis=0)
            else:
                center[i] = np.random.uniform(data.min(),data.max(),len(data[0]))

        if np.array_equal(pcenter, center):
            break

        for i in range(clusterNum):
            if np.isnan(center[i]).any():
                center[i] = np.random.uniform(data.min(),data.max(),len(data[0]))
                print("クラスターID {} の中心座標を更新！".format(i))

        pcenter = center.copy()

    print_cluster(clusterNum, center, clusterID, data)

#クラスターID毎に結果を出力（出力部分）
def print_cluster(clusterNum, center, clusterID, data):
    for i in range(clusterNum):
        cnn = []
        cn = np.empty((0,len(data[0])))
        for j in range(len(data)):
            if clusterID[j] == i:
                cn = np.append(cn, [data[j]], axis=0)
                cos = np.dot(data[j], center[i]) / (np.linalg.norm(data[j])*np.linalg.norm(center[i]))
                cnn.append(cos)
        average = sum(cnn)/len(cnn)
        print("クラスターID:{}\t中心座標{} 密集度:{}".format(i, center[i], average))
    print()
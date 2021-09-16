# -*-coding:utf8-*-
import os
import re
import subprocess

# 读取txt文件内容，每行分开加入到list中


def readTxt(path, ignore):
    contentList = list()
    for line in open(path, "r"):
        line = re.sub(r'\n', '', line)
        if line.find(ignore) == -1:
            contentList.append(line)
    return contentList


def compareAudio(fileNameList, compareFile):
    print('comparing........')
    # 调用AudioCompare库方法比较两个文件
    fileName = compareFile.split('/')[-1]
    filePath = compareFile[:-len(fileName)]
    if not os.path.exists(filePath):
        os.mkdir(filePath)
    if os.path.exists(compareFile):  # 已存在
        fout = open(compareFile, 'a')
    else:
        fout = open(compareFile, 'w')
        fout.write('# 记录音频比较结果的文件\n')
    contentList = readTxt(compareFile, '#')
    for index, fileName in enumerate(fileNameList):
        for compareFileName in fileNameList[index + 1:]:
            # 从记录的文件中取值，如果已经比较过就不再比较
            needCompareFlag = True
            for content in contentList:
                if fileName in content.split('|') and compareFileName in content.split('|'):
                    needCompareFlag = False
                    print('已存在：' + fileName + '|' + compareFileName)
            if needCompareFlag:
                command = ' AudioCompare-master/main.py -f ' + \
                    fileName + ' -f ' + compareFileName
                p = subprocess.Popen('python' + command,
                                     stdout=subprocess.PIPE, shell=True)
                stdoutput = p.stdout.readlines()
                fout.write(stdoutput[0])


# 获取文件大小
def getFileSize(fileName):
    try:
        return os.path.getsize(fileName)
    except Exception as err:
        print(err)

# 得到文件大小相似的集合，返回[[('xx.wav',3715364L)],[('xx.wav',3715364L),('xx.wav',3715364L),('xx.wav',3715364L)]]


def sortedNearFile(fileNamesList, level):
    # 得到每个文件的大小
    fileSizeDict = dict()

    for fileName in fileNamesList:
        fileSizeDict.setdefault(fileName, getFileSize(fileName))
    # 先按照文件的大小排序
    sortedFileSizeList = sorted(
        fileSizeDict.items(), key=lambda item: item[1])

    print(f'sortedFileSizeList {sortedFileSizeList}')

    # 逐个比较相邻的文件大小，小于阈值，提取出来
    nearFileList = list()
    for index in range(0, len(sortedFileSizeList)):
        if index + 1 < len(sortedFileSizeList) and index > 0:
            # 和左边的比
            preVal = abs(sortedFileSizeList[index]
                         [1] - sortedFileSizeList[index - 1][1])
            # 和右边比
            nextVal = abs(
                sortedFileSizeList[index][1] - sortedFileSizeList[index + 1][1])
            # 得出与左边或右边音频大小小于阀值的音频
            if preVal <= level or nextVal <= level:
                nearFileList.append(sortedFileSizeList[index])
    # 把重复的放在一个列表中，返回[[('xx.wav',3715364L)],[('xx.wav',3715364L),('xx.wav',3715364L),('xx.wav',3715364L)]]
    sortedNearFileList = list()
    i = 0
    for index in range(0, len(nearFileList)):
        # 如果nearFileList[index] - sortedNearFileList[i][0] <= level 就添加，否则添加到sortedNearFileList[i+1]中
        if len(sortedNearFileList) == 0:
            sortedNearFileList.append([nearFileList[index]])
        else:
            # 右边减左边，小于阀值的保存
            val = abs(sortedNearFileList[i][0][1] - nearFileList[index][1])
            if val <= level:
                sortedNearFileList[i].append(nearFileList[index])
            else:
                i += 1
                sortedNearFileList.append([nearFileList[index]])
    return sortedNearFileList

# 找出指定文件夹下的所有后缀名为suffix的文件名称，返回列表


def getFileNames(dirPath, suffix):
    fileNamesList = list()
    for fileName in os.listdir(dirPath):
        if os.path.splitext(fileName)[1] == suffix:
            fileNamesList.append(dirPath + '/' + fileName)
    return fileNamesList


if __name__ == '__main__':
    fileNameList = getFileNames(os.path.curdir, '.mp3')

    sortedFileList = sortedNearFile(fileNameList, 13 * 1024)
    print('sortedFileList')
    print(sortedFileList)

    for fileTupleList in fileNameList:
        if len(fileTupleList) > 1:
            compareList = list()
            for fileTuple in fileTupleList:
                compareList.append(fileTuple[0])
            compareAudio(compareList[:], './compare.txt')

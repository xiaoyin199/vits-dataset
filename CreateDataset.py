from AudioSlicer import AudioSlicer
from WhisperTranscriber import WhisperTranscriber
import os
import sys
import logging

'''
创建数据集
'''


class CreateDataset:
    # 音频类型
    AUDIO_TYPE = ['mp3', 'wav', 'ogg', 'flv', 'aac', 'm4a', 'wma',
                  'ape', 'flac', 'alac', 'aiff', 'pcm', 'amr', 'm4r']

    def __init__(self, inputFile, outputDir='./output', format='wav', frameRate=0):
        self.inputFile = inputFile
        self.outputDir = outputDir
        self.format = format
        self.frameRate = frameRate
        # 创建输出目录
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)
        self.create()

    def create(self):
        logFile = self.outputDir+'/train_filelist.txt'
        logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[
                            logging.FileHandler(logFile, 'a', 'utf-8')])
        list = self.handleDataSource()
        for i, l in enumerate(list):
            slicer = AudioSlicer(l['file'])
            baseName, ext = os.path.splitext(os.path.basename(l['file']))
            for j, item in enumerate(l['data']):
                filename = self.outputDir + '/'+baseName + '_' +\
                    str(i) + '_' + str(j) + '.' + self.format
                slicer.slice(self.vttTimeToMs(item['start']), self.vttTimeToMs(
                    item['end']), outputFile=filename, format=self.format, frameRate=self.frameRate)
                # 写入日志
                log = filename + '|' + item['text']
                logging.info(log)

    # vtt时间转毫秒

    def vttTimeToMs(self, vttTime):
        hms = vttTime.split(':')
        return int(hms[0]) * 60 * 60 * 1000 + int(hms[1]) * 60 * 1000 + int(float(hms[2]) * 1000)

    # 处理数据源
    def handleDataSource(self):

        whisperModel = WhisperTranscriber()
        list = []
        # 单个文件处理同时兼容目录处理
        if os.path.isfile(self.inputFile):
            data = whisperModel.getSimpleResults(self.inputFile)
            list.append({'file': self.inputFile, 'data': data})
        else:
            fileList = self.getAudioFlieList()
            for file in fileList:
                data = whisperModel.getSimpleResults(file)
                list.append({'file': file, 'data': data})
        return list

    # 获取音频文件列表
    def getAudioFlieList(self):
        list = []
        if os.path.isdir(self.inputFile):
            # 遍历目录下所有文件
            for filename in os.listdir(self.inputFile):
                file = os.path.join(self.inputFile, filename)
                # 如果是文件，判断是否是音频类型
                if os.path.isfile(file) and file.split('.')[-1] in self.AUDIO_TYPE:
                    list.append(file)
        return list


if __name__ == '__main__':

    args = sys.argv
    print(len(args))
    if len(args) > 1:
        # 定义需要裁剪的音频文件路径
        inputFile = args[1]
        if len(args) > 4:
            outputDir = args[2]
            format = args[3]
            frameRate = int(args[4])
            CreateDataset(inputFile, outputDir, format, frameRate)
        elif len(args) > 3:
            outputDir = args[2]
            format = args[3]
            CreateDataset(inputFile, outputDir, format)
        elif len(args) > 2:
            outputDir = args[2]
            CreateDataset(inputFile, outputDir)
        else:
            CreateDataset(inputFile)
    print('done')

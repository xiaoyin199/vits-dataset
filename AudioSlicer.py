from pydub import AudioSegment
import sys
import os

'''
音频裁剪类
'''


class AudioSlicer:
    def __init__(self, inputFile, outputFile='./output/out.wav', format='wav'):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.format = format
        self.audio = AudioSegment.from_file(self.inputFile)

    # 音频切片
    def slice(self, startTime, endTime, outputFile='', format='', frameRate=0):
        # 裁剪音频
        if startTime >= 0 and endTime > 0:
            outputAudio = self.audio[startTime:endTime]
        if outputFile != '':
            self.outputFile = outputFile
        # 创建输出文件夹
        outDir = os.path.dirname(self.outputFile)
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        # 输出格式
        if format != '':
            self.format = format
        if frameRate > 0:
            outputAudio = outputAudio.set_frame_rate(frameRate)
        # 导出裁剪后的音频文件
        outputAudio.export(self.outputFile, format=self.format)
        return self.outputFile


if __name__ == '__main__':

    # 最多5个参数 1:文件路径 2:开始时间 3:结束时间 4:输出文件路径 5:输出格式
    args = sys.argv
    print(len(args))
    if len(args) > 1:
        # 定义需要裁剪的音频文件路径
        inputFile = args[1]
        audio = AudioSlicer(inputFile)
        if len(args) > 4:
            if len(args) > 5:
                audio.slice(int(args[2]), int(args[3]), args[4], args[5])
            else:
                audio.slice(int(args[2]), int(args[3]), args[4])
        else:
            audio.slice(int(args[2]), int(args[3]))
        print(args)

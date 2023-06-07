import stable_whisper as whisper
import os
import sys
import zhconv

'''
# 语音转文字，根据停顿切分句子
'''


class WhisperTranscriber:

    def __init__(self, model_name="large-v2"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path, language='Chinese'):
        result = self.model.transcribe(audio_path, language=language)
        return result.segments_to_dicts()

    # 获取简单的结果
    def getSimpleResults(self, audio_path, language='Chinese'):
        res = []

        data = self.transcribe(audio_path, language=language)
        for item in data:
            if item['text'] != "字幕由 Amara.org 社群提供" and item['text'] != "字幕由Amara.org社群提供":
                text = zhconv.convert(item['text'], 'zh-cn')
                res.append({'start': self.sec2vtt(item['start']), 'end': self.sec2vtt(
                    item['end']), 'text': text})
        return res

    def sec2hhmmss(self, seconds: (float, int)):
        mm, ss = divmod(seconds, 60)
        hh, mm = divmod(mm, 60)
        return hh, mm, ss

    def sec2vtt(self, seconds: (float, int)) -> str:
        hh, mm, ss = self.sec2hhmmss(seconds)
        return f'{hh:0>2.0f}:{mm:0>2.0f}:{ss:0>6.3f}'

    def sec2srt(self, seconds: (float, int)) -> str:
        return self.sec2vtt(seconds).replace(".", ",")


if __name__ == '__main__':

    args = sys.argv
    print(len(args))
    if len(args) > 1:
        model = WhisperTranscriber()
        data = model.getSimpleResults(args[1])
        print(data)

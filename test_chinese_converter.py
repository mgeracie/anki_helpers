from opencc import OpenCC

cc = OpenCC('t2s')
text = 'hello 傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。'

print(cc.convert(text))
#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
# from lxml import etree
import time
import re
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon

name = ''


# warnings.filterwarnings('ignore')
# print('等会记住验证码')
# print(title)
def make_dir():
    if os.path.exists('.//党课复习'):
        os.chdir(".//党课复习")
    else:
        os.makedirs(".//党课复习")
        os.chdir(".//党课复习")

    if os.path.exists('单项选择题.txt'):
        pass
    else:
        with open('单项选择题.txt', 'w') as f:
            pass

    if os.path.exists('多项选择题.txt'):
        pass
    else:
        with open('多项选择题.txt', 'w') as f:
            pass

    if os.path.exists('判断题.txt'):
        pass
    else:
        with open('判断题.txt', 'w') as f:
            pass

    if os.path.exists('填空题.txt'):
        pass
    else:
        with open('填空题.txt', 'w') as f:
            pass


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

session = requests.Session()


def get_src():
    t = time.time()
    t = int(round(t * 1000))  # 获取毫秒级时间戳
    scr_url = 'https://dxpx.uestc.edu.cn/user/captcha?v=' + str(t)
    # 获取验证码
    img = session.get(url=scr_url, headers=headers).content
    with open('./验证码.png', mode='wb') as f:
        f.write(img)


def get_xsrf():
    # 获取xsrf
    url = 'https://dxpx.uestc.edu.cn/user/login'
    html = session.get(url=url, headers=headers)
    xsrf = re.findall('<input type="hidden" name="_xsrf" value="(.*?)"/>', html.text)[0]
    return xsrf






class Stats:

    def __init__(self):
        self.ui = loadUi('dl.ui')
        self.ui.setWindowIcon(QIcon('b8888.ico'))
        make_dir()
        self.ui.resize(374, 285)
        self.ui.move(800, 300)
        self.ui.pushButton.clicked.connect(self.handleCalc)
        self.ui.pushButton_2.clicked.connect(self.help)
        get_src()
        pix = QPixmap('./验证码.png')
        self.ui.label_2.setPixmap(pix)

    def help(self):
        QMessageBox.information(
            self.ui,
            '解答',
            '爬取的是你做过的题，并清除重复题\nQQ联系我2310173245')

    def handleCalc(self):
        xuehao = self.ui.lineEdit.text()
        mima = self.ui.lineEdit_2.text()
        yzm = self.ui.lineEdit_3.text()
        data = {
            'user_sid': xuehao,
            'user_pass': mima,
            'next': '/',
            'v_code': yzm,
            '_xsrf': get_xsrf()
        }
        url = 'https://dxpx.uestc.edu.cn/user/login'
        html = session.post(url=url, headers=headers, data=data)
        #print(html.raise_for_status)
        # 获取每套题库链接地址
        url = 'https://dxpx.uestc.edu.cn/fzdx/exam_center/end_record'
        # 进入试卷界面
        html = session.get(url=url, headers=headers)
        try:

            test_ur = re.findall('<a href="(.*?)">查看试卷</a></td>', html.text)
            test_url = []

            for i in test_ur:
                test_url.append('https://dxpx.uestc.edu.cn' + i)
            number = len(test_ur)
            num = 0
            '''for i in range(len(test_url)):
                html = session.get(url=test_url[i],headers=headers)
                word = html.content.decode()
                with open('%d.txt'%num,'w',encoding='utf-8') as f:
                    f.write(word)
                num +=1
            '''
            for i in range(len(test_url)):
                # print(i + 1, '张试卷')
                txt = session.get(url=test_url[i], headers=headers).content.decode('utf-8')
                # print(txt)
                global name
                name = \
                    re.findall(r'<a href="/user/home" class="person"><i[\s\S]*?class="iconfont">&#xe619;</i>(.*?)</a>',
                               txt)[0]

                title = re.findall(r'<h3>(.*?)\n([\s\S]*?)</h3>', txt)
                for i in range(len(title)):
                    title[i] = list(title[i])
                    title[i][1] = title[i][1].replace(' ', '')
                    title[i][1] = title[i][1].replace('&nbsp;&nbsp;', '')
                    title[i][1] = title[i][1].replace('\n', '')
                    title[i][0] = '\n' + title[i][0]
                    # title[i][1] += '\n'
                # print(title)题目
                # print(len(title))

                answer1 = re.findall(r'<input type="radio" name="radio3"/>\n([\s\S]*?)\n.*?</label>', txt)
                # print(answer1)
                for i in range(len(answer1)):
                    answer1[i] = answer1[i].replace(' ', '')
                    answer1[i] = answer1[i].replace('\n', '')
                    # answer1[i] += '\n'
                # print(answer1,len(answer1))#单选和判断的所有答案

                answer2 = re.findall(r'<input type="checkbox" name="checkbox"/>\n([\s\S]*?)\n.*?</label>', txt)
                # print(answer2)
                for i in range(len(answer2)):
                    answer2[i] = answer2[i].replace(' ', '')
                    answer2[i] = answer2[i].replace('\n', '')
                    # answer2[i] += '\n'
                # print(answer2,len(answer2))#多选的所有答案

                key = re.findall(r'<span class="sub_color">(.*?)</span>', txt)
                # print(answer2)
                for i in range(len(key)):
                    key[i] = key[i].replace(' ', '')
                    key[i] = key[i].replace('\n', '')
                    key[i] += '\n'
                    key[i] = '@@@' + key[i]
                # print(key,len(key))#所有的正确答案,一共100个

                index = -1
                # 全部的给出答案
                '''for i in answer1[:120]:
                    if 'A' in i:
                        index += 1
                    title[index].append(i)

                index = 59
                for i in answer1[120:]:
                    if 'A' in i:
                        index += 1
                    title[index].append(i)

                index = 29
                for i in answer2:
                    if 'A' in i:
                        index += 1
                    title[index].append(i)'''

                for i in range(len(key[:100])):
                    title[i].append(key[i])

                '''for i in range(len(blank)):
                    title[80 + i].append(blank[i])'''

                # print(title)

                with open('单项选择题.txt', 'r', encoding='utf-8') as f:
                    xzt = f.read()
                index1 = 0
                with open('单项选择题.txt', 'a+', encoding='utf-8') as f:
                    for i in title[:30]:
                        if i[1] not in xzt:
                            f.writelines(i[1:])
                            index1 += 1

                # print('单选更新', index1, '道题')
                self.ui.textBrowser.append('单选更新' + str(index1) + '道题')
                self.ui.textBrowser.ensureCursorVisible()
                with open('多项选择题.txt', 'r', encoding='utf-8') as f:
                    dxt = f.read()
                index2 = 0
                with open('多项选择题.txt', 'a+', encoding='utf-8') as f:
                    for i in title[30:60]:
                        if i[1] not in dxt:
                            f.writelines(i[1:])
                            index2 += 1

                self.ui.textBrowser.append('多选更新' + str(index2) + '道题')
                self.ui.textBrowser.ensureCursorVisible()
                with open('判断题.txt', 'r', encoding='utf-8') as f:
                    pdt = f.read()
                index3 = 0
                with open('判断题.txt', 'a+', encoding='utf-8') as f:
                    for i in title[60:80]:
                        if i[1] not in pdt:
                            f.writelines(i[1:])
                            index3 += 1

                self.ui.textBrowser.append('判断更新' + str(index3) + '道题')
                self.ui.textBrowser.ensureCursorVisible()
                with open('填空题.txt', 'r', encoding='utf-8') as f:
                    tkt = f.read()
                index4 = 0
                with open('填空题.txt', 'a+', encoding='utf-8') as f:
                    for i in title[80:100]:
                        if i[1] not in tkt:
                            f.writelines(i[1:])
                            index4 += 1

                    self.ui.textBrowser.append('填空更新' + str(index4) + '道题')
                    self.ui.textBrowser.ensureCursorVisible()

            QMessageBox.information(
                self.ui,
                '%s你好' % name,
                '爬取完毕共获取%d套\n已保存在同级路径' % number)

        except Exception as e:
            # 访问异常的错误编号和详细信息
            self.ui.textBrowser.append('错误')
            self.ui.textBrowser.ensureCursorVisible()
            print(e)


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()

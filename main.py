# 程序仅用于学习参考
# Made by SCHAUDING

import io
import os
import csv
import time
import subprocess
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

print("#"*30+'\n本程序仅用于爬取“www.aqistudy.cn”成都地区的空气质量数据\n输入两个两年即可爬取两年之间每一天的空气质量数据\n'+"#"*30)
start_yaer = int(input('请输入需要爬取的第一个年份：'))
end_year = int(input('请输入最后一个需要爬取的年份：'))

# 打开一个新的命令提示符窗口
subprocess.Popen('cmd', shell=True)
# 在新的命令提示符窗口执行命令打开谷歌浏览器
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222', shell=True)

# 用selenium连接到打开的谷歌浏览器窗口
options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
#driver = webdriver.Chrome(executable_path=r"E:\Program Files\Driver_Chrome\chromedriver.exe", options=options) # executable_path已弃用
Google_driver_path = Service(executable_path=r'E:\Program Files\Driver_Chrome\chromedriver.exe')
driver = webdriver.Chrome(service=Google_driver_path,options=options)

print('\n程序启动成功，3秒后开始爬取数据......')
time.sleep(3)

while start_yaer <= end_year:
    # 一、循环爬取1月到12月的天气数据
    for i in range(1,13):
        if i < 10:
            date = "0" + str(i)
        else:
            date = str(i)

        # 遍历12个月的网站
        driver.get(f'https://www.aqistudy.cn/historydata/daydata.php?city=%E6%88%90%E9%83%BD&month={start_yaer}{date}')

        # 判断是否存在文件夹如果不存在则创建为文件夹
        folder_path = f'E:\Backups\Python\爬虫\original_data\{start_yaer}年'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 保存初始数据
        file = open(f'E:\Backups\Python\爬虫\original_data\{start_yaer}年\\{start_yaer}年{date}月.txt',"w",encoding='utf-8')

        # 爬取数据 设置每页等待时间为3s
        # 与time.sleep()不同，该等待只会在网页元素未加载出时触发，而time.sleep()无论如何都会进行等待
        driver.implicitly_wait(3)
        list = driver.find_elements(By.CSS_SELECTOR,".row tr")
        for tr in list:
            s_data = str(tr.text)
            if s_data != "":
                file.write(f"{s_data}" + "\n")
                print(s_data)
    # 保存文件
    file.close()

    print(f'\n爬取结束，爬取的原始数据保存在"original_data/{start_yaer}"文件夹里。')
    print(f'正在处理原始数据，处理后的数据保存在"optimize_data/{start_yaer}"文件里。')
    time.sleep(1)

    # 二、修正数据格式
    for i in range(1,13):
        if i < 10:
            date = "0" + str(i)
        else:
            date = str(i)

        # 读取初始文件
        with open(f'E:\Backups\Python\爬虫\original_data\{start_yaer}年\\{start_yaer}年{date}月.txt','r',encoding='utf-8') as f:
            lines = f.readlines()

        # 判断是否存在文件夹如果不存在则创建为文件夹
        folder_path = f'E:\Backups\Python\爬虫\optimize_data\{start_yaer}年'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 生成修正后的文件
        filename = open(f'E:\Backups\Python\爬虫\optimize_data\{start_yaer}年\\{start_yaer}年{date}月.txt','w',encoding='utf-8')
        filename.write(lines[0])

        # 向修正后的文件中写入数据
        line_tests = ''
        a = -2
        b = -1
        c = 0
        while c != len(lines)-1:
            a += 3
            b += 3
            c += 3
            line_test = str(lines[a].strip()) + str(' '+lines[b].strip()+' ') + str(lines[c].strip())
            filename.write(line_test+"\n")
            line_tests = ''
        # 保存文件
        filename.close()

    print('\n处理完成，开始将文本转换为excel表格。')
    print(f'处理后的表格保存在"csv_data/{start_yaer}"文件夹中。')

    # 三、txt文本转csv
    for i in range(1,13):
        if i < 10:
            date = "0" + str(i)
        else:
            date = str(i)

        # 读取修正后的文件
        with open(f'E:\Backups\Python\爬虫\optimize_data\{start_yaer}年\\{start_yaer}年{date}月.txt', 'r',encoding='utf-8') as f:
            text = f.read()

        # 将txt数据转换成dataframe
        df = pd.read_csv(io.StringIO(text), sep=' ', engine='python')

        # 判断是否存在文件夹如果不存在则创建为文件夹
        folder_path = f'E:\Backups\Python\爬虫\csv_data\{start_yaer}年'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # 将dataframe写入到csv文件中
        df.to_csv(f'E:\Backups\Python\爬虫\csv_data\{start_yaer}年\\{start_yaer}年{date}月.csv', index=False,encoding='utf-8-sig')

    # csv文件数据合并
    print('\n开始对文档进行汇总。')
    data_list = []
    for i in range(1,13):
        if i < 10:
            date = "0" + str(i)
        else:
            date = str(i)

        # 读取修正后的文件
        with open(f'E:\Backups\Python\爬虫\optimize_data\{start_yaer}年\\{start_yaer}年{date}月.txt', 'r', encoding = 'utf-8') as f:
            lines_list = f.readlines()
        
        if date != '01':
            for line in lines_list[1:]:
                data = line.strip().split(" ")
                data_list.append(data)
        else:
            for line in lines_list:
                data = line.strip().split(" ")
                data_list.append(data)

    # 创建CSV文件对象并写入数据
    with open(f'E:\Backups\Python\爬虫\csv_data\{start_yaer}年\\all_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data_list:
            writer.writerow(row)

    print(f'\n{start_yaer}年爬取完成，数据存放在“csv_data/{start_yaer}”中。')
    start_yaer += 1

# 执行完毕，退出程序
print('数据已经爬取完成，即将退出程序。')
exit()
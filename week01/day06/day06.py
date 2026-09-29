#爬取网页演示
import requests
from lxml import html
import csv

target_url = "https://www.tiobe.com/tiobe-index"

response=requests.get(target_url, timeout=30)
response.raise_for_status()

document=html.fromstring(response.text)

with open('./tiobe.csv', 'w',encoding='utf-8', newline='') as csvfile:

    #获取表头
    th_list = [th.text_content().strip() for th in
               document.xpath('//table[@id="top20"]/thead/tr/th')]

    # 表头有两个 Change，按列写入，避免字典的同名键覆盖数据。
    writer = csv.writer(csvfile)
    writer.writerow(th_list)

    #获取表格内容
    tr_list=document.xpath('//table[@id="top20"]/tbody/tr')
    for tr in tr_list:
        # 语言表头横跨图标和名称两列，导出时排除 td-top20 图标列。
        # 其他空单元格仍需保留，确保列对齐。
        td_list = [td.text_content().strip() for td in tr.xpath(
            './td[not(contains(concat(" ", normalize-space(@class), " "), " td-top20 "))]'
        )]
        writer.writerow(td_list)


# print(th_list)



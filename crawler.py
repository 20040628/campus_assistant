from bs4 import BeautifulSoup
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# 得到所有校史故事的超链接
def getAllLinks():
    url = 'https://xsyj.hust.edu.cn/xsyj/xsgs/1.htm'
    # 发送HTTP请求获取网页内容
    response = requests.get(url, headers=headers)
    # 中文乱码问题
    response.encoding = 'utf-8'
    # 确保请求成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(response.text, 'lxml')

        # 查找<title>标签
        title_tag = soup.find_all('li')

        # 打印标题文本
        if title_tag:
            print(title_tag)
        else:
            print("未找到标签")
    else:
        print("请求失败，状态码：", response.status_code)

def getAllText(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # 文件名
        h1_tag = soup.find('h1')
        if h1_tag:

            raw_title = h1_tag.get_text(strip=True)
            # 分隔符可能是英文|或中文｜，取后半部分作为文件名
            title_prefix = re.split(r'[|]', raw_title)[1]
            # 清除非法字符
            safe_title = re.sub(r'[\\/:*?"<>|]', '', title_prefix)
            filename = safe_title + '.txt'
        else:
            filename = 'output.txt'

        # 获取所有 font-size: 15px 的 span 文本
        spans = soup.find_all('span')
        text_list = []

        for span in spans:
            style = span.get('style', '')
            if 'font-size: 15px' in style:
                text = span.get_text(strip=True)
                if text:
                    text_list.append(text)

        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            for line in text_list:
                f.write(line + '\n')

        print(f"✅ 已保存内容到文件：{filename}")
    else:
        print("请求失败，状态码：", response.status_code)
data = [
"https://mp.weixin.qq.com/s?__biz=MzUzNjMzMTQxOA==&amp;mid=2247489188&amp;idx=1&amp;sn=0a7c0eca68a55d4df37cad8d6fab27aa&amp;chksm=faf68351cd810a47d5de0d947b0f1994d629b611f2641cb31aa304de72f5de7aa9e97d5d5938&amp;mpshare=1&amp;scene=23&amp;srcid=1114MIfe3Sw92diciAFbRcJa&amp;sharer_shareinf",
"https://mp.weixin.qq.com/s?__biz=MzUzNjMzMTQxOA==&amp;mid=2247489150&amp;idx=1&amp;sn=3d69fe381cfacd4b9d0cf0d559f497cf&amp;chksm=faf6838bcd810a9da15df86fd10376853513c256f0468ad76109eb4a53dca434328f3e47488a&amp;mpshare=1&amp;scene=23&amp;srcid=1010pJfvNLOW3tFCPGwYepte&amp;sharer_shareinf",
"https://mp.weixin.qq.com/s/f33MltqvSCD-cLOCh-dIfQ",
"https://mp.weixin.qq.com/s/qpyF8qoZibi0l0TXY3pR0w",
"https://mp.weixin.qq.com/s/ea0kKAa4Sf53xvrhK8pb8A",
"https://mp.weixin.qq.com/s/h6UbUfflCoRp9Cb3Z8YPHA",
"https://mp.weixin.qq.com/s/kGN-QdxvgkuwtCrJHPQbhA",
"https://mp.weixin.qq.com/s/tGKeEwSejU9Du0jritOt7w",
"https://mp.weixin.qq.com/s/-pt9bS0N3NOeejAiZrFx_w",
"https://mp.weixin.qq.com/s/TKDLfAf9JAMYGq8MWD8UWQ",
"https://mp.weixin.qq.com/s/a5AIagey6QtcEzfM4JvoXA",
"https://mp.weixin.qq.com/s/lPcOIZy_W6IAEIWQw5tBeg",
"https://mp.weixin.qq.com/s/KpZdixHCIv0kkLijXMbQNg",
"https://mp.weixin.qq.com/s/uqWWI5KYIOUcYcEuhMOVAg",
"https://mp.weixin.qq.com/s/si6eke7SoggrZEcLAoIVOw"
]

data1 = [
"https://mp.weixin.qq.com/s/n522oIR7v9JzaFriGJ94ug",
"https://mp.weixin.qq.com/s/9xizJC9HMkxUj_uoO0dkGw",
"https://mp.weixin.qq.com/s/zmJo1UxUyR0dMFUN1-_XVQ",
"https://mp.weixin.qq.com/s/2cSrKJnd1tNgmw5wWTYhAA",
"https://mp.weixin.qq.com/s/k6I__JHqNR_qzgoetjombQ",
"https://mp.weixin.qq.com/s/OMgicn04nnRLsBC0ZDWKrw",
"https://mp.weixin.qq.com/s/ujWQTNtqu6wt__WbJxTweA",
"https://mp.weixin.qq.com/s/zoKAb6LmIi1IkL1nkkD4GA",
"https://mp.weixin.qq.com/s/ZKO4qjWeYcFRI56S_cdWpw",
"https://mp.weixin.qq.com/s/AQHmb7hHbzNcxOf6MylQIQ",
"https://mp.weixin.qq.com/s/4ifhTfqIS1ZHqpB1K-DpZg"

]
for url in data1:
    getAllText(url)

import requests
import re
from fontTools.ttLib import TTFont
from lxml import etree

class Sxs():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        }

    def get_html(self):
        # 第1步：获取html，且存为html文件以便后面研究使用
        url = 'https://www.shixiseng.com/interns?keyword=%E4%BA%A7%E5%93%81&city=%E5%85%A8%E5%9B%BD&type=intern&from=menu'
        ret = requests.get(url=url, headers=self.headers).text
        with open('index.html', 'w', encoding='utf8') as f:
            f.write(ret)
        return ret

    def get_font(self, ret):
        # 第2步：下载html配套的ttf文件
        font_url = re.findall('src: url\((.*?)\);', ret)
        f_url = 'https://www.shixiseng.com' + font_url[0] if font_url else font_url
        font_data = requests.get(f_url)
        with open('file.woff', 'wb') as f:
            f.write(font_data.content)

    def get_font_data(self, ttf):
        font_dict = {}
        # font = TTFont("file.woff")
        font = TTFont(ttf)
        cmap = font.get("cmap").getBestCmap()
        for k, v in cmap.items():
            if v[3:]:
                content = "\\u00" + v[3:] if len(v[3:]) == 2 else "\\u" + v[3:]
                real_content = content.encode('utf-8').decode('unicode_escape')
                k_hex = hex(k)
                # 网页返回的字体是以&#x开头  ，换成以这个开头，下面代码就是直接替换
                real_k = k_hex.replace("0x", "&#x")
                font_dict[real_k] = real_content
        return font_dict

    def put_html(self, ttf_dict):
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
            for k, v in ttf_dict.items():
                html = html.replace(k, v)
            return html

    def get_data(self, html):
        html = etree.HTML(html)
        li_list = html.xpath("//div[@class='intern-wrap interns-point intern-item']")
        for li in li_list:
            title = "".join(li.xpath(".//div[@class='f-l intern-detail__job']//a/text()")[0].split())
            price = "".join(
                li.xpath(".//div[@class='f-l intern-detail__job']//span[@class='day font']/text()")[0].split())
            name = li.xpath('.//a[@class="title ellipsis"]/text()')[0]
            print(title, price, name)

    def main(self):
        # 第1步：获取html，且存为html文件以便后面研究使用
        ret = self.get_html()
        # 第2步：下载html配套的ttf文件
        self.get_font(ret)
        # 第3步：提取ttf中摄影的数据
        font_dict = self.get_font_data('file.woff')
        # 第4步：对下载（HTML内容）进行替换
        html = self.put_html(font_dict)
        # 第5步：使用xpath提取想要的数据
        data = self.get_data(html)
        print(data)


if __name__ == '__main__':
    Sxs().main()
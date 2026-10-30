# import requests
from bs4 import BeautifulSoup
import os
import pathlib
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re
import time
from urllib.parse import urlparse


All_Image_Num = 0
Need_Image_num = 20
# 下载函数
def Download_Images(img):
    global All_Image_Num

    for i in range(len(img)):
        if All_Image_Num >= Need_Image_num:
            return
        time.sleep(1)
        imga=img[i].find('a').get('href')
        # imga=img[i].find_parent('a').get('href')

        page.goto(
            imga,
            wait_until="domcontentloaded",
            timeout=30000
        )
        # for size in ["S", "M"]:
        #     download = page.locator(f"a.-download{size}")
        #     print(f"\n{size} 下载按钮:")
        #     print(download.evaluate("(el) => el.outerHTML"))
        download=page.locator("a.photoDownload__button.-downloadL")
        try:
            download.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            if download.count()==0:
                print("没有下载按钮")
                continue


        # print(download.inner_html())
        with page.expect_download() as download_info:
            download.click()

        print("-------------------")
        print("下载地址：",download.get_attribute('href'))
        picture=download_info.value
        filename=picture.suggested_filename

        save_path=pathlib.Path(os.path.abspath("."))/"image"
        save_path.mkdir(parents=True,exist_ok=True)
        save_path=save_path / filename

        picture.save_as(save_path)
        print("下载图片成功：",filename)
        print("图片位置：",save_path)
        print("-------------------")
        All_Image_Num=All_Image_Num+1

# 检索当前页面中可下载的图片
def Search_Images(soup,page_Num):
    img = soup.find_all(class_="photoEntries")
    print(f"当前第{page_Num}页,检索到{len(img)}个图片")

    if len(img) == 0:
        print("页面没有图片，程序已经返回")
        return
    print("开始下载")
    Download_Images(img)

#开始爬取
def Begin_Download():
    page_Num = 1
    while (True):
        Now_Page_list = page.locator('li.-current')
        if Now_Page_list.count()==0:
            print("搜索没有结果，爬虫已结束")
            return
        if int(Now_Page_list.inner_text().strip())< page_Num:
            return

        Back_url = page.url
        soup = BeautifulSoup(page.content(), 'lxml')
        Search_Images(soup,page_Num)
        page.goto(
            Back_url,
            wait_until="domcontentloaded",
            timeout=30000
        )
        page_Num = page_Num + 1
        Next_Page_list = page.locator("a.pageNav__link").filter(
            has_text=re.compile(rf"^\s*{page_Num}\s*$")
        )

        if Next_Page_list.count() == 0 or All_Image_Num >= Need_Image_num:
            print(f"已下载{max(0, All_Image_Num)}张图片")
            break
        else:
            Next_Page_list.click()


if __name__ == "__main__":
    url = "https://www.pakutaso.com/"
    print("=====================================")
    print("该爬虫可以爬取某日本图片网站素材：https://www.pakutaso.com/")
    print("使用说明：")
    print("1.你可以通过关键词爬取，也可以输入以预览的界面网址爬取")
    print("例如：“https://www.pakutaso.com/ai/aisozai.html” 或者“AI”")

    print("\n2.网站为日本网站，所以建议先到网站上找到想爬的界面或日语关键词，然后输入关键词")

    print("\n3.爬虫会启动一个edge浏览器，请不要关闭这个浏览器")
    print("=====================================")
    keyword = input("请输入搜索关键词:")
    result = urlparse(keyword)
    num = input("下载图片数量(回车默认20张): ").strip()
    Need_Image_num = int(num) if num else 20

    print("正在加载网站，请等待后续提示.(如果等太久或者失败，可能是需要VPN)")


    with sync_playwright() as p:
        brower=p.chromium.launch(
            headless=False,
            channel='msedge'
        )
        context=brower.new_context(
            accept_downloads=True
        )
        page=context.new_page()
        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=30000
        )
        soup=BeautifulSoup(page.content(),'lxml')



        Search=page.locator('#headerSearch')
        if result.scheme in ("http", "https") and result.netloc:
            page.goto(
                keyword,
                wait_until="domcontentloaded",
                timeout=30000
            )
            Begin_Download()
        else:
            Search.fill(keyword)
            Search.press("Enter")
            page.wait_for_url(
                "**/search.html?*",
                wait_until="domcontentloaded",
                timeout=30000
            )
            print("正在跳转至：",page.url)
            Begin_Download()


    input("程序运行结束，按回车退出...")
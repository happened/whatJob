


from selenium import webdriver
import time

def BrowerGetHTML(url):
    brower = webdriver.Chrome("D:\python\whatJob\driver\chromedriver.exe")
    brower.get(url)
    time.sleep(1)
    brower.refresh()
    time.sleep(1)
    html=brower.page_source
    brower.close()
    return html
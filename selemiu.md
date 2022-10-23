# pachong
from selenium import webdriver
import time
# 创建driver对象
driver = webdriver.Chrome()
# 访问的起始的url地址
start_url = 'https://www.baidu.com'
# 访问
driver.get(url=start_url)
time.sleep(1)
driver.find_element_by_id('kw').send_keys('python')
time.sleep(1)
driver.find_element_by_id('su').click()
time.sleep(1)

# 通过执行js来新开一个标签页
js = 'window.open("https://www.csdn.net");'
driver.execute_script(js)
time.sleep(1)

# 1.获取所有浏览器窗口
windows = driver.window_handles

# 2.根据窗口索引进行切换
driver.switch_to.window(windows[0])
time.sleep(1)
driver.switch_to.window(windows[1])

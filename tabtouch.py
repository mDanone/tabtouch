import sys
import re
import os

from selenium import webdriver

from selenium.webdriver.common.proxy import Proxy, ProxyType


from tabtouchmethods import RunScript

print(f"{os.getcwd()}+\\browser`s drivers\\chromedriver.exe")
name = None
code = None
try:
    if "--name" in sys.argv:
        if (re.findall(r"[a-zA-Z]+", sys.argv[sys.argv.index("--name") + 1])):
            name = sys.argv[sys.argv.index("--name") + 1]
except:
    print("Введите название заезда")
    sys.exit(0)

try:
    if "--code" in sys.argv:
        if (re.findall(r"[A-Z][0-9]{1,2}", sys.argv[sys.argv.index("--code") + 1])):
            code = sys.argv[sys.argv.index("--code") + 1]
except:
    print("Введите код заезда")
    sys.exit(0)

if "-p" in sys.argv:
    try:
        if (re.findall(r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\:?([0-9]{1,5})?", sys.argv[sys.argv.index("-p") + 1])):
            ip = sys.argv[sys.argv.index("-p") + 1]
    except:
        print("Вы не написали верный proxy адрес")

    if "firefox" in sys.argv:
        options = webdriver.FirefoxOptions()
        # If you need proxy set it here else delete lines from 5 to 12
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        if ip:
            proxy.http_proxy = ip
            proxy.ssl_proxy = ip
            print(proxy.ssl_proxy)
        print(ip)
        # setting up proxy settings ()
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        proxy.add_to_capabilities(capabilities)
        # Put the path of your browser`s driver
        PATH = f"{os.getcwd()}\\browser`s drivers\\geckodriver.exe"

        # Delete desired capabilities argument if you don`t need proxy
        driver = webdriver.Firefox(
            firefox_options=options, executable_path=PATH,
            desired_capabilities=capabilities
        )
    elif "chrome" in sys.argv:
        
        options = webdriver.ChromeOptions()
        # If you need proxy set it here else delete lines from 5 to 12
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        if ip:
            proxy.http_proxy = ip
            proxy.ssl_proxy = ip
            print(proxy.ssl_proxy)
        print(ip)
        # setting up proxy settings ()
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)
        # Put the path of your browser`s driver
        PATH = f"{os.getcwd()}\\browser`s drivers\\chromedriver.exe"

        # Delete desired capabilities argument if you don`t need proxy
        driver = webdriver.Chrome(
            options=options, executable_path=PATH,
            desired_capabilities=capabilities
        )
else:
    if "firefox" in sys.argv:
        PATH = f"{os.getcwd()}\\browser`s drivers\\geckodriver.exe"

        # Delete desired capabilities argument if you don`t need proxy
        driver = webdriver.Firefox(executable_path=PATH)
    elif "chrome" in sys.argv:
        PATH = f"{os.getcwd()}\\browser`s drivers\\chromedriver.exe"

        # Delete desired capabilities argument if you don`t need proxy
        driver = webdriver.Chrome(executable_path=PATH)


RunScript(driver, name, code)

#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import func
from htmlmin import minify
import datetime
import re
import sys
import time
import traceback
import fasttext
import jieba
import requests
from send_email import get_xlex, send_emails
from config import *
import openpyxl

from tools import get_screenshot, cutting_content, get_snapshot, uploadFile, readPDF, setProxy, \
    get_proxy, find, clearmb4, base64_to_image
from models import QualityScraper, Quality, QualityFile, QualityList, SpiderPros, SpiderArticleTag, SpiderEmail
from MCMT.predict_article_title import load_all_ft_model, load_all_cnn_model, predict_one_from_mysql
from setting import *

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class QualitySpider(object):
    def __init__(self):
        self.logger = logger_info()  #记录一些日志信息
        self.model = fasttext.train_supervised('/data/spider/qualityspider/qualitycut.txt')
        # self.model = fasttext.train_supervised('qualitycut.txt')
        self.numre = re.compile(r'\d+')

        self.mongodb_production = linkMongo(host=DATABASES['mongodb']['HOST'], prot=DATABASES['mongodb']['PORT'],
                                            user=DATABASES['mongodb']['USER'], pwd=DATABASES['mongodb']['PASSWORD'],
                                            col=DATABASES['mongodb']['COL'],
                                            collection=DATABASES['mongodb']['COLLECTION'])
        self.engine_production = linkMysql(user=DATABASES['mysql']['USER'], pwd=DATABASES['mysql']['PASSWORD'],
                                           host=DATABASES['mysql']['HOST'],prot=DATABASES['mysql']['PORT'],
                                           table=DATABASES['mysql']['TABLE'])
        self.mongodb_test = linkMongo(host=DATABASES_TEST['mongodb']['HOST'], prot=DATABASES_TEST['mongodb']['PORT'],
                                      user=DATABASES_TEST['mongodb']['USER'], pwd=DATABASES_TEST['mongodb']['PASSWORD'],
                                      col=DATABASES_TEST['mongodb']['COL'],
                                      collection=DATABASES_TEST['mongodb']['COLLECTION'])
        self.engine_test = linkMysql(user=DATABASES_TEST['mysql']['USER'], pwd=DATABASES_TEST['mysql']['PASSWORD'],
                                     host=DATABASES_TEST['mysql']['HOST'], prot=DATABASES_TEST['mysql']['PORT'],
                                     table=DATABASES_TEST['mysql']['TABLE'])
        self.session_production = scoped_session(sessionmaker(bind=self.engine_production))   #
        self.session_test = scoped_session(sessionmaker(bind=self.engine_test))

        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "Connection": "close",
        }
        # 公告信息统计字段
        self.quality_amount = 0
        self.succeed = 0
        self.fail = 0
        self.newdata = 0
        self.updata = 0
        self.list_count = 0
        self.list_fail = 0
        self.list_new = 0
        # 召回信息统计字段
        self.zhaohui_list_count = 0
        self.zhaohui_list_new = 0
        self.zhaohui_list_fail = 0
        self.zhaohui_quality_amount = 0
        self.zhaohui_succeed = 0
        self.zhaohui_fail = 0
        self.zhaohui_newdata = 0
        self.zhaohui_updata = 0
        # 比较试验统计字段
        self.bjsy_list_count = 0
        self.bjsy_list_new = 0
        self.bjsy_list_fail = 0
        self.bjsy_quality_amount = 0
        self.bjsy_succeed = 0
        self.bjsy_fail = 0
        self.bjsy_newdata = 0
        self.bjsy_updata = 0

        # 日志保存路径
        # self.path = '/data/spider/qualityspider/log/'
        self.path = ''
        self.driver = None

    def upadate_email_data(self):
        data = self.session_test.query(SpiderEmail).filter().first()

        # 公告信息统计字段
        self.quality_amount = data.quality_amount
        self.succeed = data.quality_succeed
        self.fail = data.quality_fail
        self.newdata = data.quality_newdata
        self.updata = data.quality_updata
        self.list_count = data.list_count
        self.list_fail = data.list_fail
        self.list_new = data.list_new
        # 召回信息统计字段
        self.zhaohui_list_count = data.zhaohui_list_count
        self.zhaohui_list_new = data.zhaohui_list_new
        self.zhaohui_list_fail = data.zhaohui_list_fail
        self.zhaohui_quality_amount = data.zhaohui_quality_amount
        self.zhaohui_succeed = data.zhaohui_succeed
        self.zhaohui_fail = data.zhaohui_fail
        self.zhaohui_newdata = data.zhaohui_newdata
        self.zhaohui_updata = data.zhaohui_updata
        # 比较试验统计字段
        self.bjsy_list_count = data.bjsy_list_count
        self.bjsy_list_new = data.bjsy_list_new
        self.bjsy_list_fail = data.bjsy_list_fail
        self.bjsy_quality_amount = data.bjsy_quality_amount
        self.bjsy_succeed = data.bjsy_succeed
        self.bjsy_fail = data.bjsy_fail
        self.bjsy_newdata = data.bjsy_newdata
        self.bjsy_updata = data.bjsy_updata

    def commit_email_data(self):
        data = self.session_test.query(SpiderEmail).filter().first()

        data.quality_amount = self.quality_amount
        data.quality_succeed = self.succeed
        data.quality_fail = self.fail
        data.quality_newdata = self.newdata
        data.quality_updata = self.updata
        data.list_count = self.list_count
        data.list_fail = self.list_fail
        data.list_new = self.list_new
        # 召回信息统计字段
        data.zhaohui_list_count = self.zhaohui_list_count
        data.zhaohui_list_new = self.zhaohui_list_new
        data.zhaohui_list_fail = self.zhaohui_list_fail
        data.zhaohui_quality_amount = self.zhaohui_quality_amount
        data.zhaohui_succeed = self.zhaohui_succeed
        data.zhaohui_fail = self.zhaohui_fail
        data.zhaohui_newdata = self.zhaohui_newdata
        data.zhaohui_updata = self.zhaohui_updata
        # 比较试验统计字段
        data.bjsy_list_count = self.bjsy_list_count
        data.bjsy_list_new = self.bjsy_list_new
        data.bjsy_list_fail = self.bjsy_list_fail
        data.bjsy_quality_amount = self.bjsy_quality_amount
        data.bjsy_succeed = self.bjsy_succeed
        data.bjsy_fail = self.bjsy_fail
        data.bjsy_newdata = self.bjsy_newdata
        data.bjsy_updata = self.bjsy_updata

        self.session_test.commit()

    def create_take_log(self):
        # 错误日志表头
        field_order = ["time", 'url', 'status_code', 'spider_channel', 'exception']
        # 表名
        todytime = time.strftime("%Y-%m-%d")
        csvname = '{}_公告、召回和比较试验信息的抓取结果汇总.xlsx'.format(todytime)
        self.csvfilepath = self.path + csvname

        # 创建表格
        get_xlex(self.csvfilepath, field_order)
        self.wb = openpyxl.load_workbook(self.csvfilepath)
        self.sheet1 = self.wb['sheet1']

    def hasaddr(self, addr):
        return self.session_production.query(QualityList).filter_by(url=addr).all()

    def nextpage(self, driver, scraper, index):
        proxy = get_proxy()
        if scraper.site_administrator_id == '1261189142004609103':

            driver = setProxy(driver, proxy)
        if scraper.indexPage:
            if scraper.ID == 1367371348984475648:
                index = int(index) * 15
            driver.get(scraper.indexPage.replace("{0}", "{}").format(index))
            return True

        elif scraper.site_administrator_id == '1438317455104815104':
            list_page = find(driver, 'x//*[@class="page"]/a')
            if len(list_page) == 1:
                self.logger.info("只有一页")

            else:
                _p = 0
                for list in list_page:
                    _p = _p + 1
                    time.sleep(2)
                    next_page = driver.find_element_by_xpath(f"//*[contains(@id,'page_a{_p}')]")
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(2)
                return True
                
        elif scraper.byPages:
            nums = set()
            for byPage in scraper.byPages.split("|"):
                try:
                    for i in find(driver, byPage):
                        text = i.text
                        for n in self.numre.findall(text):
                            nums.add(int(n))
                except Exception as err:
                    self.logger.error(err)
                    exstr = traceback.format_exc()
                    self.logger.error(exstr)
            if len(nums) > 1:
                try:
                    next = find(driver, scraper.byNext)
                    next[0].click()
                    time.sleep(2)
                    return True
                except:
                    return False
            else:
                self.logger.info("Number Only One")
                return False
        else:
            lastpage = driver.current_url
            next = find(driver, scraper.byNext)
            if len(next) == 0:
                self.logger.info("No Next Elem")
                print("No Next Elem")
                return False
            elem = next[0]
            try:
                driver.execute_script("arguments[0].scrollIntoView();", elem)
            except Exception as err:
                self.logger.error(err)
                pass
            href = elem.get_attribute("href")
            if scraper.disableClass:
                if scraper.disableClass == '!' and not elem.is_displayed():
                    self.logger.info("Next Elem Not Displayed")
                    return False
                elif scraper.disableClass in elem.get_attribute("class"):
                    self.logger.info("Next Elem Not Enabled")
                    return False
            if href and not href.endswith("#") and "javascript" not in href:
                for i in range(3):
                    try:
                        driver.get(href)
                        break
                    except Exception as err:
                        self.logger.error(err)
            else:
                try:
                    elem.click()
                    return True
                except:
                    if elem.get_attribute is not None:
                        driver.execute_script(elem.get_attribute("onclick"))
                    else:
                        self.logger.log("No OnClick")
                        return False

        time.sleep(0.5)
        # 翻页判断
        # if scraper.disableClass :
        if scraper.disableClass or driver.current_url != lastpage:
            return True
        self.logger.info("Same Url")
        print("Same Url")
        # return False

    def runpage(self,scraper, item, proxy=None):  #self.runpage(scraper, item, self.proxy)
        if proxy:
            self.proxies = {
                'http': 'http://' + str(proxy['IP']) + ":" + str(proxy["Port"]),
                'https': 'https://' + str(proxy['IP']) + ":" + str(proxy["Port"])
            }
            driver = getWebdriver(proxy=proxy)
            # driver = setProxy(driver, proxy)
        else:
            # 浏览器驱动
            driver = getWebdriver()
        self.driver = driver
        driver.set_page_load_timeout(90)
        driver.set_script_timeout(90)

        # try:
        #     driver.get(scraper.site_url)
        #     cookies = driver.get_cookies()
        #     for cookie in cookies:
        #         driver.add_cookie(cookie)
        #         time.sleep(0.5)
        # except:
        #     pass

        page = item.url
        self.headers['referer'] = page
        self.logger.info(page)
        q_id = get_id()
        defeated = item.defeated
        if not defeated:
            defeated = 0

        list_test = self.session_test.query(QualityList).filter_by(id=item.id).first()
        try:
            defeated_test = list_test.defeated
            if not defeated_test:
                defeated_test = 0
        except Exception as err:
            print(err)

        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        session = requests.Session()
        try:
            if page.endswith("pdf") or page.endswith("xlsx") or page.endswith("xls") or page.endswith(
                "docx") or page.endswith("doc") or page.endswith("zip") or page.endswith("rar"):
                existing_production_list = self.session_production.query(Quality).filter_by(source_url=page).all()
                existing_test_list = self.session_test.query(Quality).filter_by(source_url=page).all()
                # 检查
                if not existing_production_list:
                    f_id = get_id()
                    data = requests.get(page, headers=self.headers)

                    file_name = page.split(".")[-1]
                    filename = item.title + '.' + file_name

                    article_list_production = self.session_production.query(QualityList).filter_by(
                        id=item.id).first()
                    article_list_production.snapshot_id = q_id

                    article_list_test = self.session_test.query(QualityList).filter_by(id=item.id).first()
                    article_list_test.snapshot_id = q_id

                    q_production = Quality(ID=q_id,
                                           notification_title=item.title,
                                           content='',
                                           source_url=page,
                                           spider_channel_id=scraper.ID,
                                           create_time=datetime.datetime.now(),
                                           create_by=0,
                                           notification_date=item.date,
                                           snap_url='=',
                                           collect_time=datetime.datetime.now())

                    q_test = Quality(ID=q_id,
                                     notification_title=item.title,
                                     content='',
                                     source_url=page,
                                     spider_channel_id=scraper.ID,
                                     create_time=datetime.datetime.now(),
                                     create_by=0,
                                     notification_date=item.date,
                                     snap_url='',
                                     collect_time=datetime.datetime.now())

                    fs = []
                    fs2 = []
                    # 附件保存至mongodb
                    # 保存至生产环境mongodb
                    imageId_production = uploadFile(filename, data.content, f_id,self.mongodb_production,
                                                    DATABASES['mongodb']['gridFS'])

                    # 保存至测试环境mongodb
                    imageId_test = uploadFile(filename, data.content, f_id,self.mongodb_test,
                                                    DATABASES_TEST['mongodb']['gridFS'])

                    print(imageId_production, imageId_test)
                    print("ok", filename)

                    f_production = QualityFile(ID=f_id,
                                               original_url=page,
                                               filename=filename,
                                               file_url=imageId_production,   #/file/find/61e50b1c2bddbd32a0843685/e26c3c39a39388bccd871c20ce52a10e
                                               create_time=datetime.datetime.now(),
                                               create_by=0)


                    f_test = QualityFile(ID=f_id,
                                         original_url=page,
                                         filename=filename,
                                         file_url=imageId_test,
                                         create_time=datetime.datetime.now(),
                                         create_by=0)

                    article_list_production = self.session_production.query(QualityList).filter_by(url=page).first()
                    article_list_test = self.session_test.query(QualityList).filter_by(url=page).first()

                    if not article_list_production.date or not article_list_test.date:
                        article_list_production.date = item.date
                        article_list_test.date = item.date

                    # session_test.add(f_test)
                    fs.append(f_production)
                    fs2.append(f_test)

                    q_production.files = fs
                    q_test.files = fs2

                    self.session_production.add(article_list_production)
                    self.session_test.add(article_list_test)
                    self.session_production.add(q_production)
                    self.session_test.add(q_test)
                    self.session_production.commit()
                    self.session_test.commit()
                    driver.quit()
                    return True
                else:
                    article_list_production = self.session_production.query(QualityList).filter_by(url=page).first()
                    article_list_test = self.session_test.query(QualityList).filter_by(url=page).first()

                    if not article_list_production.snapshot_id:
                        article_list_production.snapshot_id = q_id

                    if not article_list_test.snapshot_id:
                        article_list_test.snapshot_id = q_id

                    if not article_list_production.date or not article_list_test.date:
                        article_list_production.date = item.date
                        article_list_test.date = item.date

                    for existing_production in existing_production_list:
                        existing_production.notification_title = item.title
                        self.session_production.commit()

                    for existing_test in existing_test_list:
                        existing_test.notification_title = item.title
                        self.session_test.commit()

                    print('updata\n')

                    f_id = get_id()
                    data = requests.get(page, headers=self.headers)
                    file_name = page.split(".")[-1]
                    filename = item.title + '.' + file_name
                    # 附件保存至mongodb
                    # 保存至生产环境mongodb
                    imageId_production = uploadFile(filename, data.content, f_id,self.mongodb_production,
                                                    DATABASES['mongodb']['gridFS'])
                    # imageId_production = uploadFile(filename, f_id, self.mongodb_production)


                    # 保存至测试环境mongodb
                    imageId_test = uploadFile(filename, data.content, f_id,self.mongodb_test,
                                                    DATABASES_TEST['mongodb']['gridFS'])
                    # imageId_test = uploadFile(filename, f_id, self.mongodb_test)

                    print(imageId_production, imageId_test)

                    itemList = self.session_production.query(Quality).filter_by(source_url=page).first()
                    itemfile = self.session_production.query(QualityFile).filter_by(snapshot_id=itemList.ID).first()

                    itemList_test = self.session_test.query(Quality).filter_by(source_url=page).first()
                    itemfile_test = self.session_test.query(QualityFile).filter_by(snapshot_id=itemList_test.ID).first()

                    itemfile.filename = filename
                    itemfile.original_url = page
                    itemfile.file_url = imageId_production

                    itemfile_test.filename = filename
                    itemfile_test.original_url = page
                    itemfile_test.file_url = imageId_production

                    self.session_production.commit()
                    self.session_test.commit()
                    return True

            if '404' in driver.title:
                errData = [create_time, page, 404, str(scraper.ID) + "\t", ""]
                self.sheet1.append(errData)
                self.wb.save(self.csvfilepath)

                defeated += 1
                defeated_test += 1
                item.defeated = defeated
                list_test.defeated = defeated_test

                self.session_production.commit()
                self.session_test.commit()
                print('拒绝访问,状态码：', 404, page)
                driver.quit()
                return False

            driver.get(page)
            time.sleep(1)

            # 发布时间
            date = None
            try:
                datere = re.compile(scraper.reDate)
                datestr = driver.current_url
                if scraper.byDate:
                    # datestr = driver.find_elements_by_xpath('//*[@class="publish"]')[0].text
                    # print(scraper.byDate)
                    datestr = find(driver, scraper.byDate)[0].text.replace(' ','').replace('\n','')

                redate = re.findall(scraper.reDate, datestr)
                print(redate)
                datem = datere.search(datestr)
                if redate:
                    redate = redate[0]
                    date = datetime.datetime.strptime("{}-{}-{}".format(redate[0], redate[1], redate[2]),
                                                      "%Y-%m-%d").date()
                elif datem:
                    dateg = datem.groups()
                    date = datetime.datetime.strptime("{}-{}-{}".format(dateg[0], dateg[1], dateg[2]),
                                                      "%Y-%m-%d").date()
            except Exception as err:
                date = item.date
                print("date:", err)
                self.logger.warning(err)

            pagetitle = driver.title.replace('\n', '').replace('/', '').replace('<B>', '').replace(
                '<br>','').replace('"','”')
            # 公告标题
            try:
                article_title = find(driver, scraper.byTitle)[0].text.replace('\n', '').replace('/', '').replace(
                    '<B>', '').replace('<br>', '').replace('"', '”')
            except Exception as err:
                print("title:", err)
                article_title = item.title
                self.logger.warning(err)

            if 'scjgj.shanxi.gov.cn' in page:
                date = item.date
            if 'scjgj.suzhou.gov.cn' in page:
                article_title = pagetitle
            if item.src == 1351824355541397504 or item.src == 1351822647650168832:
                article_title = item.title

            print('article_title:', article_title, date)
            if article_title and "该页已移动或删除" not in pagetitle and date:
                title = article_title
                print(title, date, page)
                # 附件链接和响应对象的字典
                files = {}
                # 附件链接对应的文件名
                filesName = {}
                try:
                    content = find(driver, scraper.byContent)[0].get_attribute('innerHTML')
                    try:
                        pdfUrl = find(driver, scraper.byContent + '//iframe')[0].get_attribute("src")
                        print('正文PDF：', pdfUrl)
                        # 将PDF正文转换成字符
                        # content = readPDF(pdfUrl)
                        # 将PDF正文保存成附件
                        if proxy:
                            data = requests.get(pdfUrl, headers=self.headers, proxies=self.proxies, timeout=60)
                        else:
                            data = requests.get(pdfUrl, headers=self.headers)
                        files[pdfUrl] = data
                        filesName[pdfUrl] = ''.join([title, '-正文.pdf'])
                    except:
                        pass
                    content = minify(content, True, True, True)
                except Exception as err:
                    print('content:', err)
                    content = driver.find_elements_by_xpath('//*[@id="js_content"]')[0].get_attribute('innerHTML')
                    content = minify(content, True, True, True)
                    self.logger.warning(err)
                    # return False

                # 保存内容
                content = clearmb4(content)
                content_id_production = cutting_content(content, self.mongodb_production)
                content_id_test = cutting_content(content, self.mongodb_test)

                filepath = title.replace('\n', '').replace(':', '：').replace('/', '') + '.png'
                if len(title) > 50:
                    filepath = title[:45].replace('\n', '').replace(':', '：').replace('/', '').strip() + '.png'

                filesList = find(driver, scraper.byFile)
                if not filesList:
                    filesList = driver.find_elements_by_xpath('//div[@class="wzcon j-fontContent clearfix"]//a')

                for file in filesList:
                    try:
                        fileaddr = file.get_attribute("href")
                        fileaddrName = file.get_attribute('textContent')
                        file_name = fileaddr.split(".")[-1]
                        if fileaddrName == '':
                            fileaddrName = '默认附件命名'
                        if fileaddrName.endswith(".pdf") or fileaddrName.endswith(".xlsx") or fileaddrName.endswith(
                            ".xls") or fileaddrName.endswith(".docx") or fileaddrName.endswith(
                            ".doc") or fileaddrName.endswith(".zip") or fileaddrName.endswith(".rar"):
                            fileaddr_name = fileaddrName
                        else:
                            if 'pdf' in file_name or 'xlsx' in file_name or 'xls' in file_name or 'docx' in file_name or 'doc' in file_name or 'zip' in file_name or 'rar' in file_name:
                                if '.' + file_name in fileaddrName:
                                    fileaddr_name = fileaddrName
                                else:
                                    fileaddr_name = fileaddrName + '.' + file_name
                            else:
                                continue
                        fileaddr_name = fileaddr_name.replace(' ', '').replace('\n', '').replace('/', '').replace(
                            ':', '：').replace('"', '”').replace('．', '.').replace('\xa0', '.').strip()

                        self.logger.info("FILE\t{}".format(fileaddr))
                        if fileaddr and fileaddrName.endswith(".pdf") or fileaddrName.endswith(
                            ".xlsx") or fileaddrName.endswith(".xls") or fileaddrName.endswith(
                            ".docx") or fileaddrName.endswith(".doc") or fileaddrName.endswith(
                            ".zip") or fileaddrName.endswith(".rar"):
                            try:
                                self.logger.info('files download')
                                if proxy:
                                    data = session.get(fileaddr, headers=self.headers, proxies=self.proxies, timeout=60)
                                else:
                                    data = session.get(fileaddr, headers=self.headers)
                                files[fileaddr] = data
                                filesName[fileaddr] = fileaddr_name
                            except Exception as err:
                                self.logger.warning(err)
                                files[fileaddr] = None
                                filesName[fileaddr] = None
                        else:
                            files[fileaddr] = None
                            filesName[fileaddr] = None
                    except Exception as err:
                        self.logger.warning(err)
                existing_production_list = self.session_production.query(Quality).filter_by(source_url=page).all()
                existing_test_list = self.session_test.query(Quality).filter_by(source_url=page).all()

                # 查重
                if not existing_production_list:
                    if item.classify != '比较试验':
                        # 快照
                        imageId = get_snapshot(driver=driver, filepath=filepath, id=q_id,
                                               mongodb=self.mongodb_production,
                                               gridFS=DATABASES['mongodb']['gridFS'])
                        if imageId:
                            print(imageId)
                            print('ok', filepath)
                        else:
                            print('ERR:imageId is None')
                            return False
                    else:
                        imageId = None
                        print('isquality:False')

                    article_list_production = self.session_production.query(QualityList).filter_by(
                        id=item.id).first()
                    article_list_production.snapshot_id = q_id

                    article_list_test = self.session_test.query(QualityList).filter_by(id=item.id).first()
                    article_list_test.snapshot_id = q_id

                    if '...' in item.title or '…' in item.title:
                        article_list_production.title = title
                        article_list_test.title = title

                    if not article_list_production.date or not article_list_test.date:
                        article_list_production.date = date
                        article_list_test.date = date

                    q_production = Quality(ID=q_id,
                                           notification_title=title,
                                           content=content_id_production,
                                           source_url=page,
                                           spider_channel_id=scraper.ID,
                                           create_time=datetime.datetime.now(),
                                           create_by=0,
                                           notification_date=date,
                                           snap_url=imageId,
                                           collect_time=datetime.datetime.now(),
                                           update_time=datetime.datetime.now())

                    q_test = Quality(ID=q_id,
                                     notification_title=title,
                                     content=content_id_test,
                                     source_url=page,
                                     spider_channel_id=scraper.ID,
                                     create_time=datetime.datetime.now(),
                                     create_by=0,
                                     notification_date=date,
                                     snap_url=imageId,
                                     collect_time=datetime.datetime.now(),
                                     update_time=datetime.datetime.now())

                    # 处理附件
                    fs = []
                    fs2 = []
                    for file in files.keys():
                        f_id = get_id()
                        data = files[file]
                        f_production = QualityFile(original_url=file)
                        f_test = QualityFile(original_url=file)
                        if data:
                            headers = data.headers
                            filename = filesName[file]
                            if filename:
                                if not filename and os.path.basename(file):
                                    filename = os.path.basename(file).split("?")[0]
                                self.logger.info("{}\t{}\t{}".format(file, filename, len(data.content)))

                                # 保存至生产环境mongodb
                                imageId_production = uploadFile(filename, data.content, f_id, self.mongodb_production, DATABASES['mongodb']['gridFS'])

                                # 保存至测试环境mongodb
                                imageId_test = uploadFile(filename, data.content, f_id, self.mongodb_test, DATABASES_TEST['mongodb']['gridFS'])

                                print(imageId_production, imageId_test)
                                print("ok", filename)

                                print(f_id)
                                f_production = QualityFile(ID=f_id,
                                                           original_url=file,
                                                           filename=filename,
                                                           file_url=imageId_production,
                                                           create_by=0,
                                                           create_time=datetime.datetime.now())

                                f_test = QualityFile(ID=f_id,
                                                     original_url=file,
                                                     filename=filename,
                                                     file_url=imageId_test,
                                                     create_by=0,
                                                     create_time=datetime.datetime.now())
                            else:
                                continue
                            fs.append(f_production)
                            fs2.append(f_test)

                    # 解析召回信息配图
                    if item.classify == '召回' and scraper.ID != 1363068162958176256:
                        image_url_list = find(driver, scraper.byContent + '//img')
                        if len(image_url_list) > 0:
                            for image_url in image_url_list:
                                image_url = image_url.get_attribute("src")
                                image_file_name = str(get_id()) + '.png'
                                if scraper.ID == 1367371348984475648:
                                    # base64转图片
                                    image_data = base64_to_image(filename=image_file_name, data=image_url)
                                    image_url = item.url
                                else:
                                    if 'http' not in image_url or 'https' not in image_url:
                                        image_url = 'http://' + image_url
                                    # 附件保存至mongodb
                                    image_data = requests.get(image_url, headers=self.headers).content

                                image_id = get_id()

                                # 保存至生产环境mongodb
                                imageId_production = uploadFile(image_file_name, image_data, image_id, self.mongodb_production, DATABASES['mongodb']['gridFS'])

                                # 保存至测试环境mongodb
                                imageId_test = uploadFile(image_file_name, image_data, image_id, self.mongodb_test, DATABASES_TEST['mongodb']['gridFS'])

                                print(imageId_production, imageId_test)
                                print("ok image:", image_file_name)

                                i_production = QualityFile(ID=image_id,
                                                           original_url=image_url,
                                                           filename=image_file_name,
                                                           file_url=imageId_production,
                                                           create_by=0,
                                                           create_time=datetime.datetime.now())

                                i_test = QualityFile(ID=image_id,
                                                     original_url=image_url,
                                                     filename=image_file_name,
                                                     file_url=imageId_test,
                                                     create_by=0,
                                                     create_time=datetime.datetime.now())

                                fs.append(i_production)
                                fs2.append(i_test)

                    q_production.files = fs
                    q_test.files = fs2

                    self.session_production.add(article_list_production)
                    self.session_test.add(article_list_test)

                    self.session_production.add(q_production)
                    self.session_test.add(q_test)

                    self.session_production.commit()
                    self.session_test.commit()
                    self.logger.info('url:{}\timageId:{}\tstate:{}'.format(page, imageId, filepath))

                    if scraper.classify == '召回':
                        self.zhaohui_newdata += 1
                    elif scraper.classify == '比较试验':
                        self.bjsy_newdata += 1
                    else:
                        self.newdata += 1
                else:
                    if item.classify != '比较试验':
                        # 快照
                        imageId = get_snapshot(driver=driver,
                                               filepath=filepath,
                                               id=q_id,
                                               mongodb=self.mongodb_production,
                                               gridFS=DATABASES['mongodb']['gridFS'])
                    else:
                        imageId = None

                    article_list_production = self.session_production.query(QualityList).filter_by(
                        id=item.id).first()
                    article_list_test = self.session_test.query(QualityList).filter_by(id=item.id).first()

                    print(item.title)
                    if '...' in item.title or '…' in item.title:
                        article_list_production.title = title
                        article_list_test.title = title

                    if not article_list_production.date or not article_list_test.date:
                        article_list_production.date = date
                        article_list_test.date = date

                    for existing_production in existing_production_list:
                        # snapshot_id
                        if not article_list_production.snapshot_id:
                            article_list_production.snapshot_id = existing_production.ID

                        if not existing_production.snap_url and item.classify != '比较试验':
                            existing_production.snap_url = imageId
                        else:
                            # 获取到原快照保存的mongoDB ID
                            snap_url_id = re.findall(r'/file/find/(.+)/.+', existing_production.snap_url)[0]
                            # 删除掉旧的快照文件
                            self.mongodb_production.removeFile(snap_url_id, 'fs')
                            existing_production.snap_url = imageId

                        existing_production.notification_title = title
                        existing_production.notification_date = date
                        # 正文
                        if not existing_production.content:
                            content_id_production = cutting_content(content, self.mongodb_production)
                            existing_production.content = content_id_production
                        else:
                            # 删除掉旧的正文数据
                            self.mongodb_production.delete(existing_production.content, 'notificationContent')
                            existing_production.content = content_id_production

                        existing_production.update_time = datetime.datetime.now()

                        self.session_production.commit()

                    for existing_test in existing_test_list:
                        # snapshot_id
                        if not article_list_test.snapshot_id:
                            article_list_test.snapshot_id = existing_test.ID

                        existing_test.notification_title = title
                        existing_test.notification_date = date
                        # 正文
                        if not existing_test.content:
                            content_id_test = cutting_content(content, self.mongodb_test)
                            existing_test.content = content_id_test
                        else:
                            # 删除掉旧的正文数据
                            self.mongodb_production.delete(existing_test.content, 'notificationContent')
                            existing_test.content = content_id_test

                        existing_test.update_time = datetime.datetime.now()

                        self.session_test.commit()
                    print('updata\n')

                    if scraper.classify == '召回':
                        self.zhaohui_updata += 1
                    elif scraper.classify == '比较试验':
                        self.bjsy_updata += 1
                    else:
                        self.updata += 1
                driver.quit()
                return True
            else:
                if not date:
                    errData = [create_time, page, str(scraper.ID) + "\t", "发布时间匹配失败,或无法正常访问"]
                    print('缺失发布时间,状态码：', page)
                elif not article_title:
                    errData = [create_time, page, str(scraper.ID) + "\t", "公告标题匹配失败,或无法正常访问"]
                    print('公告标题缺失,状态码：', page)
                elif '该页已移动或删除' in pagetitle:
                    errData = [create_time, page, str(scraper.ID) + "\t", "该页已移动或删除"]
                    print('该页已移动或删除：', page)
                    defeated += 3
                    defeated_test += 3
                    list_test.defeated = defeated_test
                    item.defeated = defeated

                    self.session_production.commit()
                    self.session_test.commit()

                else:
                    errData = [create_time, page, str(scraper.ID) + "\t", "无法正常访问"]
                    print('无法正常访问,状态码：', page)

                self.sheet1.append(errData)
                self.wb.save(self.csvfilepath)
                driver.quit()
                return False

        except Exception as err:
            with open(self.path + 'err_url.log', 'a', encoding="utf-8") as f:
                f.write('{}\turl:{}\tspider_channel:{}\n'.format(create_time, page, scraper.ID))
            print('errUrl无法正常访问:', page)
            print(err)
            self.logger.warning(err)

            self.proxy = get_proxy()

            errData = [create_time, page, "", str(scraper.ID) + "\t", str(err)]
            self.sheet1.append(errData)
            self.wb.save(self.csvfilepath)

            exstr = traceback.format_exc()
            self.logger.error(exstr)
            self.session_production.rollback()
            self.session_test.rollback()
            driver.quit()
            return False

    def runsanp(self,scraper):
        list = self.session_production.query(QualityList).filter(QualityList.src == scraper.ID,
                                                                 QualityList.indb == 0,
                                                                 QualityList.defeated < 4).all()       #这个表spider_article_list
        for item in list:
            try:
                # 预测公告标题
                # TODO 应考虑先过滤掉已经打过标的
                # predict_one_from_mysql(item.id)
                article_tag = self.session_production.query(SpiderArticleTag).filter_by(       #这个表spider_article_tag
                    spider_article_list_id=item.id).first()     #获取第一个元素
                if not article_tag:
                    predict_one_from_mysql(item.id)
                    article_tag = self.session_production.query(SpiderArticleTag).filter_by(
                        spider_article_list_id=item.id).first()
                print('此标题分类打标tag：', article_tag.tag)
                tag = int(article_tag.tag)
            except Exception as err:
                self.logger.warning(str(err) + 'ListId' + str(item.id))
                tag = 15
            if tag == 15 or tag == 19 or scraper.classify == '比较试验' or scraper.classify == '召回':

                if scraper.site_administrator_id == '6735912978988560385' or scraper.site_administrator_id == '1254298127759020038':
                    self.proxy = get_proxy()
                    print(self.proxy)
                    res = self.runpage(scraper, item, self.proxy)
                else:
                    res = self.runpage(scraper, item)

                list_test = self.session_test.query(QualityList).filter_by(id=item.id).first()
                if res:
                    list_test.indb = True
                    item.indb = True

                    if scraper.classify == '召回' or tag == 19:
                        self.zhaohui_succeed += 1
                    elif scraper.classify == '比较试验':
                        self.bjsy_succeed += 1
                    else:
                        self.succeed += 1

                    self.session_production.commit()
                    self.session_test.commit()
                else:
                    if scraper.classify == '召回' or tag == 19:
                        self.zhaohui_fail += 1
                    elif scraper.classify == '比较试验':
                        self.bjsy_fail += 1
                    else:
                        self.fail += 1

                    list_test.defeated += 1
                    item.defeated += 1
                    self.session_production.commit()
                    self.session_test.commit()

                if scraper.classify == '召回' or tag == 19:
                    self.zhaohui_quality_amount += 1
                elif scraper.classify == '比较试验':
                    self.bjsy_quality_amount += 1
                else:
                    self.quality_amount += 1

                print('此次处理抽检公告详情总数：', self.quality_amount, '公告快照爬取成功数：', self.succeed, '公告快照爬取失败数：', self.fail,
                      '此次处理召回信息采集总数：', self.zhaohui_quality_amount, '召回信息爬取成功数：', self.zhaohui_succeed,
                      '召回信息爬取失败数：', self.zhaohui_fail,
                      '此次处理比较试验采集总数：', self.bjsy_quality_amount, '比较试验爬取成功数：', self.bjsy_succeed, '比较试验爬取失败数：',
                      self.bjsy_fail
                      )
                print('\n')

    def runlist(self, scraper):
        if scraper.site_administrator_id == '6735912978988560385' or scraper.site_administrator_id == '1254298127759020038':
            self.proxy = get_proxy()
            print(self.proxy)
            driver = getWebdriver(proxy=self.proxy)
            # driver = setProxy(driver, proxy)
        else:
            # 浏览器驱动
            driver = getWebdriver()

        self.driver = driver
        driver.set_page_load_timeout(90)  #set_page_load_timeout() 设置网页超时加载时间
        driver.set_script_timeout(90)

        driver.get(scraper.source_url)

        index = 1
        pages = set()
        flag = False
        while True:
            time.sleep(2)
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            flag = False
            if (scraper.byFrame):
                driver.switch_to.frame(find(driver, scraper.byFrame)[0])
            items = find(driver, scraper.byItem)
            dates = find(driver, scraper.byItemDate)
            if scraper.ID == 1250613341882327069:
                del dates[0]
            try:
                if '公开日期' in dates:
                    dates.remove('公开日期')
            except:
                pass
            self.logger.info("{}\t{}".format(scraper.name, driver.current_url))
            idx = 0
            _dx = 0
            if not items:
                break
            for i in items:
                _dx = _dx+1
                try:
 # < a href = "http://amr.ah.gov.cn/public/5248926/146380621.html"class ="title xh-highlight" target="_blank" > 安徽省市场监督管理局食品安全抽检信息通告（2022年第1期） </ a>
                    title = items[idx].get_attribute('title').replace('\n', '').replace('<P>', '').replace('</P>', '').replace('\u2002', '”')
                    if 'cat:' in title:
                        title = driver.title.replace('\n', '').replace('/', '').replace('<B>', '').replace(
                            '<br>','').replace('"', '”')
                except Exception as err:
                    title = items[idx].get_attribute("textContent").replace('\n', '').replace('\u2002', '”')
                    self.logger.warning(err)

                try:
                    addr = items[idx].get_attribute("href").split(';')[0]
                except Exception as err:
                    # self.logger.warning(f'addr.split-ERR:{err}')
                    addr = items[idx].get_attribute("href")

                # 针对个别网站特殊处理
                # TODO 对一些结构特殊的需要抽取出来独立管理
                if scraper.ID == 1367371348984475648:
                    dates = find(driver, scraper.byItemDate)
                    addr = 'http://swj.xm.gov.cn/xmtbt-sps/show.asp?id=' + \
                           find(driver, f'x//*[@class="list_ul"]/li[{idx + 1}]')[0].get_attribute(
                               'aid').replace('\n','')
                elif scraper.ID == 1371341646410821632:
                    data_link = items[idx].get_attribute("data_link")
                    if data_link != '' and data_link != 'null':
                        addr = data_link
                    else:
                        addr_id = items[idx].get_attribute("id")
                        channel_id = items[idx].get_attribute("data_id")
                        textId = items[idx].get_attribute("data_textid")
                        category_id = items[idx].get_attribute("data_category")
                        addr = f'http://www.jl315.org/Form/listDetails.html?id={addr_id}&channel_id={channel_id}&textId={textId}&category_id={category_id}&data_type=guidance&module=compare&doType=undefined'
                elif scraper.ID == 1371378987573719040:
                    _data_link = items[idx].get_attribute("data-link")
                    if _data_link != '' and _data_link != 'null':
                        addr = _data_link
                    else:
                        addr_id = items[idx].get_attribute("id")
                        channel_id = items[idx].get_attribute("data-id")
                        textId = items[idx].get_attribute("data-textid")
                        category_id = items[idx].get_attribute("data-category")
                        addr = f'https://web.jshcsoft.com/jiangsu/HTML/listDetails.html?id={addr_id}&channel_id={channel_id}&type=undefined&textId={textId}&category_id='
                elif scraper.ID == 1250613341882327061:
                    if addr is None:
                        addr_id = re.findall(r'gotodetial\((.*)\);', find(driver, f'x//div[@class="zw-right-list"]/ul/li[{idx + 1}]/a')[0].get_attribute(
                                   'onclick').replace('\n', ''))[0]
                        addr = f'http://scjg.nx.gov.cn/article/{addr_id}.html'
                elif scraper.ID == 1427570152001777664:
                    if addr is None:
                        addr_id = re.findall(r'name2\(\'(.*)\'\)', items[idx].get_attribute(
                                   'onclick').replace('\n', ''))[0]
                        addr = f'http://scjgj.lyg.gov.cn{addr_id}'
                elif scraper.ID == 1439127896961855488:
                    addr_id =find(driver,f'x//*[@class="test rightList supervise_list active"]/div[{_dx}]')[0].get_attribute("id")
                    channel_id =find(driver,f'x//*[@class="test rightList supervise_list active"]/div[{_dx}]')[0].get_attribute("data_id")

                    addr = f'http://www.njsxbw.com/Form/infoDetails.html?id={addr_id}&channel_id={channel_id}'

                elif scraper.ID == 1440568584064741376:
                    addr_id =find(driver,f'x//*[@class="compareListWrap"]/div[{_dx}]')[0].get_attribute("datas")
                    channel_id =find(driver,f'x//*[@class="compareListWrap"]/div[{_dx}]')[0].get_attribute("channelid")

                    addr = f'http://yn315.org.cn/html/details.html?id={addr_id}&channel_id={channel_id}'

                elif scraper.ID == 1440572434133823488:
                    data_link = find(driver,f'x//*[@class="bjsy-list"]/li[{_dx}]/a')[0].get_attribute("data_link")

                    addr_id =find(driver,f'x//*[@class="bjsy-list"]/li[{_dx}]/a')[0].get_attribute("id")
                    channel_id =find(driver,f'x//*[@class="bjsy-list"]/li[{_dx}]/a')[0].get_attribute("channel_id")
                    row_number = find(driver, f'x//*[@class="bjsy-list"]/li[{_dx}]/a')[0].get_attribute("row_number")
                    category_id = find(driver, f'x//*[@class="bjsy-list"]/li[{_dx}]/a')[0].get_attribute("category_id")
                    if not data_link:
                        addr = f'http://www.qh315.org/Form/frm_PublicInfo.htm?id={addr_id}&channel_id={channel_id}&row_number={row_number}&category_id={category_id}'

                    else:
                        addr = data_link

                print(addr)
                if scraper.byItemTitle:
                    title = find(driver, scraper.byItemTitle.format(idx + 1))[0].get_attribute(
                        "title").replace('\n', '').replace('\u2002', '”').replace('\u200b', '”')
                    if not title:
                        title = find(driver, scraper.byItemTitle.format(idx + 1))[0].text.replace("\n", "")
                if not title:
                    title = items[idx].text.replace("\n", "")

                if scraper.byItemUrl:
                    addr = find(driver, scraper.byItemUrl.format(idx + 1))[0].get_attribute("href")

                if scraper.fmtClick:
                    id = items[idx].get_attribute("onclick")
                    if not id:
                        id = items[idx].get_attribute("data-id")
                    if id:
                        mid = self.numre.search(id)
                        if mid:
                            addr = scraper.fmtClick.replace("{0}", "{}").format(mid.group())

                if addr is None or len(addr) == 0:
                    continue

                try:
                    if not self.hasaddr(addr):  #self.hasaddr得到的是这个self.session_production.query(QualityList).filter_by(url=addr).all()   这个原本表里面有内容，判断url跟传过来的标题地址是否一样，不一样就把标题地址传进去
                        if scraper.classify == '召回':
                            self.zhaohui_list_count += 1
                        elif scraper.classify == '比较试验':
                            self.bjsy_list_count += 1
                        else:
                            self.list_count += 1
                        self.logger.info("New\t{}".format(addr))
                        pages.add(addr)  #set(addr)
                        date = None
                        datestr = None
                        try:
                            datere = re.compile(scraper.reItemDate)
                            if scraper.byItemDate[0] == 'a':
                                datestr = items[idx].get_attribute(scraper.byItemDate[1:])  # 得到响应字符串的内容  adate-time   byItemDate[1:]字符串别片得到date-time   得到相应的value
                            elif dates is not None and len(dates) > idx:
                                datestr = dates[idx].text
                        except:
                            pass
                        if datestr is not None:
                            try:
                                datem = datere.search(datestr)   #正则得到对应的具体时间
                                if datem:
                                    dateg = datem.groups()
                                    if len(dateg) == 2:
                                        year = datetime.datetime.now().year
                                        date = datetime.datetime.strptime("{}-{}-{}".format(year, dateg[0], dateg[1]),
                                                                          "%Y-%m-%d").date()
                                    elif len(dateg) == 3:
                                        date = datetime.datetime.strptime(
                                            "{}-{}-{}".format(dateg[0], dateg[1], dateg[2]), "%Y-%m-%d").date()    #date才是得到具体的日期
                            except:
                                exstr = traceback.format_exc()
                                self.logger.error(exstr)
                        # else:
                        #     errData = [create_time, addr, '', str(scraper.ID) + "\t", "reItemDate 为空"]
                        #     sheet1.append(errData)
                        #     wb.save(csvfilepath)

                        if '...' in title or not dates:
                            driver.get(addr)
                            try:
                                if '...' in title:
                                    full_title = find(driver, scraper.byTitle)[0].text.replace('\n', '').replace(
                                        '/', '').replace('<B>', '').replace('<br>', '').replace('"', '”').replace('\u2002', '”')
                                    title = full_title
                                elif not dates:
                                    # 发布时间
                                    date = None
                                    datere = re.compile(scraper.reDate)
                                    datestr = driver.current_url
                                    if scraper.byDate:
                                        # datestr = driver.find_elements_by_xpath('//*[@class="publish"]')[0].text
                                        # print(scraper.byDate)
                                        datestr = find(driver, scraper.byDate)[0].text.replace(' ','').replace('\n','')

                                    redate = re.findall(scraper.reDate, datestr)
                                    datem = datere.search(datestr)
                                    if redate:
                                        redate = redate[0]
                                        date = datetime.datetime.strptime(
                                            "{}-{}-{}".format(redate[0], redate[1], redate[2]),
                                            "%Y-%m-%d").date()
                                    elif datem:
                                        dateg = datem.groups()
                                        date = datetime.datetime.strptime(
                                            "{}-{}-{}".format(dateg[0], dateg[1], dateg[2]),
                                            "%Y-%m-%d").date()
                                time.sleep(.25)
                                driver.back()
                            except Exception as err:
                                exstr = traceback.format_exc()
                                self.logger.error(exstr)
                                driver.back()
                            items = find(driver, scraper.byItem)
                            dates = find(driver, scraper.byItemDate)

                        ss = " ".join(jieba.cut(title, True))
                        print(ss)
                        classify = self.model.predict(ss)[0][0]
                        classify = classify.replace("__label__", "")
                        isquality = classify != '非'
                        indb = self.session_production.query(func.count(Quality.source_url)).filter_by(
                            source_url=addr).scalar() > 0
                        if not indb:
                            memo = ''
                            if date:
                                if create_time < date.strftime("%Y-%m-%d %H:%M:%S"):
                                    memo = '时间超前'

                            if scraper.classify == '召回':
                                classify = '召回'
                            elif scraper.classify == '比较试验':
                                classify = '比较试验'
                            l_id = get_id()
                            site_administrator_id = scraper.site_administrator_id
                            if site_administrator_id == '':
                                site_administrator_id = 0

                            l = QualityList(id=l_id,
                                            date=date,
                                            title=title,
                                            url=addr,
                                            src=scraper.ID,
                                            classify=classify,
                                            defeated=0,
                                            isquality=isquality,
                                            indb=indb,
                                            organization_id=site_administrator_id,
                                            create_time=datetime.datetime.now(),
                                            memo=memo)
                            #  create_time=datetime.datetime.now()
                            l2 = QualityList(id=l_id,
                                             date=date,
                                             title=title,
                                             url=addr,
                                             src=scraper.ID,
                                             classify=classify,
                                             defeated=0,
                                             isquality=isquality,
                                             indb=indb,
                                             organization_id=site_administrator_id,
                                             create_time=datetime.datetime.now(),
                                             memo=memo)

                            self.session_production.add(l)
                            self.session_test.add(l2)

                            if scraper.classify == '召回':
                                self.zhaohui_list_new += 1
                            elif scraper.classify == '比较试验':
                                self.bjsy_list_new += 1
                            else:
                                self.list_new += 1
                            flag = True
                        else:
                            self.logger.info("Exists\t{}".format(addr))
                    else:
                        self.logger.info("Exists\t{}".format(addr))
                except Exception as err:
                    self.logger.info(f'公告清单保存失败:{addr}')
                    exstr = traceback.format_exc()
                    self.logger.error(exstr)
                    errData = [create_time, addr, '', str(scraper.ID) + "\t", "无法正常访问"]

                    self.sheet1.append(errData)
                    self.wb.save(self.csvfilepath)

                    if scraper.classify == '召回':
                        self.zhaohui_list_fail += 1
                    elif scraper.classify == '比较试验':
                        self.bjsy_list_fail += 1
                    else:
                        self.list_fail += 1
                    flag = True

                    continue
                idx += 1
                self.session_production.commit()
                self.session_test.commit()

            index += 1
            print(flag, index)
            if not self.nextpage(driver, scraper, index):
                self.logger.info("Last Page")
                driver.quit()
                break
            if not flag:
                driver.quit()
                break

    def update(self, scraper):
        scraper.total_article = self.session_production.query(func.count(QualityList.id)).filter_by(
            src=scraper.ID).scalar()
        scraper.total_matched = self.session_production.query(func.count(QualityList.id)).filter_by(src=scraper.ID,
                                                                                                    isquality=True).scalar()
        scraper.total_stocked = self.session_production.query(func.count(QualityList.id)).filter_by(src=scraper.ID,
                                                                                                    indb=True).scalar()
        self.session_production.commit()

        scraper.total_article_test = self.session_test.query(func.count(QualityList.id)).filter_by(
            src=scraper.ID).scalar()
        scraper.total_matched_test = self.session_test.query(func.count(QualityList.id)).filter_by(src=scraper.ID,
                                                                                                   isquality=True).scalar()
        scraper.total_stocked_test = self.session_test.query(func.count(QualityList.id)).filter_by(src=scraper.ID,
                                                                                                   indb=True).scalar()
        self.session_test.commit()
        spiderPros = self.session_production.query(SpiderPros).filter_by(spider_channel_id=scraper.ID).first()
        spiderPros_test = self.session_test.query(SpiderPros).filter_by(spider_channel_id=scraper.ID).first()
        if spiderPros:
            spiderPros.total_article = scraper.total_article
            spiderPros.total_matched = scraper.total_matched
            spiderPros.total_stocked = scraper.total_stocked

            spiderPros_test.total_article = scraper.total_article
            spiderPros_test.total_matched = scraper.total_matched
            spiderPros_test.total_stocked = scraper.total_stocked
        self.session_production.commit()
        self.session_test.commit()

    def run_take(self, take):
        for scraper in take:
            self.logger.info("{}\t{}\t{}".format(scraper.name, scraper.source_url, scraper.areaCode))
            sys.stderr, "{}\t{}\t{}".format(scraper.name, scraper.source_url, scraper.areaCode)
            print(scraper.name, scraper.source_url)

            self.upadate_email_data()
            try:
                self.runlist(scraper)

                self.runsanp(scraper)

            except Exception as err:
                self.logger.error(err)
                exstr = traceback.format_exc()
                self.logger.error(exstr)
            print('----'*10)
            quit_all_driver()
            scraper.lastupdate = datetime.datetime.now()
            sys.stdout.flush()
            self.update(scraper)
            # 记录本次爬取结果
            self.commit_email_data()


    def run(self):
        # 加载所有模型
        load_all_ft_model()
        load_all_cnn_model()

        # 创建任务表
        self.create_take_log()

        try:
            self.logger.info("Scraper Start")
            #filter()  直接查询里面的语句的
            first_ret = self.session_production.query(QualityScraper) \
                .filter(
                QualityScraper.valid == 1,
                QualityScraper.site_administrator_id != '6735912978988560385',
                QualityScraper.site_administrator_id != '1298138644116279320',
            ).offset(338).all()    #offset(338)开始从第338条开始

            self.run_take(first_ret)    

            # print('----------------orther_ret------------------')
            # orther_ret = self.session_production.query(QualityScraper).filter(QualityScraper.valid == 1,
            #                                                            QualityScraper.site_administrator_id == 6735912978988560385
            #                                                            ).all()

            # self.run_take(orther_ret)
            # self.driver.set_page_load_timeout(120)
            # self.driver.set_script_timeout(120)
            # orther_ret = self.session_production.query(QualityScraper).filter(QualityScraper.valid == 1,
            #                                                            QualityScraper.site_administrator_id == 1298138644116279320
            #                                                            ).all()
            # self.run_take(orther_ret)

        except Exception as e:
            logging.warning(e)
            quit_all_driver()

        self.logger.info("Scraper End")

    def __del__(self):
        self.driver.quit()


q = QualitySpider()
q.run()
quit_all_driver()
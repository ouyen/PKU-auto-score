from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
from datetime import date
import requests


class Score_Bot:

    def __init__(self) -> None:
        self.score_dict={}
        self.send_message_url=''
        self.password=""
        self.username=""
        self.sleep_time=1*60
        self.loop_times=1
        self.driver_bug_count=0

    def read_config(self,file='config.json'):
        with open(file,'r') as f:
            config_dict=json.load(f)
        self.username=config_dict['username']
        self.password=config_dict['password']
        self.send_message_url=config_dict['send_message_url']
        self.sleep_time=int(config_dict['sleep_time'])*60

    def gpa(self,score):
        # GPA(x) = 4-3*(100-x)2/1600
        if score=='W':
            return 'W'
        score=int(score)
        return "%.3f"%(4-3*(100-score)**2/1600)

    def send_message(self, raw_message: str):
        if self.send_message_url != '':
            message = requests.utils.quote(raw_message)
            try:
                print('[INFO] Sending message')
                url = self.send_message_url % message
                r = requests.get(url, timeout=5)
                r.status_code
                return 0
            except:
                print('[ERROR] Send message failed')
                return 1


    def iaaa_login(self):
        p=webdriver.FirefoxOptions()
        p.set_headless()
        driver=webdriver.Firefox(firefox_options=p)
        driver.get('https://portal.pku.edu.cn/')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_name"))
        ).send_keys(self.username)

        driver.find_element_by_id('password').send_keys(self.password)
        # driver.find_element(by='id',value='password').send_keys(passwd)
        driver.find_element_by_id('logon_button').click()
        return driver

    def get_score(self):
        d=self.iaaa_login()
        try:
            d.get('https://portal.pku.edu.cn/portal2017/#/biz/myScore')
            # tmp=d.find_elements_by_class_name('row-border-table')
            tmp=WebDriverWait(d,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"row-border-table"))
            )
            # time.sleep(2)
            WebDriverWait(d,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'ng-scope'))
            )
            # for i in range(10):
            #     if(len(tmp)>1):
            #         break
            #     else:
            #         time.sleep(1)
            score=tmp[1].text
            score_list=score.split('\n')
            d.quit()
            no_new_score=True
            if score_list[0]=='课程名称 英文名称 课程类别 学分 成绩 绩点':
                print('[INFO] Get score successfully!')
                for i in score_list[1:]:
                    course_detail=i.split(' ')
                    course_name=course_detail[0]
                    course_score=course_detail[-2]
                    if course_detail[-1]=='W':#退课
                        course_score='W'
                    if course_name not in self.score_dict:
                        no_new_score=False
                        self.score_dict[course_name]=course_score
                        message=f"[INFO] 出成绩了!, {course_name}得分 {course_score}, 折合GPA {self.gpa(course_score)}"
                        print(message)
                        self.send_message(message)
                if(no_new_score):
                    print("[INFO] 没出新成绩!")
            else:
                print('[ERROR] Get score failed')
            d.quit()
        except:
            print("[ERROR] webdriver 出现了一些问题")
            self.driver_bug_count+=1
            if(self.driver_bug_count>10):
                self.send_message(f'[IMPORT ERROR] 出现了{self.driver_bug_count}次错误!!!!!!!!!!')
                print(f'[IMPORT ERROR] 出现了{self.driver_bug_count}次错误!!!!!!!!!!')
            d.quit()


    def loop(self):
        # self.read_config()
        while(1):
            print("[INFO] Start Loop ",self.loop_times)
            self.loop_times+=1
            self.get_score()
            print(f"[INFO] Sleep {self.sleep_time/60} min")
            time.sleep(self.sleep_time)




if __name__=="__main__":
    bot=Score_Bot()
    bot.read_config()
    bot.loop()
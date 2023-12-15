from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.errors import ElementNotFoundError
from datetime import datetime as dt
from time import sleep
from os import system

with open('setInfo.ini', 'r') as f:
    RATE = f.readline()[7:-1].strip()
    ID = f.readline()[5:-1].strip()
    PWD = f.readline()[11:].strip()


TARLIST = ['mp4', 'pdf', 'ppt', 'pptx']
system('cls')
print('--------------------------------------------------')
print('XiaoYa刷课自动化程序\n')
print('Python + DrissionPage')
print('支持Chrome内核浏览器, 如Chrome Edge等')
print('可自动完成本月中所有支持的任务')
print(f'目前支持的处理类型 >>> {TARLIST}\n')
print('可以在 setInfo.ini 文件中修改 [播放倍速] [登录ID] [登录密码]')
print('也可以不进行设置后续在命令行中根据提示输入(更为安全)')
print('--------------------------------------------------')
print('@Author  : Salnewt')
print('@Latest  : 2023-12-15')
print('\n')

# 播放倍速
if RATE == '':
    while True:
        try:
            RATE = int(float(input('设置播放倍速: ').strip()))
            break
        except ValueError:
            print('!!请正确输入倍速!!')
else:
    RATE = int(float(RATE))

print('\n')

if ID == '':
    ID = input('请输入登录账号: ').strip()
print('\n')
if PWD == '':
    from pwinput import pwinput
    PWD = pwinput(prompt='请输入密码: ', mask='·')

sleep(1)
system('cls')
print('--------------------------------------------------')
print('XiaoYa刷课自动化程序\n')
print('Python + DrissionPage')
print('支持Chrome内核浏览器, 如Chrome Edge等')
print('可自动完成本月中所有支持的任务')
print(f'目前支持的处理类型 >>> {TARLIST}\n')
print('任务过程中可通过 关闭网页 来结束任务\n')
print('--------------------------------------------------\n\n')
print('初始化完成!\n\n')

try:
    co = ChromiumOptions(ini_path='.\\configs.ini')
    co.mute(False)
    co.set_argument('--no-first-run')
    page = ChromiumPage(addr_driver_opts=co)
    sleep(0.5)
except FileNotFoundError:
    system('cls')
    print('--------------------------------------------------------------------------------')
    print('未找到浏览器，请修改浏览器配置文件<configs.ini>')
    print('将[chrome_options] -> binary_location 设置为您的chrome或edge浏览器')
    print('\n例如Edge浏览器可能的部分设置: \n')
    print('[chromium_options]\naddress = 127.0.0.1:9222\nbrowser_path = C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
    print('--------------------------------------------------------------------------------')
    print('')
    system('pause')
    exit()

try:
    page.set.window.max()

    page.get('https://ccnu.ai-augmented.com/app/jw-common/user/login')
    page.ele('.^ant-card')

    try:
        alert = page.ele('.ant-modal-body', timeout=1)
        alert.ele('tag:button').click()
    except ElementNotFoundError:
        pass

    page.ele('tx:统一').click()
    sleep(0.2)
    page.ele('.ant-select-selection-search').click()
    sleep(0.5)
    page.ele('@@class=ant-select-item-option-content@@text():武汉理工大学').click()
    sleep(0.2)
    page.ele('.btn-approve').click()

    try:
        page.wait.load_start()
        page.ele('tag:input@@type=text', timeout=2)
        sleep(0.2)
        page.ele('#un', timeout=0.5).input(ID)
        sleep(0.1)
        page.ele('#pd').input(PWD)
        sleep(0.1)
        page.ele('.login_box_landing_btn').click()
        sleep(0.5)
        if page.url[:24] == 'http://zhlgd.whut.edu.cn':
            print('账号或密码错误，请在浏览器中手动输入')
            page.wait.load_start(timeout=60)
    except Exception:
        pass

    page.ele('.aia_course_home_count_panel', timeout=10)
    sleep(0.5)
    page.ele('@@class=circle@@title^点击查看').click()
    sleep(1)
    table = page.ele('.xy-modal-content-warp')
    mission = table.eles('tag:sup@@class^ant-scroll-number')

    day = dt.now().day
    row = ''
    dayList = []

    for i in mission:
        target = i.prev('.^rc')
        target.click()
        selectDay = target.child().text

        # 排除过期任务
        if int(selectDay) < day:
            sleep(0.1)
            continue

        # 同周跳过
        temp = i.parent('tag:tr@@role=row').child().attr('title')
        if temp == row:
            continue
        else:
            row = temp

        dayList.append(selectDay)

    while len(dayList) != 0:
        td = dayList[0]
        table.ele(f'@@text()={td}@@class^rc-calendar').click()
        sleep(0.5)
        WorkList = table.ele('.ant-row')
        NoWork = True
        for c in WorkList.children():
            tarTime = dt.strptime(c.ele('.xy_taskCard_bottom').text, r'%Y-%m-%d %H:%M')
            title = c.ele('.group-resource-link').text
            type = title.split('.')[-1]
            if tarTime < dt.now():
                continue
            elif type not in TARLIST:
                continue
            else:
                NoWork = False
                print(f'当前任务: {tarTime} >> {title}')
                c.ele('.group-resource-link').click()
                page.wait.load_start()

                if type == 'mp4':
                    player = page.ele('.prism-player')
                    page.wait.ele_display(player.ele('.^prism-big-play-btn'))
                    sleep(0.5)
                    btn = player.ele('.^prism-big-play-btn')
                    btn.click()
                    sleep(0.5)
                    video = page.ele('tag:video')
                    video.run_js(f'this.playbackRate = {RATE}')

                    record = ''
                    while True:
                        process = page.ele('.progress_container').text[4:-1]
                        if process != record:
                            print(f'\r                                        ', end='')
                            print(f'\r执行进度: {process}%', end='')
                            record = process
                        if process == '100':
                            break
                        if btn.states.is_displayed:
                            btn.click()
                
                sleep(1)
                
                page.ele('.btn_content').click()
                print('\n任务结束\n')
                page.back()
                page.wait.load_start()
                sleep(1)
                page.ele('@@class=circle@@title^点击查看').click()
                sleep(1)
                table = page.ele('.xy-modal-content-warp')
                break

        if NoWork:
            dayList.pop(0)

    print('\n\n本月视频文档类任务已经全部完成! ')

except (KeyboardInterrupt, Exception) as e:
    print('')
    print('浏览器工作结束')
    print('若非预期的结束工作，可能由于浏览器初始化弹窗造成，重启解决')
finally:
    print('')
    system('pause')
    system('cls')
    try:
        page.quit()
    except Exception:
        pass
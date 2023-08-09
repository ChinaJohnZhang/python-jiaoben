import time
import json
import requests


def send_message(uid, content):
    print(f"Sending message to {uid}: {content}")  # 添加这行
    data = {
        'msg[sender_uid]': my_uid,
        'msg[receiver_id]': uid,
        'msg[receiver_type]': '1',
        'msg[msg_type]': '1',
        'msg[msg_status]': '0',
        'msg[content]': '{{"content":"{}"}}'.format(content),
        'msg[timestamp]': str(time.time())[:10],
        'msg[new_face_version]': '0',
        'msg[dev_id]': msg_id,
        'from_firework': '0',
        'build': '0',
        'mobi_app': 'web',
        'csrf_token': csrf,
        'csrf': csrf,
    }
    headers = {
        'cookie': cookie,
        'origin': 'https://message.bilibili.com',
        'referer': 'https://message.bilibili.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
    }
    url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'
    resp = requests.post(url, headers=headers, data=data).json()
    print(resp)
    if resp['code'] == 0:
        return True
    else:
        return False
    print(f"[DEBUG] Pretending to send message to {uid}: {content}")

last_check_timestamp = time.time()
def get_new_session():
    global last_check_timestamp
    begin_ts = str(time.time()).replace('.', '')[:-1]
    while True:
        params = {
            'begin_ts': begin_ts,
            'build': '0',
            'mobi_app': 'web',
        }
        headers = {
            'cookie': cookie,
            'origin': 'https://message.bilibili.com',
            'referer': 'https://message.bilibili.com/',
            'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
        }
        #get_new_follow()
        url = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/new_sessions?'
        resp = requests.get(url, headers=headers, params=params).json()
        session_list = resp['data']['session_list']
        
        if not session_list:
            time.sleep(4)
            continue
            
        for session in session_list:
            message_timestamp = session['last_msg']['timestamp']
            message_key = session['last_msg']['msg_key']
            if message_timestamp <= last_check_timestamp:
                continue  # 如果消息是在上次检查之前发送的，就跳过
            uid = session['talker_id']
            begin_ts = session['session_ts']
            message = json.loads(session['last_msg']['content'])['content']
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(message_timestamp))
            sender = uid
            if uid == my_uid:
                sender = 'Me'
            log = 'Time: {}\nMessage_key: {}\nSender: {}\nMessage: {}\n\n'.format(time_, message_key, sender, message)
            print(log)
            
            # 在这里，你可以添加一个条件来检查是否需要回复这个消息
            if uid != my_uid and message_key not in msg_key_list:
                send_message(uid=uid, content=first_follow_message)
                msg_key_list.append(message_key) 
            
        last_check_timestamp = time.time()  # 更新上次检查的时间戳
        time.sleep(4)

def get_new_follow():
    params = {
        'vmid': my_uid,
        'pn': '1',
        'ps': '100',
        'order': 'desc',
        'order_type': 'attention',
        'jsonp': 'jsonp',
    }
    headers = {
        'cookie': cookie,
        'origin': 'https://message.bilibili.com',
        'referer': 'https://message.bilibili.com/',
        'user-agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/96.0.4664.110Safari/537.36Edg/96.0.1054.62',
    }
    url = 'https://api.bilibili.com/x/relation/followers?'
    resp = requests.get(url, headers=headers, params=params).json()
    follow_li = resp['data']['list']
    for follow in follow_li:
        mid = str(follow['mid'])
        if mid not in follow_list:
            send_message(mid, content=first_follow_message)
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print('UID: {} -*- Time: {} -*- Send: 欢迎关注'.format(mid, time_))
            with open('C:\\UnityProgram\\python-jiaoben\\B站相关\\B站私信回复\\信息储存\\关注我的.txt', 'a')as f:
                f.write('{}-'.format(mid))
            follow_list.append(mid)
            time.sleep(0.3)


my_uid = '3493260838308803' #3493260838308803
csrf = 'cc7e551f6094f0c649daaf0e678d5292'#  cc7e551f6094f0c649daaf0e678d5292
msg_id = 'cc7e551f6094f0c649daaf0e678d5292'

cookie = open('C:\\UnityProgram\\python-jiaoben\\B站相关\\B站私信回复\\信息储存\\Cookie.txt', 'r').read()
file_1 = open('C:\\UnityProgram\\python-jiaoben\\B站相关\\B站私信回复\\信息储存\\已读消息.txt', 'r').read()
file_2 = open('C:\\UnityProgram\\python-jiaoben\\B站相关\\B站私信回复\\信息储存\\关注我的.txt', 'r').read()

msg_key_list = file_1.split('-')
follow_list = file_2.split('-')

first_follow_message = '‍新地址：https://chat.gpt200.cn \\n电脑/手机浏览器打开就能使用，不需要魔法，打不开可以尝试更换浏览器，或者加V：Reader_Han \\n邀请码写 102744 （可以多获得10000Token）\\n准备好接收你的AI女友吧'

print('---开始运行----')
get_new_session()
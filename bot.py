import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import random
import os

import json
import datetime

# на будущее возможно никогда на наступившее
# from vk_api.longpoll import VkEventType
# import requests


# configuration operations
def load_config():
    with open('config.json') as file:
        file_data = json.load(file)
    return file_data


def save_config(data):
    with open('config.json') as file:
        json.dump(data, file)


# writing event log
def wLog(*data, log_path):
    with open(log_path, 'a+', encoding='utf_8') as f:
        f.write('{} - {}\n'.format(str(datetime.datetime.now()), str(data)))
    return data


def send_admin_msg(msg):
    send_msg(load_config()["admin_id"], msg)


def send_msg(reply_to_id, msg):
    """
        кто peer_id
            group_id='68239915'
        кому user_id
        текст message
        случайный набор random_id
    """
    try:
        session_api.messages.send(
            peer_id=reply_to_id,
            random_id=random.randint(1, 10 ** 5),
            message=msg,
            group_id=load_config()["group_id"])
    except Exception as excp:
        print(wLog(type(excp), log_path=log_path))


def main(config_data):
    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_REPLY:
            # wLog(event.type, name=log_path)
            wLog(event.obj, log_path=log_path)
            send_admin_msg(msg=f"{event.obj}")
            # print(event)

        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message

            print(f"user: {message['peer_id']}\n",
                  f"text: {message['text']}")
            print(int(config_data['default_group_id']))

            if int(message['peer_id']) >= int(config_data['default_group_id']):
                if 'начать' in message['text'].lower():
                    send_msg(reply_to_id=message['peer_id'],
                             msg=(f"вот то, что я умею:\n"
                                  "'начать' - я пишу начальную помощь\n"
                                  "'кубик' - я пишу число от 0 до твоего числа\n"
                                  "'/nr' - установлю твою роль в чате"
                                  " это сможет делать только создатель чата(пока не работает)\n"
                                  "'/whoami' - напомню тебе твою роль в чате(пока не работает)\n"
                                  "'/r' - напомню все роли в чате(пока не работает)\n"
                                  "\n"
                                  "соглашаясь на мои скромные "
                                  "услуги вы понимаете, что я был создан само-криво-учкой.\n"
                                  "ах да, самое главное - что бы я тебе ответил тебе нужно меня пнуть :)\n"
                                  "* или @ и выбери из выпавшего списка и напиши свое желание\n"
                                  "писать в личку конечно мне можно но это только в том случае, "
                                  "если ты любишь играть волейбол со стеной. возможно ты знаешь в этом толк"))

                elif 'кубик' in message['text'].lower():
                    try:
                        max_val = int(message['text'].split(' ')[1])
                    except Exception:
                        max_val = 100

                    send_msg(reply_to_id=message['peer_id'],
                             msg=f"Случайное число от 1 до {max_val}\n{random.randint(0, max_val)}")

                elif '/bb ' in message['text'].lower():
                    for i in range(5):
                        send_msg(reply_to_id=message['peer_id'],
                                 msg=f"[id{message['text'].split(' ')[1].split('|')[0][3:]}|Вас] звали!")

                elif '/nr ' in message['text'].lower():
                    """todo:change your roles"""
                    print('nr')
                    pass

                elif '/whoami' in message['text'].lower():
                    """todo: send your roles"""
                    print('nr')
                    pass

                elif '/r ' in message['text'].lower():
                    print('working..')
                    pass
                    # todo: send all roles
                    # user_id = '1'
                    # user_role = '1'
                    # set_settings[message['peer_id']]['users'][user_id] = user_role

                    # for i in settg:
                    #     print(settg[i])

            elif int(message['peer_id']) < config_data['default_group_id']:
                # just repeeating the income message
                send_msg(reply_to_id=message['peer_id'],
                         msg=f"давай поиграем в попугая :D\n{message['text']}")

                print(f"user: {message['peer_id']}\n",
                      f"text: {message['text']}")


# loging preinstalls
today = datetime.datetime.today()
log_path = f'{os.path.dirname(__file__)}{os.sep}logs{os.sep}{str(datetime.datetime.today()).split(" ")[0]}_vk_bot_log'
print('editing log at: ' + log_path)

# config preinstalls
config = load_config()

# bot preinstalls
vk_session = vk_api.VkApi(token=config["token"])
longpoll = VkBotLongPoll(vk_session, config["group_id"])
session_api = vk_session.get_api()
send_admin_msg('i woke up')

if __name__ == '__main__':
    main(config)

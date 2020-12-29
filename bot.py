import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import random
import datetime
import os


# на будущее
# from vk_api.longpoll import VkEventType
# import requests
# import json


def send_msg_to_user(msg):
    try:
        session_api.messages.send(peer_id='608258212',
                                  random_id=random.randint(1, 10 ** 5),
                                  message=f'text: {msg}',
                                  group_id='68239915')

    except Exception as exp:
        print(wLog(type(exp)))


def get_settings_for_chat():
    global session_api
    # start_message_id='0',
    #     group_id='68239915',

    return session_api.messages.getHistory(
        offset='0',
        user_id='227027256',
        peer_id='2000000151',
        rev='0',
        count='200'
    )


# def set_settings_for_chat():
#     print(session_api.messages)
#     pass


def wLog(*data):
    global name
    with open(name, 'a+', encoding='utf_8') as f:
        f.write('{} - {}\n'.format(str(datetime.datetime.now()), str(data)))
    return data


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
            group_id='68239915')
    except Exception as exp:
        print(wLog(type(exp)))


def main():
    global rules
    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_REPLY:
            wLog(event.type)
            wLog(event.obj)
            send_msg_to_user(msg=f"{event.obj}")

        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message

            print(f"user: {message['peer_id']}\n",
                  f"text: {message['text']}")

            if '200000000' in str(message['peer_id']):
                if 'начать' in message['text'].lower():
                    send_msg(reply_to_id=message['peer_id'],
                             msg=(f"вот что я умею:\n"
                                  "'начать' - я пишу начальную помощь\n"
                                  "'/d' - я пишу число от 0 до твоего числа\n"
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

                elif '/d ' in message['text'].lower():
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
                    # todo: send your roles
                    pass

                elif '/whoami' in message['text'].lower():
                    # todo: send your roles
                    pass

                elif '/r ' in message['text'].lower():
                    # todo: send all roles
                    print('working..')
                    for i in get_settings_for_chat():

                        print(get_settings_for_chat()[i])

            elif '200000000' not in str(message['peer_id']):
                send_msg(reply_to_id=message['peer_id'],
                         msg=f"давай поиграем в попугая :D\n{message['text']}")

                print(f"user: {message['peer_id']}\n",
                      f"text: {message['text']}")


token = "12cb2fe1cd67f00bf8fee625fe583de280a908467efdd9ef7108f4c1f2a1b9282784467c77e336e96b431"
group_id = '68239915'

today = datetime.datetime.today()
name = f'{os.path.dirname(__file__)}{os.sep}vk_bot_log'
print('editing log at: ' + name)

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id)
session_api = vk_session.get_api()

rules = {}


if __name__ == '__main__':
    main()

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime
import os

# на будущее
# from vk_api.longpoll import VkEventType
# import requests
# import json


def send_msg_to_loguser(reply_from_id, user_from_id, msg):
    try:
        session_api.messages.send(
            peer_id='608258212',
            random_id=random.randint(1, 10 ** 5),
            message=f'chat:{reply_from_id}\n\
                      user: @id{user_from_id} ({user_from_id})\n\
                      text: {msg}',
            group_id='68239915')

    except Exception:
        pass


def wLog(*data):
    with open(name, 'a+', encoding='utf_8') as f:
        f.write('{} - {}\n'.format(str(datetime.datetime.now()), str(data)))
    # send_msg_to_loguser(str(data), 'dsa')
    return data


def send_msg(reply_to_id, msg):
    """
        кто peer_id
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


token = "12cb2fe1cd67f00bf8fee625fe583de280a908467efdd9ef7108f4c1f2a1b9282784467c77e336e96b431"
group_id = '68239915'

global today, currentPath, session_api, name, event

today = datetime.datetime.today()
currentPath = str(os.path.dirname(__file__))
name = r'{}{}vk_bot_log'.format(currentPath, os.sep)
print('editing log at: ' + name)

vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id)
session_api = vk_session.get_api()

for event in longpoll.listen():
    # print(wLog(event.type))
    if event.type == VkBotEventType.MESSAGE_NEW:
        wLog(event.type)
        wLog(event.obj)
        print(f"user: {event.obj.message['peer_id']}\n",
              f"text: {event.obj.message['text']}")
        send_msg_to_loguser(reply_from_id=event.obj.message['peer_id'],
                            user_from_id=event.obj.message['from_id'],
                            msg=f"{event.obj.message['text']}")

        send_msg_to_loguser(reply_from_id=event.obj.message['peer_id'],
                            user_from_id=event.obj.message['from_id'],
                            msg=f"{event.obj.message['text']}")

        if '200000000' in str(event.obj.message['peer_id']) and '[club68239915|' in event.obj.message['text']:
            send_msg(reply_to_id=event.obj.message['peer_id'],
                     msg="Вы [club68239915|меня] звали, Мой сладкий пирожочек?")

            send_msg_to_loguser(reply_from_id=event.obj.message['peer_id'],
                                user_from_id=event.obj.message['from_id'],
                                msg=f"{event.obj.message['text']}")

            if 'начать' in event.obj.message['text'].lower():
                send_msg(reply_to_id=event.obj.message['peer_id'],
                         msg=(f"вот что я умею:\n"
                              "'начать' - я пишу начальную помощь\n"
                              "'кости' - я пишу число от 0 до 100\n"
                              "'назначить' - установлю твою роль в чате"
                              " это сможет делать только создатель чата(пока не работает)\n"
                              "'кто я' - напомню тебе твою роль в чате(пока не работает)\n"
                              "'роли' - напомню все роли в чате(пока не работает)\n"
                              "\n"
                              "соглашаясь на мои скромные "
                              "услуги вы понимаете, что я был создан само-криво-учкой.\n"
                              "ах да, самое главное - что бы я тебе ответил тебе нужно меня пнуть :)\n"
                              "* или @ и выбери из выпавшего списка и напиши свое желание\n"
                              "писать в личку конечно мне можно но это только в том случае, "
                              "если ты любишь играть волейбол со стеной. возможно ты знаешь в этом толк"))

            elif 'кости' in event.obj.message['text'].lower():
                send_msg(reply_to_id=event.obj.message['peer_id'],
                         msg=f"Кости брошены!\n{random.randint(0, 100)}")

            elif 'назначить' in event.obj.message['text'].lower():
                pass

            elif 'роли' in event.obj.message['text'].lower():
                pass

            elif 'кто я' in event.obj.message['text'].lower():
                pass

        elif '200000000' not in str(event.obj.message['peer_id']):
            send_msg(reply_to_id=event.obj.message['peer_id'],
                     msg=f"давай поиграем в попугая :D\n{event.obj.message['text']}")

            print(f"user: {event.obj.message['peer_id']}\n",
                  f"text: {event.obj.message['text']}")

# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.ttypes import Message
from LineAlpha.TalkService import Client
import time, datetime, random ,sys, re, string, os, json, codecs
reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin()
print client._loginresult()
print client._client.reissueUserTicket(0,3)

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
    	if 0 == msg.contentType:
            if msg.text == "/さようなら":
                client.leaveGroup(msg.to)
            elif msg.text:
                sendMessage(msg.to, msg.text)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print error
tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
    	client.acceptGroupInvitation(op.param1)

    except Exception as e:
    	print e
tracer.addOpInterrupt(13, NOTIFIED_INVITE_INTO_GROUP)


while True:
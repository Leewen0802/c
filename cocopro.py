# -*- coding: utf-8 -*-
from linepy import *
from akad.ttypes import Message
from datetime import datetime
import json,sys,atexit,time,codecs,timeit
botStart = time.time()
cl = LINE("mail","passwd")
channelToken = cl.getChannelResult()
print ("======登入成功=====")
oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
clMID = cl.profile.mid
KAC=[cl]
admin=['u28d781fa3ba9783fd5144390352b0c24',clMID]
msg_dict = {}
bl = [""]
def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def helpmessage():
    helpMessage = """
        ╔═══════════
        ╠♥ ✿ CoCo指令表 ✿ ♥
        ╠➥ 「查看指令」查看全部指令
        ╠➥ 「黑單 @」標記加入黑單
        ╠➥ 「解黑 @」標記解除黑單
        ╠➥ 「查看黑名單」查看被黑單的人
        ╠➥ 「踢出黑單」踢出群組裡的黑單
        ╠➥ 「測試速度」查看機器速度
        ╠➥ 「設定:確認」查看機器目前設定
        ╠➥ 「自動入群開啟/關閉」機器自動進群開啟/關閉
        ╠➥ 「邀請保護開啟/關閉」群組邀請保護開啟/關閉
        ╠➥ 「網址保護開啟/關閉」群組網址保護開啟/關閉
        ╠➥ 「群組保護開啟/關閉」群組保護開啟/關閉
        ╚═〘 Credits By: ©CoCo™  〙
        """
    return helpMessage
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 11:
            group = cl.getGroup(op.param1)
            contact = cl.getContact(op.param2)
            if settings["qrprotect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
                    invsend = 0
                    cl.sendMessage(op.param1,cl.getContact(op.param2).displayName + "不要打開群組網址")
                    cl.kickoutFromGroup(op.param1,[op.param2])
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            print ("[ 13 ] 通知邀請群組: " + str(group.name) + "\n邀請者: " + contact1.displayName + "\n被邀請者" + contact2.displayName)
            if settings["inviteprotect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    cl.cancelGroupInvitation(op.param1,[op.param3])
            if settings["autoJoin"] == True:
                if op.param2 in admin:
                    print ("進入群組: " + str(group.name))
                    cl.acceptGroupInvitation(op.param1)
                pass
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) +"\n踢人者: " + contact1.displayName + "\nMid: " + contact1.mid + "\n被踢者" + contact2.displayName + "\nMid:" + contact2.mid )
            if settings["protect"] == True:
                if op.param2 in admin:
                    pass
                else:
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    settings["blacklist"][op.param2] = True
        if op.type == 24:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 25 or op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in admin:
                if msg.text in ["查看指令"]:
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                    cl.sendContact(to, "u28d781fa3ba9783fd5144390352b0c24")
                elif "黑單 @" in msg.text:
                    if msg.toType == 2:
                        _name = msg.text.replace("黑單 @","")
                        _nametarget = _name.rstrip('  ')
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _nametarget == g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    settings["blacklist"][target] = True
                                    cl.sendMessage(msg.to,"已加入黑名單")
                                except:
                                    pass
                elif "解黑 @" in msg.text:
                    if msg.toType == 2:
                        _name = msg.text.replace("解黑 @","")
                        _nametarget = _name.rstrip('  ')
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _nametarget == g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            pass
                        else:
                            for target in targets:
                                try:
                                    del settings["blacklist"][target]
                                    cl.sendMessage(to, "已解除黑名單")
                                except:
                                    pass
                elif msg.text in ["查看黑單"]:
                    if settings["blacklist"] == {}:
                        cl.sendMessage(to, "沒有黑名單")
                    else:
                        cl.sendMessage(to, "以下是黑名單")
                        mc = ""
                        for mi_d in settings["blacklist"]:
                            mc += "->" + cl.getContact(mi_d).displayName + "\n"
                        cl.sendMessage(to, mc)
                elif msg.text in ["踢出黑單"]:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                        for tag in settings["blacklist"]:
                            matched_list+=filter(lambda str: str == tag, gMembMids)
                        if matched_list == []:
                            print ("1")
                            cl.sendMessage(to, "沒有黑名單")
                            return
                        for jj in matched_list:
                            cl.kickoutFromGroup(to, [jj])
                            cl.sendMessage(to, "黑名單以踢除")
                elif msg.text in ["測試速度"]:
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    start = time.time()
                    cl.sendMessage(to,'處理速度\n' + str1 + '秒')
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,'指令反應\n' + format(str(elapsed_time)) + '秒')
                elif msg.text in ["設定:確認"]:
                    try:
                        ret_ = "╔══[ 設定 ]"
                        if settings["autoJoin"] == True: ret_ += "\n╠ 自動加入群組 ✅"
                        else: ret_ += "\n╠ 自動加入群組 ❌"
                        if settings["inviteprotect"] == True: ret_ += "\n╠ 邀請保護 ✅"
                        else: ret_ += "\n╠ 邀請保護 ❌"
                        if settings["qrprotect"] == True: ret_ += "\n╠ 網址保護 ✅"
                        else: ret_ += "\n╠ 網址保護 ❌"
                        if settings["protect"] == True: ret_ += "\n╠ 群組保護 ✅"
                        else: ret_ += "\n╠ 群組保護 ❌"
                        ret_ += "\n╚══[ 設定 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif msg.text in ["自動入群開啟"]:
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動加入群組已開啟")
                elif msg.text in ["自動入群關閉"]:
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動加入群組已關閉")
                elif msg.text in ["邀請保護開啟"]:
                    settings["inviteprotect"] = True
                    cl.sendMessage(to, "群組邀請保護已開啟")
                elif msg.text in ["邀請保護關閉"]:
                    settings["inviteprotect"] = False
                    cl.sendMessage(to, "群組邀請保護已關閉")
                elif msg.text in ["網址保護開啟"]:
                    settings["qrprotect"] = True
                    cl.sendMessage(to, "群組網址保護已開啟")
                elif msg.text in ["網址保護關閉"]:
                    settings["qrprotect"] = False
                    cl.sendMessage(to, "群組網址保護已關閉")
                elif msg.text in ["群組保護開啟"]:
                    settings["protect"] = True
                    cl.sendMessage(to, "群組保護已開啟")
                elif msg.text in ["群組保護關閉"]:
                    settings["protect"] = False
                    cl.sendMessage(to, "群組保護已關閉")
            elif msg.contentType == 13:
                if settings["contact"] == True:
                    msg.contentType = 0
                    if 'displayName' in msg.contentMetadata:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                            cl.sendMessage(msg.to,"[顯示名稱]:\n" + msg.contentMetadata["顯示名稱"] + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[狀態消息]:\n" + contact.statusMessage + "\n[圖片網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
                    else:
                        contact = cl.getContact(msg.contentMetadata["mid"])
                        try:
                            cu = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                        except:
                            cu = ""
                        cl.sendMessage(msg.to,"[顯示名稱]:\n" + contact.displayName + "\n[mid]:\n" + msg.contentMetadata["mid"] + "\n[狀態消息]:\n" + contact.statusMessage + "\n[圖片網址]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[封面網址]:\n" + str(cu))
        if op.type == 26:
            try:
                msg = op.message
                if msg.toType == 0:
                    cl.log("[%s]"%(msg._from)+msg.text)
                else:
                    cl.log("[%s]"%(msg.to)+msg.text)
                if msg.contentType == 0:
                    msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":msg.createdTime}
            except Exception as e:
                print(e)
        if op.type == 65:
            try:
                at = op.param1
                msg_id = op.param2
                if msg_id in msg_dict:
                    if msg_dict[msg_id]["from"] not in bl:
                        cl.sendMessage(at,"[收回訊息者]\n%s\n[訊息內容]\n%s"%(cl.getContact(msg_dict[msg_id]["from"]).displayName,msg_dict[msg_id]["text"]))
                    del msg_dict[msg_id]
            except Exception as e:
                print(e)
    except Exception as error:
        logError(error)
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)

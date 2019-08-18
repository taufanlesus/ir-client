from linepy import *
from akad.ttypes import *
from datetime import datetime, timedelta, date
import time, asyncio, json, threading, codecs, sys, os, re, urllib, requests, html5lib, timeit, pytz
from bs4 import BeautifulSoup

def waktu(secs):
    mins, secs  = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '%02d Hari %02d Jam %02d Menit %02d Detik' % (days, hours, mins, secs)

class RAFAMILY(object):
    
    def __init__(self, resp, authQR=None):
        self.resp = resp
        self.resp = self.resp+' '
        self.authQR = authQR
        self.login(authQR)
        self.fetch()
        
    def login(self, auth):
        if auth == None:
            self.client = LINE()
        else:
            self.client = LINE(idOrAuthToken=auth)
        self.client.log("Auth Token : " + str(self.client.authToken))
        self.mid = self.client.getProfile().mid
        with open("penyimpanan.json","r") as account:
            self.wait = json.load(account)
        
    def fetch(self):
        while True:
            try:
                self.operations = self.client.poll.fetchOperations(self.client.revision, 10)
                for op in self.operations:
                    if (op.type != OpType.END_OF_OPERATION):
                        self.client.revision = max(self.client.revision, op.revision)
                        self.bot(op)
            except Exception:
                pass
    
    def bot(self, op):
        ketua   = self.client
        setmain = self.wait
        try:
            if op.type == 0:
                return
            if op.type == 5:
                if op.param1 in setmain["list"]["bot"]:
                    ketua.findAndAddContactsByMid(op.param1)
                    ketua.sendMention(op.param1,"@!sudah aku addback\nHanya (OWNER ADMIN STAFF) yang bisa invite saya ke room\nSupport my channel\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA","http://dl.profile.line-cdn.net/{}".format(str(ketua.getContact("u7b7156567827616ebd35687e96990e95").pictureStatus)),"http://line.me/ti/p/~dewatuak","OWNER BOT SILENT-VERSION",[op.param1])
                else:
                    ketua.sendMention(op.param1,"@!sudah aku addback\nHanya (OWNER ADMIN STAFF) yang bisa invite saya ke room\nSupport my channel\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA","http://dl.profile.line-cdn.net/{}".format(str(ketua.getContact("u7b7156567827616ebd35687e96990e95").pictureStatus)),"http://line.me/ti/p/~dewatuak","OWNER BOT SILENT-VERSION",[op.param1])
            if op.type == 11:
                if op.param1 in setmain["protect"]["linkqr"]:
                    if ketua.getGroup(op.param1).preventedJoinByTicket == True:
                        if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                            ketua.reissueGroupTicket(op.param1)
                            X = ketua.getGroup(op.param1)
                            X.preventedJoinByTicket = True
                            ketua.updateGroup(X)
                            ketua.kickoutFromGroup(op.param1,[op.param2])
                            time.sleep(0.001)
                
                if op.param2 in setmain["list"]["blacklist"]:
                    if ketua.getGroup(op.param1).preventedJoinByTicket == False:
                        if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                            ketua.reissueGroupTicket(op.param1)
                            X = ketua.getGroup(op.param1)
                            X.preventedJoinByTicket = True
                            ketua.updateGroup(X)
                            ketua.kickoutFromGroup(op.param1,[op.param2])
                            time.sleep(0.001)
                            
            if op.type == 13:
                if self.mid in op.param3:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["bot"]:
                        ketua.acceptGroupInvitation(op.param1)
                        ketua.sendMention(op.param1,"@!tidak dapat menginvite bot",'http://dl.profile.line-cdn.net/{}'.format(str(ketua.getContact(op.param2).pictureStatus)),'','Akses ditolak dalam hal ini',[op.param2])
                        ketua.leaveGroup(op.param1)
                    else:
                        ketua.acceptGroupInvitation(op.param1)
                        time.sleep(0.001)
                
            if op.type == 13:
                if op.param2 in setmain["list"]["blacklist"]:
                    a = ketua.getGroup(op.param1)
                    if a.invitee is not None:
                        b = [contact.mid for contact in a.invitee]
                        for target in b:
                            if target in op.param3:
                                ketua.cancelGroupInvitation(op.param1,[target])
                                time.sleep(0.001)
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        time.sleep(0.001)
                        
                if op.param3 in setmain["list"]["blacklist"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                        a = ketua.getGroup(op.param1)
                        if a.invitee is not None:
                            b = [contact.mid for contact in a.invitee]
                            for target in b:
                                if target in setmain["list"]["blacklist"]:
                                    ketua.cancelGroupInvitation(op.param1,[target])
                                    time.sleep(0.001)
                            ketua.kickoutFromGroup(op.param1,[op.param2])
                            time.sleep(0.001)
                            setmain["list"]["blacklist"][op.param2] = True
                            f = codecs.open("penyimpanan.json","w","utf-8")
                            json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                    else:
                        a = ketua.getGroup(op.param1)
                        if a.invitee is not None:
                            b = [contact.mid for contact in a.invitee]
                            for target in b:
                                if target in setmain["list"]["blacklist"]:
                                    ketua.cancelGroupInvitation(op.param1,[target])
                                    time.sleep(0.001)
                            ketua.sendMention(op.param1,"Maaf den @!,kita cancel karena ada diblacklist",'http://dl.profile.line-cdn.net/{}'.format(str(ketua.getContact(op.param2).pictureStatus)),'','Akses ditolak dalam hal ini',[op.param2])
                            
                if op.param1 in setmain["protect"]["invite"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                        a = ketua.getGroup(op.param1)
                        if a.invitee is not None:
                            b = [contact.mid for contact in a.invitee]
                            for target in b:
                                if target in op.param3:
                                    ketua.cancelGroupInvitation(op.param1,[target])
                                    time.sleep(0.001)
                            ketua.kickoutFromGroup(op.param1,[op.param2])
                            time.sleep(0.001)
                            setmain["list"]["blacklist"][op.param2] = True
                            f = codecs.open("penyimpanan.json","w","utf-8")
                            json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                            
            if op.type == 17:
                if op.param2 in setmain["list"]["blacklist"]:
                    ketua.kickoutFromGroup(op.param1,[op.param2])
                    time.sleep(0.001)
            
            if op.type == 19:
                if op.param1 in setmain["protect"]["kick"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        setmain["list"]["blacklist"][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                        if op.param3 not in setmain["list"]["blacklist"]:
                            try:
                                ketua.findAndAddContactsByMid(op.param3)
                                time.sleep(0.001)
                                ketua.inviteIntoGroup(op.param1,[op.param3])
                                time.sleep(0.001)
                            except:
                                ketua.inviteIntoGroup(op.param1,[op.param3])
                                time.sleep(0.001)
                        else:
                            ketua.sendMention(op.param1,"Maaf den @!tidak bisa aku invite karena ada didalam blacklist",'http://dl.profile.line-cdn.net/{}'.format(str(ketua.getContact(op.param3).pictureStatus)),'','Akses ditolak dalam hal ini',[op.param3])
                
                if op.param3 in setmain["list"]["superadmin"] and op.param3 in setmain["list"]["admin"] and op.param3 in setmain["list"]["staff"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                        try:
                            ketua.findAndAddContactsByMid(op.param3)
                            time.sleep(0.001)
                            ketua.inviteIntoGroup(op.param1,[op.param3])
                            time.sleep(0.001)
                        except:
                            ketua.inviteIntoGroup(op.param1,[op.param3])
                            time.sleep(0.001)
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        time.sleep(0.001)
                        setmain["list"]["blacklist"][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                
                if op.param3 in setmain["list"]["bot"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"]:
                        ketua.inviteIntoGroup(op.param1,[op.param3])
                        setmain["list"]["blacklist"][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        time.sleep(0.001)
            
            if op.type == 22:
                if self.mid in op.param3:
                    ketua.leaveRoom(op.param1)
            
            if op.type == 32:
                if op.param1 in setmain["protect"]["cancel"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"] and op.param2 not in setmain["list"]["bot"]:
                        setmain["list"]["blacklist"][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        time.sleep(0.001)
                        if op.param3 not in setmain["list"]["blacklist"]:
                            try:
                                ketua.findAndAddContactsByMid(op.param3)
                                time.sleep(0.001)
                                ketua.inviteIntoGroup(op.param1,[op.param3])
                                time.sleep(0.001)
                            except:
                                ketua.inviteIntoGroup(op.param1,[op.param3])
                                time.sleep(0.001)
                        else:
                            ketua.sendMention(op.param1,"Maaf @!tidak bisa aku invite karena ada didalam blacklist",'http://dl.profile.line-cdn.net/{}'.format(str(ketua.getContact(op.param3).pictureStatus)),'','Akses ditolak dalam hal ini',[op.param3])
                            
                if op.param3 in setmain["list"]["bot"]:
                    if op.param2 not in setmain["list"]["superadmin"] and op.param2 not in setmain["list"]["admin"] and op.param2 not in setmain["list"]["staff"]:
                        ketua.inviteIntoGroup(op.param1,[op.param3])
                        setmain["list"]["blacklist"][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                        ketua.kickoutFromGroup(op.param1,[op.param2])
                        time.sleep(0.001)
            
            if op.type == 46:
                if op.param2 in setmain["list"]["bot"]:
                    ketua.removeAllMessages()
                    
            if op.type == 55:
                if op.param1 in setmain["readpoint"]:
                    if op.param2 not in setmain["readmember"][op.param1]:
                        setmain["readmember"][op.param1][op.param2] = True
                        f = codecs.open("penyimpanan.json","w","utf-8")
                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
            
            if op.type == 26:
                msg  = op.message
                text = msg.text
                if msg.toType == 2:
                    if msg.contentType == 1:
                        if msg._from in setmain["list"]["superadmin"]:
                            if self.mid in setmain["pengaturan"]["fotoku"]:
                                path = ketua.downloadObjectMsg(msg.id)
                                ketua.updateProfilePicture(path)
                                ketua.sendMessage(msg.to,"Foto {} berhasil diubah".format(str(ketua.getContact(self.mid).displayName)))
                                del setmain["pengaturan"]["fotoku"][self.mid]
                                f = codecs.open("penyimpanan.json","w","utf-8")
                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                            if msg.to in setmain["pengaturan"]["fotoku"]:
                                path = ketua.downloadObjectMsg(msg.id)
                                ketua.updateProfilePicture(path)
                                ketua.sendMessage(msg.to,"Semua Foto bot berhasil diubah")
                                del setmain["pengaturan"]["fotoku"][msg.to]
                                f = codecs.open("penyimpanan.json","w","utf-8")
                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                        if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                            if msg.to in setmain["pengaturan"]["fotogr"]:
                                path = ketua.downloadObjectMsg(msg.id)
                                ketua.updateGroupPicture(msg.to, path)
                                ketua.sendMessage(msg.to,"Foto group berhasil diubah")
                                del setmain["pengaturan"]["fotogr"][msg.to]
                                f = codecs.open("penyimpanan.json","w","utf-8")
                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                    if msg.contentType == 13:
                        if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                            if msg.to in setmain["kirimkontak"]["switchbl"]:
                                if msg.contentMetadata["mid"] in setmain["list"]["blacklist"]:
                                    ketua.sendMessage(msg.to,"{} sudah ada didalam blacklist".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    setmain["list"]["blacklist"][msg.contentMetadata["mid"]] = True
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} masuk ke dalam blacklist".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchubl"]:
                                if msg.contentMetadata["mid"] not in setmain["list"]["blacklist"]:
                                    ketua.sendMessage(msg.to,"{} belum ada didalam blacklist".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    del setmain["list"]["blacklist"][msg.contentMetadata["mid"]]
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} terhapus dari blacklist".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                        if msg._from in setmain["list"]["superadmin"]:
                            if msg.to in setmain["kirimkontak"]["switchsadmin"]:
                                if msg.contentMetadata["mid"] in setmain["list"]["superadmin"]:
                                    ketua.sendMessage(msg.to,"{} sudah menjadi super admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    setmain["list"]["superadmin"][msg.contentMetadata["mid"]] = True
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} diangkat menjadi super admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchusadmin"]:
                                if msg.contentMetadata["mid"] not in setmain["list"]["superadmin"]:
                                    ketua.sendMessage(msg.to,"{} tidak pernah menjadi super admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    del setmain["list"]["superadmin"][msg.contentMetadata["mid"]]
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} dicopot dari super admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchadmin"]:
                                if msg.contentMetadata["mid"] in setmain["list"]["admin"]:
                                    ketua.sendMessage(msg.to,"{} sudah menjadi admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    setmain["list"]["admin"][msg.contentMetadata["mid"]] = True
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} diangkat menjadi admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchuadmin"]:
                                if msg.contentMetadata["mid"] not in setmain["list"]["admin"]:
                                    ketua.sendMessage(msg.to,"{} tidak pernah menjadi admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    del setmain["list"]["admin"][msg.contentMetadata["mid"]]
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} dicopot dari admin".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchstaff"]:
                                if msg.contentMetadata["mid"] in setmain["list"]["staff"]:
                                    ketua.sendMessage(msg.to,"{} sudah menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    setmain["list"]["staff"][msg.contentMetadata["mid"]] = True
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} diangkat menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchustaff"]:
                                if msg.contentMetadata["mid"] not in setmain["list"]["staff"]:
                                    ketua.sendMessage(msg.to,"{} tidak pernah menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    del setmain["list"]["staff"][msg.contentMetadata["mid"]]
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} dicopot dari staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                        if msg._from in setmain["list"]["admin"]:
                            if msg.to in setmain["kirimkontak"]["switchstaff"]:
                                if msg.contentMetadata["mid"] in setmain["list"]["staff"]:
                                    ketua.sendMessage(msg.to,"{} sudah menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    setmain["list"]["staff"][msg.contentMetadata["mid"]] = True
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} diangkat menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                            if msg.to in setmain["kirimkontak"]["switchustaff"]:
                                if msg.contentMetadata["mid"] not in setmain["list"]["staff"]:
                                    ketua.sendMessage(msg.to,"{} tidak pernah menjadi staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                                else:
                                    del setmain["list"]["staff"][msg.contentMetadata["mid"]]
                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                    ketua.sendMessage(msg.to,"{} dicopot dari staff".format(str(ketua.getContact(msg.contentMetadata["mid"]).displayName)))
                    if msg.contentType == 0:
                        #ketua.sendChatChecked(msg.to, msg.id)
                        if text is None:
                            return
                        else:
                            try:
                                if text.lower() == self.resp +"menu":
                                    a = " ●❀ {} ❀●\n╔───────────────── \n".format(str(setmain["pengaturan"]["Team"]))
                                    if msg._from in setmain["list"]["superadmin"]:
                                        a += "│❈ {} absen\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} spbot\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} ubah [nama/bio/setkey/team],[teks]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} botpp\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bot out\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} teambot\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} delbot\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} keluargc [nama grup]\n".format(str(setmain["pengaturan"]["setkey"]))       
                                        a += "│❈ {} hapus [bl]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} removechat\n".format(str(setmain["pengaturan"]["setkey"]))                                        
                                        a += "│❈ {} rebort\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bl   [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} ubl [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} teambot  [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} delbot [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} tsuperadmin  [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bsuperadmin [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} tadmin  [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} badmin [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} tstaff  [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bstaff [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scbl   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scubl [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scsadmin   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scusadmin [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scadmin   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scuadmin [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scstaff   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scustaff [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro qr       [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro invite  [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro kick    [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro cancel [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│●[ FUNGSI DI ATAS UNTUK ALL BOT ]●\n"
                                        a += "│       ❈ {} set\n".format(str(self.resp))
                                        a += "│       ❈ {} kick [@]\n".format(str(self.resp))
                                        a += "│       ❈ {} ubah [nama/bio],[teks]\n".format(str(self.resp))
                                        a += "│       ❈ {} botpic\n".format(str(self.resp))
                                        a += "│       ❈ {} dpgroup\n".format(str(self.resp))
                                        a += "│       ❈ {} list [bl/teman/group]\n".format(str(self.resp))
                                        a += "│       ❈ {} ourl/curl\n".format(str(self.resp))
                                        a += "│●[ FUNGSI DI ATAS UNTUK INITIAL BOT ]●\n"
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA"
                                        ketua.sendMessage(msg.to, a, {'AGENT_NAME':'Perintah super admin menu','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/912/912176.png'})
                                    if msg._from in setmain["list"]["admin"]:
                                        a += "│❈ {} absen\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} spbot\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bot out\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bl   [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} hapus [bl]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} ubl [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} tstaff  [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bstaff [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scbl   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scubl [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scstaff   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scustaff [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro qr       [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro invite  [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro kick    [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro cancel [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│● FUNGSI DI ATAS UNTUK ALL BOT ●\n"
                                        a += "│       ❈ {} pengaturan\n".format(str(self.resp))
                                        a += "│       ❈ {} kick [@]\n".format(str(self.resp))
                                        a += "│       ❈ {} dpgroup\n".format(str(self.resp))
                                        a += "│       ❈ {} list [bl/teman/group]\n".format(str(self.resp))
                                        a += "│       ❈ {} ourl/curl\n".format(str(self.resp))
                                        a += "│● FUGSI DI ATAS UNTUK INITIAL BOT ●\n"
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA"
                                        ketua.sendMessage(msg.to, a, {'AGENT_NAME':'Perintah admin menu','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/912/912176.png'})
                                    if msg._from in setmain["list"]["staff"]:
                                        a += "│❈ {} absen\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} spbot\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bot out\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} bl   [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} hapus [bl]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} ubl [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scbl   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} scubl [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro qr       [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro invite  [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro kick    [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│❈ {} pro cancel [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│● FUNGSI DI ATAS UNTUK ALL BOT ●\n"
                                        a += "│       ❈ {} set\n".format(str(self.resp))
                                        a += "│       ❈ {} kick [@]\n".format(str(self.resp))
                                        a += "│       ❈ {} list bl\n".format(str(self.resp))
                                        a += "│       ❈ {} dpgroup\n".format(str(self.resp))
                                        a += "│       ❈ {} ourl/curl\n".format(str(self.resp))
                                        a += "│● FUNGSI DI ATAS UNTUK INITIAL BOT ●\n"
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA"
                                        ketua.sendMessage(msg.to, a, {'AGENT_NAME':'Perintah staff menu','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/912/912176.png'})
                            
                                #---------------------- Semua Bot Berfungsi --------------------------#
                                
                                elif text.lower() == setmain["pengaturan"]["setkey"]+"absen":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        ketua.sendMention(msg.to,"@!",'','','',[ketua.getProfile().mid])
                                
                                elif text.lower() == setmain["pengaturan"]["setkey"]+"spbot":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        start = time.time()
                                        ketua.sendMessage("u7b7156567827616ebd35687e96990e95", 'Support my channel\nhttps://www.youtube.com/channel/UCzMgN5Zhh9aE9FEahAzgZzA')
                                        ketua.sendMessage(msg.to, '%s ' % (time.time()-start))
                                        
                                elif text.lower() == setmain["pengaturan"]["setkey"]+"removechat":
                                    if msg._from in setmain["list"]["superadmin"] :
                                        try:
                                            ketua.removeAllMessages(op.param2)
                                            ketua.sendMessage(msg.to,"Sukses mebersihakan")
                                        except:
                                            pass  
                                        
                                elif setmain["pengaturan"]["setkey"]+"ubah" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"ubah ", "")
                                        key    = tipe.split(",")
                                        jenis  = key[0]
                                        if jenis not in ["nama","bio","setkey","team"]:
                                            ketua.sendMention(msg.to,"Maaf @!perintah tidak tersedia",'','','',[ketua.getContact(msg._from).mid])
                                        else:
                                            if jenis == "nama":
                                                profile_B = ketua.getProfile()
                                                profile_B.displayName = key[1]
                                                ketua.updateProfile(profile_B)
                                                ketua.sendMessage(msg.to,"Semua bot telah berubah nama menjadi\n{}".format(str(key[1])))
                                            if jenis == "bio":
                                                profile_B = ketua.getProfile()
                                                profile_B.statusMessage = key[1]
                                                ketua.updateProfile(profile_B)
                                                ketua.sendMessage(msg.to,"Semua bot telah berubah bio menjadi\n\n{}".format(str(key[1])))
                                            if jenis == "setkey":
                                                setmain["pengaturan"]["setkey"] = "{}".format(str(key[1]))
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMessage(msg.to,"Setkey telah berubah menjadi {}".format(str(key[1])))
                                            if jenis == "team":
                                                setmain["pengaturan"]["Team"] = "{}".format(str(key[1]))
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMessage(msg.to,"Team telah berubah menjadi {}".format(str(key[1])))
                                
                                elif text.lower() == setmain["pengaturan"]["setkey"]+"botpp":
                                    if msg._from in setmain["list"]["superadmin"]:
                                        setmain["pengaturan"]["fotoku"][msg.to] = True
                                        f = codecs.open("penyimpanan.json","w","utf-8")
                                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        ketua.sendMessage(msg.to,"Silahkan kirim foto yg diinginkan")
                                        
                                elif text.lower() == setmain["pengaturan"]["setkey"]+"bot out":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        ketua.leaveGroup(msg.to)
                                     
                                elif setmain["pengaturan"]["setkey"]+"keluargc " in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        ng   = text.replace(setmain["pengaturan"]["setkey"]+"keluargc ", "")
                                        gid = ketua.getGroupIdsJoined()
                                        for i in gid:
                                            h = ketua.getGroup(i).name
                                            if h == ng:
                                                ketua.leaveGroup(i)
                                                ketua.sendMessage(msg.to,"Sukses Left Group")                         
                                        
                                elif setmain["pengaturan"]["setkey"]+"hapus" in text.lower():
                        #         if msg._from in setmain["list"]["superadmin"]:
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"hapus ", "")
                                        if tipe not in ["bl"]:
                                            ketua.sendMention(msg.to,"Maaf @!perintah tidak tersedia",'','','',[ketua.getContact(msg._from).mid])
                                        else:
                                            if tipe == "bl":
                                                if setmain["list"]["blacklist"] == {}:
                                                    ketua.sendMessage(msg.to, "Blacklist kosong")
                                                else:
                                                    setmain["list"]["blacklist"] = {}
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Blacklist telah dibersihkan total")                            

                                elif text.lower() == setmain["pengaturan"]["setkey"]+"rebort":
                                    if msg._from in setmain["list"]["superadmin"]:
                                        python3 = sys.executable
                                        os.execl(python3, python3, *sys.argv)
                                        
                                elif setmain["pengaturan"]["setkey"]+"bl" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in setmain["list"]["superadmin"] or target in setmain["list"]["admin"] or target in setmain["list"]["staff"]:
                                                ketua.sendMention(msg.to,"Maaf @!tidak bisa masuk blacklist",'','','',[ketua.getContact(target).mid])
                                            else:
                                                try:
                                                    setmain["list"]["blacklist"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMention(msg.to,"@!\nmasuk blacklist",'','','',[ketua.getContact(target).mid])
                                                except:
                                                    ketua.sendMention(msg.to,"@!\nsudah masuk blacklist",'','','',[ketua.getContact(target).mid])
                                                    
                                elif setmain["pengaturan"]["setkey"]+"ubl" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            try:
                                                del setmain["list"]["blacklist"][target]
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMention(msg.to,"@!\nterhapus dari blacklist",'','','',[ketua.getContact(target).mid])
                                            except:
                                                ketua.sendMention(msg.to,"@!\nsudah terhapus dari blacklist",'','','',[ketua.getContact(target).mid])
                                                
                                
                                elif setmain["pengaturan"]["setkey"]+"teambot" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in setmain["list"]["superadmin"] or target in setmain["list"]["admin"] or target in setmain["list"]["staff"]:
                                                ketua.sendMention(msg.to,"Maaf @!tidak bisa masuk botlist",'','','',[ketua.getContact(target).mid])
                                            else:
                                                try:
                                                    setmain["list"]["bot"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMention(msg.to,"@!\nmasuk botlist",'','','',[ketua.getContact(target).mid])
                                                except:
                                                    ketua.sendMention(msg.to,"@!\nsudah masuk botlist",'','','',[ketua.getContact(target).mid])
                                                    
                                elif setmain["pengaturan"]["setkey"]+"delbot" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            try:
                                                del setmain["list"]["bot"][target]
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMention(msg.to,"@!\nterhapus dari botlist",'','','',[ketua.getContact(target).mid])
                                            except:
                                                ketua.sendMention(msg.to,"@!\nsudah terhapus dari botlist",'','','',[ketua.getContact(target).mid])
                                                
                                
                                
                                elif setmain["pengaturan"]["setkey"]+"tsuperadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in setmain["list"]["admin"] or target in setmain["list"]["staff"]:
                                                ketua.sendMention(msg.to,"Maaf @!sudah menjadi admin/staff",'','','',[ketua.getContact(target).mid])
                                            else:
                                                try:
                                                    setmain["list"]["superadmin"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMention(msg.to,"@!\ndiangkat menjadi super admin",'','','',[ketua.getContact(target).mid])
                                                except:
                                                    ketua.sendMention(msg.to,"@!\nsudah menjadi super admin",'','','',[ketua.getContact(target).mid])
                                                    
                                elif setmain["pengaturan"]["setkey"]+"bsuperadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            try:
                                                del setmain["list"]["superadmin"][target]
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMention(msg.to,"@!\nterhapus menjadi super admin",'','','',[ketua.getContact(target).mid])
                                            except:
                                                ketua.sendMention(msg.to,"@!\nsudah terhapus dari super admin",'','','',[ketua.getContact(target).mid])
                                                
                                
                                elif setmain["pengaturan"]["setkey"]+"tadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in setmain["list"]["superadmin"] or target in setmain["list"]["staff"]:
                                                ketua.sendMention(msg.to,"Maaf @!sudah menjadi super admin/staff",'','','',[ketua.getContact(target).mid])
                                            else:
                                                try:
                                                    setmain["list"]["admin"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMention(msg.to,"@!\ndiangkat menjadi admin",'','','',[ketua.getContact(target).mid])
                                                except:
                                                    ketua.sendMention(msg.to,"@!\nsudah menjadi admin",'','','',[ketua.getContact(target).mid])
                                                    
                                elif setmain["pengaturan"]["setkey"]+"badmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            try:
                                                del setmain["list"]["admin"][target]
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMention(msg.to,"@!\nterhapus menjadi admin",'','','',[ketua.getContact(target).mid])
                                            except:
                                                ketua.sendMention(msg.to,"@!\nsudah terhapus dari admin",'','','',[ketua.getContact(target).mid])
                                                
                                elif setmain["pengaturan"]["setkey"]+"tstaff" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            if target in setmain["list"]["superadmin"] or target in setmain["list"]["admin"]:
                                                ketua.sendMention(msg.to,"Maaf @!sudah menjadi super admin/admin",'','','',[ketua.getContact(target).mid])
                                            else:
                                                try:
                                                    setmain["list"]["staff"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMention(msg.to,"@!\ndiangkat menjadi staff",'','','',[ketua.getContact(target).mid])
                                                except:
                                                    ketua.sendMention(msg.to,"@!\nsudah menjadi staff",'','','',[ketua.getContact(target).mid])
                                                    
                                elif setmain["pengaturan"]["setkey"]+"bstaff" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        key = eval(msg.contentMetadata["MENTION"])
                                        key["MENTIONEES"][0]["M"]
                                        targets = []
                                        for x in key["MENTIONEES"]:
                                            targets.append(x["M"])
                                        for target in targets:
                                            try:
                                                del setmain["list"]["staff"][target]
                                                f = codecs.open("penyimpanan.json","w","utf-8")
                                                json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                ketua.sendMention(msg.to,"@!\nterhapus menjadi staff",'','','',[ketua.getContact(target).mid])
                                            except:
                                                ketua.sendMention(msg.to,"@!\nsudah terhapus dari staff",'','','',[ketua.getContact(target).mid])
                                                
                                elif setmain["pengaturan"]["setkey"]+"pro qr" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"pro qr ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["protect"]["linkqr"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["protect"]["linkqr"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Protect QR diaktifkan ✓")
                                            if tipe == "off":
                                                if msg.to not in setmain["protect"]["linkqr"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["protect"]["linkqr"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Protect QR dinonaktifkan 㐅")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"pro invite" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"pro invite ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["protect"]["invite"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["protect"]["invite"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Protect invite diaktifkan ✓")
                                            if tipe == "off":
                                                if msg.to not in setmain["protect"]["invite"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["protect"]["invite"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Protect invite dinonaktifkan 㐅")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"pro kick" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"pro kick ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["protect"]["kick"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["protect"]["kick"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Protect kick diaktifkan ✓")
                                            if tipe == "off":
                                                if msg.to not in setmain["protect"]["kick"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["protect"]["kick"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Protect kick dinonaktifkan 㐅")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"pro cancel" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"pro cancel ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["protect"]["cancel"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["protect"]["cancel"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Protect cancel diaktifkan ✓")
                                            if tipe == "off":
                                                if msg.to not in setmain["protect"]["cancel"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["protect"]["cancel"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Protect cancel dinonaktifkan 㐅")                                                    
            
                                elif setmain["pengaturan"]["setkey"]+"scbl" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scbl ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchbl"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchbl"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin diblacklist")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchbl"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchbl"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Scbl dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scubl" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scubl ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchubl"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchubl"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin diunblacklist")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchubl"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchubl"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Scubl dinonaktifkan")
                                                    
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scsadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scsadmin ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchsadmin"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchsadmin"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin diangkat menjadi super admin")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchsadmin"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchsadmin"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Scsadmin dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scusadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scusadmin ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchusadmin"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchusadmin"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin di copot jabatanya")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchusadmin"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchusadmin"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Scusadmin dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scadmin ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchadmin"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchadmin"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin diangkat menjadi admin")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchadmin"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchadmin"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=True)
                                                    ketua.sendMessage(msg.to,"Scadmin dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scuadmin" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scuadmin ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchuadmin"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchuadmin"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin di copot jabatanya")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchuadmin"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchuadmin"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Scuadmin dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scstaff" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scstaff ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchstaff"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchstaff"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin diangkat menjadi staff")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchstaff"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchstaff"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Scstaff dinonaktifkan")
                                                    
                                elif setmain["pengaturan"]["setkey"]+"scustaff" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                        tipe   = text.replace(setmain["pengaturan"]["setkey"]+"scustaff ", "")
                                        if tipe not in ["on","off"]:
                                            ketua.sendMessage(msg.to,"Akses ditolak")
                                        else:
                                            if tipe == "on":
                                                if msg.to in setmain["kirimkontak"]["switchustaff"]:
                                                    ketua.sendMessage(msg.to,"Sudah aktif")
                                                else:
                                                    setmain["kirimkontak"]["switchustaff"][msg.to] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Kirim kontak yg ingin di copot jabatanya")
                                            if tipe == "off":
                                                if msg.to not in setmain["kirimkontak"]["switchustaff"]:
                                                    ketua.sendMessage(msg.to,"Belum aktif")
                                                else:
                                                    del setmain["kirimkontak"]["switchustaff"][msg.to]
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.sendMessage(msg.to,"Scustaff dinonaktifkan")
                                
                                #---------------------- Satuan Bot Berfungsi --------------------------#
                                
                                elif text.lower() == self.resp +"set":
                                    a = "●ɢʀᴏᴜᴘ ɴᴀᴍᴇ● \n●{}●\n●❈ sᴛᴀᴛᴜs ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ❈●\n╔───────────────── \n".format(str(ketua.getGroup(msg.to).name))
                                    if msg.to in setmain["protect"]["linkqr"]:
                                        a += "│✓ Protect open qr\n"
                                    else:
                                        a += "│🚫 : Protect open qr\n"
                                    if msg.to in setmain["protect"]["invite"]:
                                        a += "│✓ Protect invite\n"
                                    else:
                                        a += "│🚫 : Protect invite\n"
                                    if msg.to in setmain["protect"]["kick"]:
                                        a += "│✓ Protect kick member\n"
                                    else:
                                        a += "│🚫 : Protect kick member\n"
                                    if msg.to in setmain["protect"]["cancel"]:
                                        a += "│✓ Protect cancel member\n"
                                    else:
                                        a += "│🚫 : Protect cancel member\n"
                                    if msg._from in setmain["list"]["superadmin"]:
                                        if msg.to in setmain["kirimkontak"]["switchbl"]:
                                            a += "│✓ SC bl\n"
                                        else:
                                            a += "│🚫 : SC bl\n"
                                        if msg.to in setmain["kirimkontak"]["switchubl"]:
                                            a += "│✓ SC ubl\n"
                                        else:
                                            a += "│🚫 : SC ubl\n"
                                        if msg.to in setmain["kirimkontak"]["switchsadmin"]:
                                            a += "│✓ SC tambah super admin\n"
                                        else:
                                            a += "│🚫 : SC tambah super admin\n"
                                        if msg.to in setmain["kirimkontak"]["switchusadmin"]:
                                            a += "│✓ SC hapus super admin\n"
                                        else:
                                            a += "│🚫 : SC hapus super admin\n"
                                        if msg.to in setmain["kirimkontak"]["switchadmin"]:
                                            a += "│✓ SC tambah admin\n"
                                        else:
                                            a += "│🚫 : SC tambah admin\n"
                                        if msg.to in setmain["kirimkontak"]["switchuadmin"]:
                                            a += "│✓ SC hapus admin\n"
                                        else:
                                            a += "│🚫 : SC hapus admin\n"
                                        if msg.to in setmain["kirimkontak"]["switchstaff"]:
                                            a += "│✓ SC tambah staff\n"
                                        else:
                                            a += "│🚫 : SC tambah staff\n"
                                        if msg.to in setmain["kirimkontak"]["switchustaff"]:
                                            a += "│✓ SC hapus staff\n"
                                        else:
                                            a += "│🚫 : SC hapus staff\n"
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────"
                                    if msg._from in setmain["list"]["admin"]:
                                        if msg.to in setmain["kirimkontak"]["switchbl"]:
                                            a += "│✓ SC bl\n"
                                        else:
                                            a += "│🚫 : SC bl\n"
                                        if msg.to in setmain["kirimkontak"]["switchubl"]:
                                            a += "│✓ SC ubl\n"
                                        else:
                                            a += "│🚫 : SC ubl\n"
                                        if msg.to in setmain["kirimkontak"]["switchstaff"]:
                                            a += "│✓ SC tambah staff\n"
                                        else:
                                            a += "│🚫 : SC tambah staff\n"
                                        if msg.to in setmain["kirimkontak"]["switchustaff"]:
                                            a += "│✓ SC hapus staff\n"
                                        else:
                                            a += "│🚫 : SC hapus staff\n"
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────"
                                    if msg._from in setmain["list"]["staff"]:
                                        if msg.to in setmain["kirimkontak"]["switchbl"]:
                                            a += "│✓ SC bl\n"
                                        else:
                                            a += "│🚫 :  SC bl\n"
                                        if msg.to in setmain["kirimkontak"]["switchubl"]:
                                            a += "│✓ SC ubl\n"
                                        else:
                                            a += "│🚫 : SC ubl\n"
                                        a += "│‣ {} bl   [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} ubl [@]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} scbl   [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} scubl [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} pro qr       [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} pro invite  [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} pro kick    [on/off]\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│‣ {} pro cancel [on/off]\n\n".format(str(setmain["pengaturan"]["setkey"]))
                                        a += "│🕺ɢᴜɴᴀᴋᴀɴ ʙᴏᴛ ᴅᴇɴɢᴀɴ ʙɪᴊᴀᴋ🕺\n╚─────────────────────"
                                    ketua.sendMessage(msg.to,a, {'AGENT_NAME':'Jangan lupa matikan setelah aktif','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/912/912176.png'})
                                
                                elif self.resp +"kick" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        if 'MENTION' in msg.contentMetadata.keys()!=None:
                                            key = eval(msg.contentMetadata["MENTION"])
                                            key["MENTIONEES"][0]["M"]
                                            targets = []
                                            for x in key["MENTIONEES"]:
                                                targets.append(x["M"])
                                            for target in targets:
                                                if target in setmain["list"]["superadmin"] or target in setmain["list"]["admin"] or target in setmain["list"]["staff"]:
                                                    ketua.sendMention(msg.to,"Maaf @!, {} ada didalam list bot jadi tidak bisa dikick".format(str(ketua.getContact(target).mid)),'','','',[ketua.getContact(msg._from).mid])
                                                else:
                                                    setmain["list"]["blacklist"][target] = True
                                                    f = codecs.open("penyimpanan.json","w","utf-8")
                                                    json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                                    ketua.kickoutFromGroup(msg.to,[target])
                                                    time.sleep(0.001)
                                
                                elif self.resp +"ubah" in text.lower():
                                    if msg._from in setmain["list"]["superadmin"]:
                                        tipe   = text.replace(self.resp +"ubah ", "")
                                        key    = tipe.split(",")
                                        jenis  = key[0]
                                        if jenis not in ["nama","bio"]:
                                            ketua.sendMention(msg.to,"Maaf @!perintah tidak tersedia",'','','',[ketua.getContact(msg._from).mid])
                                        else:
                                            if jenis == "nama":
                                                profile_B = ketua.getProfile()
                                                profile_B.displayName = key[1]
                                                ketua.updateProfile(profile_B)
                                                ketua.sendMessage(msg.to,"Bot telah berubah nama menjadi\n{}".format(str(key[1])))
                                            if jenis == "bio":
                                                profile_B = ketua.getProfile()
                                                profile_B.statusMessage = key[1]
                                                ketua.updateProfile(profile_B)
                                                ketua.sendMessage(msg.to,"Bot telah berubah bio menjadi\n\n{}".format(str(key[1])))
                                
                                elif text.lower() == self.resp +"botpic":
                                    if msg._from in setmain["list"]["superadmin"]:
                                        setmain["pengaturan"]["fotoku"][msg.to] = True
                                        f = codecs.open("penyimpanan.json","w","utf-8")
                                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        ketua.sendMessage(msg.to,"ꓢꓲꓡꓮꓧꓗꓮꓠ ꓗꓲꓣꓲꓟ ꓝꓳꓔꓳ ꓬꓮꓠꓖ ꓓꓲ ꓲꓠꓖꓲꓠꓗꓮꓠ")
                                
                                elif text.lower() == self.resp +"dpgroup":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        setmain["pengaturan"]["fotogr"][msg.to] = True
                                        f = codecs.open("penyimpanan.json","w","utf-8")
                                        json.dump(setmain, f, sort_keys=True, indent=4,ensure_ascii=False)
                                        ketua.sendMessage(msg.to,"ꓢꓲꓡꓮꓧꓗꓮꓠ ꓗꓲꓣꓲꓟ ꓝꓳꓔꓳ ꓬꓮꓠꓖ ꓓꓲ ꓲꓠꓖꓲꓠꓗꓮꓠ")
                                
                                elif self.resp +"list" in text.lower():
                                    tipe   = text.replace(self.resp +"list ", "")
                                    if tipe not in ["bl","teman","group"]:
                                        ketua.sendMention(msg.to,"Maaf @!perintah tidak tersedia",'','','',[ketua.getContact(msg._from).mid])
                                    else:
                                        if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                            if tipe == "bl":
                                                if setmain["list"]["blacklist"] == {}:
                                                    ketua.sendMessage(msg.to, "Blacklist kosong", {'AGENT_NAME':'BLACKLIST','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/349/349354.png'})
                                                else:
                                                    no = 0
                                                    a  = "⚒ List\n"
                                                    for b in setmain["list"]["blacklist"]:
                                                        no += 1
                                                        a  += "\n{}. {}".format(str(no), str(ketua.getContact(b).displayName))
                                                    a += "\nTotal {} blacklist".format(str(len(setmain["list"]["blacklist"])))
                                                    ketua.sendMessage(msg.to,a, {'AGENT_NAME':'BLACKLIST','AGENT_ICON': 'https://image.flaticon.com/icons/png/512/349/349354.png'})
                                            if tipe == "teman":
                                                if msg._from in setmain["list"]["superadmin"]:
                                                    no = 0
                                                    a = "今 ꓳꓪꓠꓰꓣ ꓡꓲꓢꓔ 今\n⎯⎯⎯⎯⎯⎯⎯⎯\n"
                                                    b = "今 ꓮꓓꓟꓲꓠ ꓡꓲꓢꓔ 今\n⎯⎯⎯⎯⎯⎯⎯⎯\n"
                                                    c = "今 ꓢꓔꓮꓝꓝ ꓡꓲꓢꓔ 今\n⎯⎯⎯⎯⎯⎯⎯⎯\n"
                                                    d = "今 ꓐꓳꓔ ꓡꓲꓢꓔ 今\n⎯⎯⎯⎯⎯⎯⎯⎯\n"
                                                    for aa in setmain["list"]["superadmin"]:
                                                        no += 1
                                                        a += "{}. {}\n".format(str(no), str(ketua.getContact(aa).displayName[0:40]))
                                                    for bb in setmain["list"]["admin"]:
                                                        no += 1
                                                        b += "{}. {}\n".format(str(no), str(ketua.getContact(bb).displayName[0:40]))
                                                    for cc in setmain["list"]["staff"]:
                                                        no += 1
                                                        c += "{}. {}\n".format(str(no), str(ketua.getContact(cc).displayName[0:40]))
                                                    for dd in setmain["list"]["bot"]:
                                                        no += 1
                                                        d += "{}. {}\n".format(str(no), str(ketua.getContact(dd).displayName[0:40]))
                                                    ketua.sendMessage(msg.to,a+"\n"+b+"\n"+c+"\n"+d+"\n\nTotal %s teman" %(str(len(setmain["list"]["superadmin"])+len(setmain["list"]["admin"])+len(setmain["list"]["staff"])+len(setmain["list"]["bot"]))))
                                                if msg._from in setmain["list"]["admin"]:
                                                    no = 0
                                                    a = "今 ꓢꓔꓮꓝꓝ ꓡꓲꓢꓔ 今\n"
                                                    for aa in setmain["list"]["staff"]:
                                                        no += 1
                                                        a += "{}. {}\n".format(str(no), str(ketua.getContact(aa).displayName[0:40]))
                                                    a += "Total {} staff".format(str(len(setmain["list"]["staff"])))
                                                    ketua.sendMessage(msg.to,a)
                                        else:
                                            pass
                                        if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"]:
                                            if tipe == "group":
                                                no = 0
                                                a = "❇ ꓡꓲꓢꓔ ꓖꓣꓳꓴꓑ ❇\n⎯⎯⎯⎯⎯⎯⎯⎯\n"
                                                for b in ketua.getGroupIdsJoined():
                                                    no += 1
                                                    a  += "{}. {}\n".format(str(no), str(ketua.getGroup(b).name))
                                                a += "Total {} group\n⎯⎯⎯⎯⎯⎯⎯⎯\n".format(str(len(ketua.getGroupIdsJoined())))
                                                ketua.sendMessage(msg.to,a)
                                                
                                elif text.lower() == self.resp +"ourl":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        x = ketua.getGroup(msg.to)
                                        if x.preventedJoinByTicket == True:
                                            x.preventedJoinByTicket = False
                                            ketua.updateGroup(x)
                                        gurl = ketua.reissueGroupTicket(msg.to)
                                        ketua.sendMessage(msg.to,"line://ti/g/{}".format(str(gurl)))
                                
                                elif text.lower() == self.resp +"curl":
                                    if msg._from in setmain["list"]["superadmin"] or msg._from in setmain["list"]["admin"] or msg._from in setmain["list"]["staff"]:
                                        X = ketua.getGroup(msg.to)
                                        X.preventedJoinByTicket = True
                                        ketua.updateGroup(X)
                            except Exception as e:
                                ketua.sendMessage(msg.to,"{}".format(str(e)))
                                
        except Exception as e:
            print(e)
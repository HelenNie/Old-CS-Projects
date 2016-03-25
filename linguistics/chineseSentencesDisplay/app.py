#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import request,Flask,render_template, url_for,redirect,request
from flask_mail import Mail, Message
import urllib2,json
import random
import time
import base64

with open("pwd.txt", "r") as myfile:
  pwd = base64.b64decode(myfile.read())

app = Flask(__name__)
app.config.update(
  DEBUG = True,
  MAIL_SERVER = 'smtp.gmail.com',
  MAIL_PORT = 587,
  MAIL_USE_TLS = True,
  MAIL_USE_SSL = False,
  MAIL_USERNAME="helen.nie94@gmail.com",
  MAIL_PASSWORD=pwd
)
mail = Mail(app)

global ordered_sentences, shuffled_indexes, subject_number, round_number, currTime, ordered_sounds

subject_number = 2
round_number = 1

currTime = time.strftime("%c")

ordered_sentences = [
      '他养过青蛙。',
      '她明年要生娃。',
      '他要去买砖瓦。',
      '你忘了穿丝袜。',
      '现在是高温。',
      '娜娜会说中文。',
      '红色的椅子都稳。',
      '他要去我家问。',
      '他喜欢吃烧鸭。',
      '你忘了刷牙。',
      '她的姿态高雅。',
      '玛丽要游三亚。',
      '孙悟空会捉妖。',
      '他会唱歌谣。',
      '这药膏治叮咬。',
      '他讨厌吃药。',
      '你懂得中医。',
      '他认识这个阿姨。',
      '他要买新桌椅。',
      '小张有争议。',
      '他想要偷溜。',
      '大河是向东流。',
      '你每年去插柳。',
      '他的狗要每天溜。',
      '猫都让她摸。',
      '西游记里有妖魔。',
      '日霜是白天抹。',
      '这岛会被淹没。',
      '她名字叫三妞。',
      '他喜欢吹牛。',
      '秧歌是边跳边扭。',
      '丽丽比小明拗。',
      '他养过青蛙？',
      '她明年要生娃？',
      '他要去买砖瓦？',
      '你忘了穿丝袜？',
      '现在是高温？',
      '娜娜会说中文？',
      '红色的椅子都稳？',
      '他要去我家问？',
      '他喜欢吃烧鸭？',
      '你忘了刷牙？',
      '她的姿态高雅？',
      '玛丽要游三亚？',
      '孙悟空会捉妖？',
      '他会唱歌谣？',
      '这药膏治叮咬？',
      '他讨厌吃药？',
      '你懂得中医？',
      '他认识这个阿姨？',
      '他要买新桌椅？',
      '小张有争议？',
      '他想要偷溜？',
      '大河是向东流？',
      '你每年去插柳？',
      '他的狗要每天溜？',
      '猫都让她摸？',
      '西游记里有妖魔？',
      '日霜是白天抹？',
      '这岛会被淹没？',
      '她名字叫三妞？',
      '他喜欢吹牛？',
      '秧歌是边跳边扭？',
      '丽丽比小明拗？'
]

ordered_sounds = ['wa', 'wen', 'ya', 'yao', 'yi', 'liu', 'mo', 'niu']

@app.route("/", methods=["GET", "POST"])
def home():
  if request.method=="GET":
    return render_template("home.html")

@app.route("/record", methods=["GET", "POST"])
def record():
  if request.method=="GET":
    with open("record.txt", "r") as myfile:
      record = myfile.read().splitlines()
    return render_template("record.html", record=record)

@app.route("/get_sentences")
def get_sentences():
  global ordered_sentences, shuffled_indexes
  shuffled_indexes = [i for i in range(0,len(ordered_sentences))]
  random.shuffle(shuffled_indexes)
  #save_indexes();
  shuffled_sentences = [ordered_sentences[i] for i in shuffled_indexes]
  return json.dumps(shuffled_sentences)

@app.route("/save_indexes")
def save_indexes():
  global ordered_sentences, shuffled_indexes, subject_number, currTime, ordered_sounds;

  shuffled_sounds = []
  for i in shuffled_indexes:
    if i < 32:
      sound = "S_"
    else:
      sound = "Q_"
    i_sound = (i%32)/4
    sound = sound + ordered_sounds[i_sound] + "_"
    i_tone = (i%32)%4+1
    sound = sound + str(i_tone)
    shuffled_sounds.append(sound)

  with open("record.txt", "a") as myfile:
    myfile.write("\n-------------------------\n");
    myfile.write("Subject "+str(subject_number));
    myfile.write("\n");
    myfile.write("Round "+str(round_number));
    myfile.write("\n");
    myfile.write(currTime);
    myfile.write("\n");
    myfile.write(",".join([str(i) for i in shuffled_indexes]))
    myfile.write("\n");
    myfile.write(",".join([str(i) for i in shuffled_sounds]))
  return json.dumps({'indexes':"saved"})

@app.route("/email")
def email():
  global currTime
  msg = Message("Chinese Recording Log Subject "+str(subject_number)+" "+currTime,
                sender="helen.nie94@gmail.com",
                recipients=["helen.nie94@gmail.com"])
  with app.open_resource("record.txt") as fp:
    msg.attach("record.txt", "text/txt", fp.read())
  mail.send(msg)
  return json.dumps({'email':"sent"})

if __name__ == "__main__":
  app.run()
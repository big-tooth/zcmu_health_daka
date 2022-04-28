import requests, time, math, json

# from Queue import Queue, LifoQueue, PriorityQueue


def daka(id,flag):
    # print("时间戳：",int(time.time()))
    print(id,flag)
    # 获取问卷id
    d = {
        'pageNum': 1,
        'nodataFlag': 'false',
        'pageSize': 10,
        'userId': id
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post("https://daka.zcmu.edu.cn/questionnaireSurvey/queryQuestionnairePageList", headers=headers,
                      params=d)
    d_json = r.content.decode('utf-8')
    questionnaireId = json.loads(d_json)['rows'][0]['ID']
    print(questionnaireId)
    # 获取预填信息
    data = {
        'questionnaireId': questionnaireId,
        'userId': id
    }
    r = requests.post("https://daka.zcmu.edu.cn/questionnaireSurvey/queryQuestionnaireDetail", headers=headers,
                      data=data)
    # print(r.status_code)
    str_json = json.loads(r.content.decode("utf-8"))
    print(str_json['rows'])

    # 修改部分信息
    with open("question.json", 'r', encoding="utf-8") as load_question:
        load_answer = json.load(load_question)
    # 读取问卷格式
    with open("questionnaire.json", 'r', encoding='utf-8') as load_f1:
        load_qustionnaire = json.load(load_f1)
    daka_info = json.loads(r.content.decode('utf-8'))
    daka_info_rows = daka_info['rows']
    print("daka_info_raws是", daka_info_rows)
    for i in range(1, len(daka_info_rows) ):
        load_qustionnaire["answerData"][i - 1]['itemId'] = daka_info_rows[i]["ITEMID"]
        load_qustionnaire["answerData"][i - 1]['itemType'] = daka_info_rows[i]["TYPE"]
        if ("ANSWERTEXT" in daka_info_rows[i]):
            load_qustionnaire["answerData"][i - 1]['answerArr'][0] = daka_info_rows[i]["ANSWERTEXT"]
        else:
            for ii in range(len(daka_info_rows[i]['OPTIONS'])):
                if daka_info_rows[i]['OPTIONS'][ii]['CHECKED'] == True:
                    load_qustionnaire["answerData"][i - 1]['answerArr'][0] = daka_info_rows[i]['OPTIONS'][ii]['SUBID']
    for i in range(len(load_answer)-1):
        load_qustionnaire["answerData"][load_answer[i]["id"]-1]["answerArr"][0] = daka_info_rows[load_answer[i]["id"]]['OPTIONS'][load_answer[i]["flag"][flag]["num"]]['SUBID']
    final_daka = json.dumps(load_qustionnaire, ensure_ascii=False)

    print("提交内容"+final_daka)

    data = {
        'questionnaireId': questionnaireId,
        'userId': id,
        'answerData': final_daka
    }
    r = requests.post("https://daka.zcmu.edu.cn/questionnaireSurvey/addQuestionnaireRecord", headers=headers, data=data)
    print(r.status_code)
    print(r.content.decode('utf-8'))
    daka_sign = str_json["rspcode"]
    if daka_sign == "000000":
        print("打卡成功")
    else:
        print("打卡失败")


# def send_daka():
#     daka_content=""
#     if qF.empty()==True:
#         daka_content="打卡成功"
#     else:
#         while qF.empty()!=True:
#             daka_content=daka+"学号："+qF.get()+"打卡失败\n"
#     daka={
#         'token':'',
#         'title':'每日健康打卡',
#         'content':daka_content
#     }
#     push_headers={'Content-Type': 'application/json'}
#     r = requests.post("http://pushplus.hxtrip.com/send", headers=push_headers,params=d)

def main_handler(event, context):
    with open("id.json", 'r') as load_f:
        load_dict = json.load(load_f)

    for i in range(4):
        daka(load_dict[i]['id'],load_dict[i]['flag'])
        print("OK")


with open("id.json", 'r') as load_f:
    load_dict = json.load(load_f)

for i in range(len(load_dict)):
    daka(load_dict[i]['id'],load_dict[i]['flag'])
    print("OK")
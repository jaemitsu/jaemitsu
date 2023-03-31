# -*- coding: utf-8 -*-
import json
import os
from argparse import ArgumentParser
import pandas as pd
import shutil

def main():
    parser = ArgumentParser(description = 'Process 2-4-2 convert to TUDataset')
    parser.add_argument('input_dir', type=str, nargs=1) #입력경로, 라벨링 완료된 JSON
    parser.add_argument('output_dir', default = "./", type=str, nargs=1) #목적경로, 변환된 TUDataset format text
    args = parser.parse_args()
    if not os.path.isdir(args.input_dir[0]): #리스트형태이므로 [0]으로 꺼내어 str으로 해당 변수가 참조가능하도록 하며 해당 path가 폴더가 아닌 경우
        print("ERROR> Invalid path") # 앞과 같은 에러를 
        return
    input_dir = args.input_dir[0]
    output_dir = args.output_dir[0]
    
    all_idnf_dict = {}
    cnt0 = {}
    cnt1 = {}
    cnt2 = {}
    cnt4 = {}
    cnt5 = {}
    nn = 0
    for (root, dirs, files) in os.walk(input_dir):
        dirname = ""
        cnt = ""
        idnf_dict = {}
        output_target_path = output_dir #remove color'빨간색' : '25', '주황색' : '26', '노란색' : '27', '초록색' : '28', '파란색' : '29', '남색' : '30', '보라색' : '31', '흰색' : '32', '검은색' : '33', '회색' : '34', '투명' : '35', '반투명' : '36', '혼합색' : '37'
        node_label = {'frame' : '0', '사물' : '1', '사람' : '2', '바닥' : '3', '벽' : '4', '보안구역' : '5', '상황혼잡도' : '6', '목적지' : '7', '이정표' : '8', '크다' : '9', '작다' : '10', '장애물' : '11', '비장애물' : '12', '비회피장애물' : '13', '정지' : '14', '이동중' : '15', '접근중' : '16', '느림' : '17', '일반' : '18', '빠름' : '19', '정면' : '20', '후면' : '21', '좌측' : '22', '우측' : '23', '방향없음' : '24', '구분안됨' : '38', '서다' : '39', '숙이다' : '40', '앉다' : '41', '눕다' : '42', '걷다' : '43', '뛰다' : '44', '그룹' : '45', '남자' : '46', '여자' : '47', '판단불가' : '48', '아동' : '49', '청중년' : '50', '노인' : '51', '안내(접객)요청자' : '52', '요구조자' : '53', '침입자' : '54', '흡연자' : '55', '오물투척자' : '56', '휴대폰사용자' : '57', '비참여자' : '58', '추종대상자' : '59', '무늬' : '60', '고속' : '61', '저속' : '62', '주행불가' : '63', '매끄러움' : '64', '거침' : '65', '요철' : '66', '오염' : '67', '경사' : '68', '카펫' : '69','점자블럭' : '70', '해당없음' : '71', '혼잡' : '72', '여유' : '73', '관측불가우측' : '74', '관측불가좌측' : '75', '관측불가후방' : '76', '원거리좌측' : '77', '근거리좌측' : '78', '원거리정면' : '79', '근거리정면' : '80', '원거리우측' : '81', '근거리우측' : '82', '좌' : '83', '우' : '84', '직진' : '85', '후진' : '86', '정지(금지)' : '87', '기타' : '88', '안내공간' : '89', '이동공간' : '90', '휴게공간' : '91', '판매공간' : '92', '전시공간' : '93', '사무공간' : '94', '의료공간' : '95', '문화공간' : '96', '화재' : '97',"불꽃심각크다" : '98', "불꽃경미작다" : '99', "연기심각농도진함" : '100', "연기경미농도옅음" : '101', '회전_우측': '102', '회전_좌측': '103', '정지 장애물 회피_좌회전_저속': '104', '접근 장애물 회피_직진_저속': '105', '접근 장애물 회피_직진_고속': '106', '정지 장애물 회피_좌회전_고속': '107', '접근 장애물 회피_우회전_고속': '108', '정지 장애물 회피_우회전_일반': '109', '접근 장애물 회피_우회전_저속': '110', '정지 장애물 회피_좌회전_일반': '111', '접근 장애물 회피_우회전_일반': '112', '접근 장애물 회피_좌회전_고속': '113', '접근 장애물 회피_좌회전_저속': '114', '정지 장애물 회피_우회전_저속': '115', '접근 장애물 회피_좌회전_일반': '116', '정지 장애물 회피_우회전_고속': '117', '추종 주행_우측': '118', '추종 주행_좌측': '119', '정지_일시정지': '120', '정지_일반': '121', '정지_긴급': '122', '추월_우회전_저속': '123', '추월_좌회전_일반': '124', '추월_좌회전_고속': '125', '추월_우회전_일반': '126', '추월_우회전_고속': '127', '추월_좌회전_저속': '128', '통로확보_장애물제거(개척)_전방': '129', '통로확보_장애물제거(개척)_좌측': '130', '통로확보_장애물제거(개척)_우측': '131', '직진_저속': '132', '우회전_고속': '133', '직진_고속': '134', '유지_통과': '135', '후진': '136', '좌회전_고속': '137', '좌회전_저속': '138', '우회전_일반': '139', '직진_일반': '140', '우회전_저속': '141', '좌회전_일반': '142', '선회_좌측': '143', '선회_우측': '144', '추월허용_좌측': '145', '추월허용_우측': '146', '경보(알람)_요구조자발생': '147', '경보(알람)_침입': '148', '경보(알람)_보행시 휴대폰 사용': '149', '경보(알람)_흡연, 오물투척 경고 등': '150', '경보(알람)_화재': '151', '행동클래스': '152'}
        #frame : 94 인위적 추가
        if input_dir != root: #최상위 폴더가 아닌 경우(재귀단계)
            subdir_name = root.replace(input_dir, "") #root 앞의 경로인 input을 지워서 지정할 폴더명을 가져옴
        if not os.path.exists(output_target_path): #정의된 path가 존재하지않으면 폴더를 생성
            os.makedirs(output_target_path)   
        try:
            if len(files) > 0: #폴더내부에 파일이 존재하면
                for filename in files: #각각의 파일들에 대하여
                    name, ext = os.path.splitext(filename)#이름과 확장자를 받아서
                    if root.split(os.sep)[-1] != dirname:
                        dirname = root.split(os.sep)[-1]
                    if ext.lower() == '.json': #대소문자를 소문자로 정규화시켜서 json파일인지 확인하고 맞다면
                        jsonPath = os.path.join(root, filename) #파일이름과 root(path)와 합쳐서 json파일의 경로를 정의 
                        newtextPath = output_target_path + os.sep + dirname
                        if not os.path.exists(newtextPath):
                            os.makedirs(newtextPath) 
                        idnf_dict, all_idnf_dict = jsoncvt(jsonPath, node_label, idnf_dict, all_idnf_dict)
                nn += len(files)
                for k, v in idnf_dict.items():
                    cnt += k + " : " + str(v) + "\n"
                cnt0[root.split(os.sep)[-1]] = len(files)
                cnt1[root.split(os.sep)[-1]] = idnf_dict
                with open(newtextPath + os.sep + "_count.txt", "w", encoding="UTF-8") as idnf_dictfile:
                    idnf_dictfile.write(f'{idnf_dict}')
    

        except Exception as e:
            print(jsonPath + " jsonError") # josnpath가 없거나 잘못된 경우 예외처리
            raise e
    for k1, v1 in cnt0.items():
        cnt3 = {}
        for k2, v2 in cnt1[k1].items():
            cnt3[k2] = v2/v1
        cnt2[k1] = cnt3
    for k3, v3 in all_idnf_dict.items():
        cnt4[k3] = v3/nn
    # print(cnt2)
    # print(cnt4)
    for k4, v4 in cnt2.items():
        cnt6 = {}
        for k5, v5 in cnt2[k4].items():
            if k5 in cnt4:
                cnt6[k5] = f'{v5/cnt4[k5]:.4f}'
            else:
                continue
        cnt5[k4] = dict(sorted(cnt6.items(), key=lambda x: x[1], reverse=True))
        
            
    df_excel = pd.concat({k6: pd.Series(v6) for k6, v6 in cnt5.items()}).reset_index()
    df_excel.columns = ['class', 'label','tf-idf']
    df_excel.to_csv(output_target_path + os.sep + "statistic.csv", encoding = 'cp949', index=False)
    # df_excel.to_csv("./statistic.csv", header= header)
        
    if not os.path.exists(output_target_path): #정의된 path가 존재하지않으면 폴더를 생성
            os.makedirs(output_target_path) 
    with open(output_target_path + os.sep + "_all_count1.txt", "w", encoding="UTF-8") as cnt4file:
        cnt4file.write(f'{all_idnf_dict}')
    with open(output_target_path + os.sep + "_all_count2.txt", "w", encoding="UTF-8") as cnt1file:
        cnt1file.write(f'{cnt1}')
    with open(output_target_path + os.sep + "_count1.txt", "w", encoding="UTF-8") as cnt0file:
        cnt0file.write(f'{cnt0}')
    with open(output_target_path + os.sep + "_count2.txt", "w", encoding="UTF-8") as cnt5file:
        cnt5file.write(f'{cnt5}')
    
        


        

def jsoncvt(jsonPath, node_label, idnf_dict, all_idnf_dict):
    with open(jsonPath, "r", encoding="UTF-8") as json_file: 
        org = json.load(json_file)
    for label in org["annotation"]: #sourcenode & sourcenode+frame중심node
        if "value" not in label["polygon"]:
            # print(graph_id, "\t", anno_num, "\t", jsonPath.split(os.sep)[-2:], "\t", "value오류", label["polygon"]["label"]) #value 결측치가 있는 json파일 index
            # print(graph_id, "\t", anno_num, "\t", jsonPath.split(os.sep)[-2:], "\t", "value오류", label["polygon"]["label"]) #value오류가 있는 유형의 종류
            continue
        else:
            for _, target in label["polygon"]["value"].items():
                attr_ = target.replace(" ","")
                if attr_ not in node_label:
                    # print(graph_id, "\t", anno_num, "\t", attr_, "\t", jsonPath, "\t", "attr_오류")
                    # print(graph_id, "\t", attr_, "\t", jsonPath.split(os.sep)[-2:], "\t", "attr_오류")
                    continue
                else:
                    endpoint = label["polygon"]["label"] + ", " + attr_

                    if endpoint in idnf_dict:
                        idnf_dict[endpoint] += 1
                    else:
                        idnf_dict[endpoint] = 1
                    if endpoint in all_idnf_dict:
                        all_idnf_dict[endpoint] += 1
                    else:
                        all_idnf_dict[endpoint] = 1
    return idnf_dict, all_idnf_dict
if __name__ == "__main__":
    main()
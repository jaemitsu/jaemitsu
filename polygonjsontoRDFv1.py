# -*- coding: utf-8 -*-
import json
import os
from argparse import ArgumentParser
import shutil
def main():
    parser = ArgumentParser(description = 'Process 2-4-2 convert to RDF')
    parser.add_argument('input_dir', type=str, nargs=1) #입력경로, 라벨링 완료된 JSON
    parser.add_argument('output_dir', type=str, nargs=1) #목적경로, 변환된 TUDataset format text
    args = parser.parse_args()
    if not os.path.isdir(args.input_dir[0]): #리스트형태이므로 [0]으로 꺼내어 str으로 해당 변수가 참조가능하도록 하며 해당 path가 폴더가 아닌 경우
        print("ERROR> Invalid path") # 앞과 같은 에러를 
        return
    input_dir = args.input_dir[0]
    output_dir = args.output_dir[0]
    dics = {}
    RDF_ = ""
    idn = 1
    for (root, dirs, files) in os.walk(input_dir):
        output_target_path = output_dir
        #frame : 94 인위적 추가
        if input_dir != root: #최상위 폴더가 아닌 경우(재귀단계)
            subdir_name = root.replace(input_dir, "") #root 앞의 경로인 input을 지워서 지정할 폴더명을 가져옴
        if not os.path.exists(output_target_path): #정의된 path가 존재하지않으면 폴더를 생성
            os.makedirs(output_target_path)   
        try:
            if len(files) > 0: #폴더내부에 파일이 존재하면
                
                for filename in files: #각각의 파일들에 대하여
                    name, ext = os.path.splitext(filename)#이름과 확장자를 받아서
                    if ext.lower() == '.json': #대소문자를 소문자로 정규화시켜서 json파일인지 확인하고 맞다면
                        jsonPath = os.path.join(root, filename) #파일이름과 root(path)와 합쳐서 json파일의 경로를 정의 
                        newtextPath = output_target_path
                        if not os.path.exists(newtextPath):
                            os.makedirs(newtextPath) 
                        RDF_, idn = jsoncvt(jsonPath, RDF_, idn, dics)
                with open(newtextPath + os.sep + output_dir + "_graph_labels.txt", "w", encoding="UTF-8") as RDFfile: #txt저장
                    RDFfile.write(RDF_)
        except Exception as e:
            print(jsonPath + " jsonError") # josnpath가 없거나 잘못된 경우 예외처리
            raise e
        
    if not os.path.exists(output_target_path): #정의된 path가 존재하지않으면 폴더를 생성
        os.makedirs(output_target_path) 
    with open(newtextPath + os.sep + output_dir + "RDF.txt", "w", encoding="UTF-8") as RDFfile: #txt저장
        RDFfile.write(RDF_)
            
        

def jsoncvt(jsonPath, RDF_, idn, dics):
    with open(jsonPath, "r", encoding="UTF-8") as json_file: 
        org = json.load(json_file)
    scene = "<" + org["metaData"]["id"] + ">"
    scene = scene.replace(" ","")
    prediction = "<" + org["metaData"]["행동 클래스"] + ">"
    prediction = prediction.replace(" ","")
    RDF_ += scene + " " + "<예측행동>" + " " + prediction + " ." + "\n" 
    for label in org["annotation"]:
        if "label" not in label["polygon"]:
            continue
        else:
            for idx in label:                         
                if label["polygon"]["label"] == "사람" or "벽" or "장애물" or "이정표" or "바닥":
                    RDF_ += scene + " " + "<있다>" + " " + "_:" + str(idn) + " ." + "\n"
                    
                    if 'value' not in label["polygon"]:
                        continue
                    for key, val in label["polygon"]["value"].items():
                        key = key.replace(" ","")
                        val = val.replace(" ","")
                        RDF_ += "_:" + str(idn) + " " + f'<{key}>' + " " + f'<{val}>' + " ." + "\n"
                    idn += 1

                else:
                    continue

        # RDF_ += scene + "<있다>" + 
         
    return RDF_, idn
if __name__ == "__main__":
    main()
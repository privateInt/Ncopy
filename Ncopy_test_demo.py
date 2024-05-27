# -*- coding: utf-8 -*-

import requests
import streamlit as st
from Ncopy_test_utils import *
from datetime import datetime
import os
import json

backup_path = "streamlit log"
os.makedirs(backup_path, exist_ok = True)

host = 'YOUR HOST'
api_key = 'YOUR API KEY'
api_key_primary_val = 'YOUR API KEY PRIMARY VAL'


model = CompletionExecutor(
        host=host,
        host_add = 'YOUR HOST ADD',
        api_key=api_key,
        api_key_primary_val=api_key_primary_val,
        request_id='YOUR REQUEST ID'
)

control_dict = make_control_dict(
    head = "\"2~3문장\"으로 이루어진 \"50글자\" 내외의 광고 헤드 카피",
    body = "\"7~8문장\"으로 이루어진 \"200글자\" 내외의 광고 바디 카피",
    
    base = "기본",
    review = "리뷰",
    action = "행동촉구",
    question = "질문",
    humor = "언어유희",
    
    base_desc = "제품이나 서비스를 소개하고, 이를 구매해야 하는 이유를 간결하고 명확하게 작성합니다.",
    review_desc = "제품을 실제로 구매해 사용해본 사용자의 입장에서 후기를 작성하듯 작성합니다.",
    action_desc = "프로모션을 소개하는 등, 소비자에게 즉각적인 행동을 유도하도록 작성합니다.",
    question_desc = "소비자의 관심을 끌고 호기심을 자극할 수 있도록 질문 형태로 작성합니다.",
    humor_desc = "비슷한 발음이나 의미를 가진 단어를 활용하여 재미있는 느낌을 주도록 작성합니다.",
    
    no_gender = "선택 안함",
    male = "남성",
    female = "여성",
    
    no_age = "전체",
    juvenile = "청소년",
    twenties_thirties = "20대,30대",
    forties_fifties = "40대,50대",
    senior = "노인",
    
    # max_num = 5
)
example_dict = make_example_dict(control_dict)

def main():
    st.title("Ncopy_ver2 test web page")
    # 생성할 카피 개수: 1 ~ {control_dict["max_num"][-1]}
    # 모델: {", ".join([i for i in model_dict])}
    # (HCX-DASH-001: HCX-003 경량화 버전, 가격 1/5수준, 속도 상승)
    # 톤앤매너 예제 삽입 여부: True, False
    # (True: 지정된 톤앤매너 예제만 사용)
    # (False: 모든 예제 사용)
    st.write(f"""
    Ncopy_ver2를 실험하기 위한 페이지입니다.\n
    생성하고 싶은 카피의 자세한 내용을 선택 및 작성 후 광고 카피 생성 버튼을 눌러주세요.
    예제 내용은 업데이트 중 입니다.
    \nparameter 설명\n
    카피 유형: body - 100글자 내외의 광고카피, head - 20글자 내외의 광고카피
    톤앤매너: {", ".join([control_dict["TM"][i] for i in control_dict["TM"]])}
    성별: {", ".join([control_dict["gender"][i] for i in control_dict["gender"]])}
    연령층: {", ".join([control_dict["age"][i] for i in control_dict["age"]])}
    상품명: 생성할 광고카피의 상품명, 수정 가능합니다. 기본값: "바나나 우유"
    키워드: 생성할 광고카피의 키워드, 수정 가능합니다. 기본값: "달콤함, 행복함\n""")
    
    with st.form('Ncopy2'):
        # model = st.selectbox("모델", [i for i in model_dict])
        # example_flag = st.selectbox("톤앤매너 예제 삽입 여부", [True, False])
        # max_num = st.selectbox("생성할 예제 개수", [i for i in control_dict["max_num"]])
        copy_type = st.selectbox("카피 유형", [i for i in control_dict["type"]])
        TM = st.selectbox("톤앤매너", [control_dict["TM"][i] for i in control_dict["TM"]])
        gender = st.selectbox("성별", [control_dict["gender"][i] for i in control_dict["gender"]])
        age = st.selectbox("연령층", [control_dict["age"][i] for i in control_dict["age"]])
        user_input_product = st.text_input(
            label = "상품명",
            value = "바나나 우유",
            placeholder = "please enter product"
        )
        user_input_keyword = st.text_input(
            label = "키워드",
            value = "달콤함,행복함",
            placeholder = "please enter keyword"
        )
        
        if st.form_submit_button(label='광고 카피 생성'):
            system_input, user_input = make_command(
                control_dict = control_dict,
                example_dict = example_dict,
                # example_flag = example_flag,
                copy_type = copy_type,
                product = user_input_product,
                key = user_input_keyword,
                gender = {v:k for k,v in control_dict["gender"].items()}[gender],
                age = {v:k for k,v in control_dict["age"].items()}[age],
                TM = {v:k for k,v in control_dict["TM"].items()}[TM],
                # max_num = max_num
            )
            
            # print(system_input)
            # print("-"*30)
            # print(user_input)
            
            result, result_org = model.execute(system_input, user_input) # model_dict[model]
            result = result[3:].replace("]","").replace('"', "").replace("\\n","").replace("\\","")
            st.write("생성된 광고 카피")
            st.write(result)
            st.write("-"*30)
            st.write("사용된 명령어")
            st.write(system_input + "\n\n### 사용자 입력\n" + user_input)
            
            with open(backup_path + "/log.log", "a")as f:
                f.write(str(datetime.now()) + "\n")
                # f.write(f"모델: {model}\n")
                # f.write(f"톤앤매너 예제 삽입 여부: {example_flag}\n")
                # f.write(f"생성할 예제 갯수: {max_num}\n")
                f.write(f"카피 유형: {copy_type}\n")
                f.write(f"톤앤매너: {TM}\n")
                f.write(f"성별: {gender}\n")
                f.write(f"연령층: {age}\n")
                f.write(f"상품명: {user_input_product}\n")
                f.write(f"키워드: {user_input_keyword}\n")
                f.write(f"생성된 광고 카피: {result}\n")
                f.write("-"*30 + '\n')

if __name__=="__main__":
    main()

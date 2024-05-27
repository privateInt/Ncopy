# -*- coding: utf-8 -*-

import requests
import streamlit as st

class CompletionExecutor:
    def __init__(self, host, host_add, api_key, api_key_primary_val, request_id):
        self._host = host
        self._host_add = host_add
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, system_input:str, user_input:str):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        
        preset_text = [{"role":"system","content":f"{system_input}"},{"role":"user","content":f"{user_input}"}]
        
        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 1024,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': ['\",'],
            'includeAiFilters': True,
            'seed': 0
        }
        
        text_lst = []
        with requests.post(self._host + self._host_add,
                           headers=headers, json=request_data, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    text_lst.append(line.decode("utf-8"))
        result = text_lst[text_lst.index("event:result")+1]
        
        start_idx = result.find("content") + len('"content":')
        end_idx = result.find("inputLength") - len('"},"')
        
        return result[start_idx: end_idx], result
    
def make_control_dict(
    head:str,
    body:str,
    base:str,
    review:str,
    action:str,
    question:str,
    humor:str,
    base_desc:str,
    review_desc:str,
    action_desc:str,
    question_desc:str,
    humor_desc:str,
    male:str,
    female:str,
    no_gender:str,
    juvenile:str,
    twenties_thirties:str,
    forties_fifties:str,
    senior:str,
    no_age:str,
    # max_num:int
):
    control_dict = {
        "type": {
            "head": head,
            "body": body
        },
        "TM": {
            "base": base,
            "review": review,
            "action": action,
            "question": question,
            "humor": humor
        },
        "TM_description": {
            "base": base_desc,
            "review": review_desc,
            "action": action_desc,
            "question": question_desc,
            "humor": humor_desc
        },
        "gender": {
            "no_gender": no_gender,
            "male": male,
            "female": female,
        },
        "age":{
            "no_age": no_age,
            "juvenile": juvenile,
            "twenties_thirties": twenties_thirties,
            "forties_fifties": forties_fifties,
            "senior": senior,
        },
        # "max_num":[i+1 for i in range(max_num)]
    }
    
    return control_dict

class Example_frame:
    def __init__(self, control_dict:dict):
        self.control_dict = control_dict
        
    def insert(self, product:str, key:str, copy:str, gender:str, age:str, TM:str):
        example = f"""상품: {product},
키워드: {key},
광고 카피 소비자 주 성별: {self.control_dict["gender"][gender]},
광고 카피 소비자 주 연령층: {self.control_dict["age"][age]},
톤앤매너: {self.control_dict["TM"][TM]},
광고카피: {copy}"""
        return example

def make_example_dict(control_dict:dict):
    example_frame = Example_frame(control_dict)
    head_base_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"공부하다 지칠 때, 친구들과 함께 즐기는 달달한 바나나 우유 한 잔! 행복한 하루!\"]",
        gender = "male",
        age = "juvenile",
        TM = "base")
    head_base_2 = example_frame.insert(
        product = "냉면",
        key = "쫄깃",
        copy = "[\"냉면 맛집 굳이 찾아가지 않아도 돼, 쫄깃한 냉면! 우리 집이 맛집이니까!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "base")
    head_base_3 = example_frame.insert(
        product = "멀티비타민",
        key = "에너지",
        copy = "[\"중년 남성의 건강을 책임지는 멀티비타민으로 더 활기차게! 더 건강하게!\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "base")
    head_base_4 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"힘없는 날엔 달콤한 바나나 우유 한 모금, 기운이 펄펄 나네!\"]",
        gender = "female",
        age = "senior",
        TM = "base")
    
    head_review_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"바나나 우유 먹어봤는데, 시험기간 스트레스가 싹 날아갔어요! 바나나 우유 한잔으로 행복 되찾으세요!\"]",
        gender = "male",
        age = "juvenile",
        TM = "review")
    head_review_2 = example_frame.insert(
        product = "MZ청바지",
        key = "트렌디함",
        copy = "[\"MZ청바지! 제가 입어보니 다양한 스타일에도 잘 어울리더라고요!. 스타일링 고민엔 MZ청바지!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "review")
    head_review_3 = example_frame.insert(
        product = "현대자동차",
        key = "안전, 가족, 승차감",
        copy = "[\"현대자동차 시승해보니 승차감이 편안합니다. 가족과 안전한 여행을 꿈꾸신다면 현대자동차가 정답입니다.\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "review")
    head_review_4 = example_frame.insert(
        product = "멀티비타민",
        key = "에너지",
        copy = "[\"자식들이 권해서 멀티비타민을 먹기 시작했어요. 이제 멀티비타민 없는 생활은 꿈도 꿀 수 없네요.\"]",
        gender = "female",
        age = "senior",
        TM = "review")
    
    head_action_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"바나나 우유 1+1 행사! 달콤함도 행복도 1+1!\"]",
        gender = "male",
        age = "juvenile",
        TM = "action")
    head_action_2 = example_frame.insert(
        product = "멀티비타민",
        key = "에너지",
        copy = "[\"피부 건강을 지켜주는 멀티비타민을 40% 할인된 가격에 살 수 있어요! 지금 바로 만나보세요!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "action")
    head_action_3 = example_frame.insert(
        product = "닭꼬치",
        key = "간편함",
        copy = "[\"간단한 술안주로 안성맞춤! 닭꼬치 밀키트 1+1 행사 중! 지금 바로 전화하세요!\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "action")
    head_action_4 = example_frame.insert(
        product = "연양갱",
        key = "달콤함",
        copy = "[\"어르신들이 자주 찾는 연양갱. 40% 할인된 가격으로 효도하세요.\"]",
        gender = "female",
        age = "senior",
        TM = "action")
    
    head_question_1 = example_frame.insert(
        product = "MZ운동화",
        key = "멋",
        copy = "[\"멋있어 지고 싶어? MZ운동화를 신어봐!\"]",
        gender = "male",
        age = "juvenile",
        TM = "question")
    head_question_2 = example_frame.insert(
        product = "MZ청바지",
        key = "트렌디함",
        copy = "[\"어디 트렌디한 청바지 없나요? 바로 여기! MZ청바지!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "question")
    head_question_3 = example_frame.insert(
        product = "멀티비타민",
        key = "피로",
        copy = "[\"매일 똑같은 피로를 견디시는 건 지루한 일이겠죠? 멀티비타민으로 변화를 만들어보세요!\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "question")
    head_question_4 = example_frame.insert(
        product = "OO암보험",
        key = "나이",
        copy = "[\"암보험에 가입하려는데 나이가 걱정되신다고요? OO암보험에서 나이는 숫자에 불과합니다. 지금 바로 가입하세요.\"]",
        gender = "female",
        age = "senior",
        TM = "question")
    
    head_humor_1 = example_frame.insert(
        product = "파운데이션",
        key = "안착",
        copy = "[\"진짜 착한 건 안착한 거야. 피부에 안착, 완벽히 밀착.\"]",
        gender = "female",
        age = "juvenile",
        TM = "humor")
    head_humor_2 = example_frame.insert(
        product = "구직 사이트",
        key = "직급",
        copy = "[\"매출 3000% 목표 달성을 외치는 그대는 사장인가 제사장인가?\"]",
        gender = "male",
        age = "twenties_thirties",
        TM = "humor")
    head_humor_3 = example_frame.insert(
        product = "김치말이 국수",
        key = "여름",
        copy = "[\"올여름은 김치말이지 말입니다.\"]",
        gender = "female",
        age = "forties_fifties",
        TM = "humor")
    head_humor_4 = example_frame.insert(
        product = "그릇",
        key = "삶",
        copy = "[\"그릇된 삶을 살 것인가. 큰 그릇이 되는 삶을 살 것인가.\"]",
        gender = "male",
        age = "senior", 
        TM = "humor")
    
    body_base_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"달콤한 바나나 우유 한 잔으로 행복한 하루를 시작해보세요! 신선한 바나나와 부드러운 우유가 만나 탄생한 바나나 우유는 특유의 달콤한 맛과 향으로 많은 사람들에게 사랑받고 있습니다. 아침 식사 대용이나 간식으로 즐기기에 딱 좋은 바나나 우유 한잔이면 에너지 충전 완료! 학업과 일상에 지친 청소년들에게 달콤한 휴식을 선물해 줄거예요.\"]",
        gender = "male",
        age = "juvenile",
        TM = "base")
    body_base_2 = example_frame.insert(
        product = "MZ청바지",
        key = "트렌디함",
        copy = "[\"MZ세대의 자유로운 감성과 개성을 담은 MZ청바지! 최신 트렌드를 반영한 다양한 디자인과 컬러로, 언제 어디서나 돋보이는 스타일을 완성해보세요. 하이퀄리티 소재와 꼼꼼한 마감처리로 높은 퀄리티를 자랑하며, 편안한 착용감으로 일상생활에서도 부담없이 즐길 수 있는 MZ청바지. 지금 바로 만나보세요!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "base")
    body_base_3 = example_frame.insert(
        product = "현대자동차",
        key = "안전, 가족",
        copy = "[\"안전한 드라이빙으로 가족을 지켜주세요. 현대자동차는 가족의 소중함을 알고 있습니다. 현대자동차의 선진적인 안전 기술과 첨단 시스템은 길 위에서의 모든 여정을 더욱 안전하고 신뢰성 있게 만들어줍니다. 우리는 운전자와 승객의 안전을 위해 끊임없이 연구하며 혁신하고 있습니다. 가족과 함께하는 모든 순간을 더욱 특별하게 만들어줄 현대자동차와 함께하세요.\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "base")
    body_base_4 = example_frame.insert(
        product = "멀티비타민",
        key = "에너지",
        copy = "[\"건강한 노후를 준비하는 지금, 꼭 필요한 영양소를 놓치지 마세요. 중년 이후에는 체내 영양소 흡수율이 떨어지기 때문에 부족한 영양소를 채워줘야 합니다. 멀티비타민은 하루 한 알 섭취로 간편하게 다양한 영양소를 보충할 수 있어 건강한 노후를 준비하는 데 도움을 줍니다. 활력 있는 일상을 원하는 분들에게 적극 추천 드립니다.\"]",
        gender = "female",
        age = "senior",
        TM = "base")
    
    body_review_1 = example_frame.insert(
        product = "파운데이션",
        key = "트러블",
        copy = "[\"파운데이션 유목민이었던 제가 드디어 정착템을 찾았습니다! 바로 이 제품인데요. 피부 트러블이 심한 편이라 아무거나 못 쓰는데, 이건 성분이 순해서 그런지 자극이 전혀 없더라구요. 발림성도 좋아서 부드럽게 발리고, 밀착력도 좋아서 들뜨거나 밀리지 않아요. 커버력도 기대 이상이라 웬만한 잡티는 다 가려지더라구요. 지속력도 좋아서 아침에 바르면 저녁까지 멀쩡해요! 덕분에 요즘은 피부 좋다는 소리 많이 듣고 있어요. 트러블 때문에 고민이신 분들께 강력 추천합니다!\"]",
        gender = "female",
        age = "juvenile",
        TM = "review")
    body_review_2 = example_frame.insert(
        product = "MZ청바지",
        key = "트렌디함",
        copy = "[\"MZ청바지는 정말 트렌디함을 살린 최고의 선택이에요. 여기서 트렌디함은 단순한 스타일을 넘어서 독특한 매력을 지칭하는데요. 이 청바지는 유행을 주도하는 패션 트렌드를 완벽하게 반영하면서도 개성적인 느낌을 줘요. 고급스러운 디자인과 편안한 착용감이 조화를 이루어 여러분의 스타일에 환상적인 변화를 불러옵니다. MZ청바지로 당신만의 독특한 패션 센스를 표현하며, 어디서든 눈에 띄는 멋을 자랑해보세요.\"]",
        gender = "female", 
        age = "twenties_thirties", 
        TM = "review")
    body_review_3 = example_frame.insert(
        product = "현대자동차", 
        key = "안전, 가족", 
        copy = "[\"현대자동차의 안전성은 진정한 보물입니다. 가족을 위해 운전하는데 있어서 어떤 것보다 중요한 것은 바로 안전입니다. 그래서 현대자동차를 선택한 것이었죠. 가장 최신 기술로 보호되는 이 자동차는 운전자와 승객의 안전을 위한 완벽한 선택이었습니다. 특히 길 위에서의 안정성과 신뢰성은 절대 어딘가에 뒤떨어지지 않는 것 같아요. 가족과 함께하는 모든 여정이 더욱 평안하고 안전한 이유는 바로 현대자동차 때문입니다.\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "review")
    body_review_4 = example_frame.insert(
        product = "연양갱",
        key = "부드러움",
        copy = "[\"나이가 들면 이가 약해지기 마련이죠. 그런 저에게 안성맞춤인 간식이 바로 연양갱입니다. 입 안에서 살살 녹는 부드러운 식감과 과하게 달지 않은 적당한 단맛이 참 좋아요. 먹고 나면 속도 든든해져서 간단한 요깃거리로도 제격입니다. 포장도 깔끔하고 고급스러워서 주변 사람들에게 선물하기도 좋고요. 역시 전통 있는 과자는 뭐가 달라도 다르네요!\"]",
        gender = "male",
        age = "senior",
        TM = "review")
    
    body_action_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"지루한 일상! 달콤한 바나나 우유 한 잔으로 시작해 보세요! 피곤한 아침, 무거운 가방, 끝나지 않는 숙제. 지루한 일상에 질렸다면, 달콤한 바나나 우유 한 잔 어떠세요? 신선한 바나나와 부드러운 우유가 만나 탄생한 바나나 우유는 특유의 달콤한 맛과 향으로 여러분의 하루를 행복하게 만들어줄거예요. 바나나는 에너지를 보충해주고, 우유는 칼슘과 단백질을 공급해주어 건강에도 좋아요. 지금 바로 편의점에서 만나보세요!\"]",
        gender = "male",
        age = "juvenile",
        TM = "action")
    body_action_2 = example_frame.insert(
        product = "MZ청바지",
        key = "트렌디함",
        copy = "[\"MZ청바지, 지금 바로 입고 나만의 개성을 표현하세요! 빠르게 변하는 패션 트렌드 속에서 나만의 스타일을 찾는 건 쉽지 않은 일이죠. 하지만 MZ 청바지와 함께라면 이야기가 달라집니다. 다양한 디자인과 색상으로 구성된 MZ 청바지는 여러분의 취향과 개성을 완벽하게 살려줍니다. 게다가 고급 원단을 사용하여 편안한 착용감까지 보장하죠. 더 이상 고민하지 마세요. MZ 청바지와 함께라면 누구나 트렌디한 패션 아이콘이 될 수 있습니다. 지금 바로 매장에서 만나보세요!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "action")
    body_action_3 = example_frame.insert(
        product = "현대자동차",
        key = "안전, 가족",
        copy = "[\"가족을 지키는 선택, 현대자동차와 함께하세요. 도로 위에서의 안전은 우리의 최우선 과제입니다. 현대의 최신 안전 기술과 품질로 가득한 차량들은 당신의 소중한 가족을 위한 완벽한 파트너가 될 것입니다. 가족과 함께하는 모든 순간을 더욱 안전하게 만들어보세요.\"]",
        gender = "male",
        age = "forties_fifties",
        TM = "action")
    body_action_4 = example_frame.insert(
        product = "멀티비타민",
        key = "에너지",
        copy = "[\"나이가 들수록 부족해지는 영양소, 멀티비타민으로 채우세요! 세월이 흘러갈수록 우리 몸은 다양한 영양소를 필요로 합니다. 하지만 노화로 인해 영양소 흡수율이 감소하면서, 충분한 영양소를 섭취하기 어려워집니다. 멀티비타민은 이러한 문제를 해결해줄 수 있는 가장 간단한 방법입니다. 13가지 비타민과 미네랄을 한 번에 섭취할 수 있어, 부족한 영양소를 보충하고 건강한 노후를 보낼 수 있도록 도와줍니다. 지금 바로 시작하세요!\"]",
        gender = "female",
        age = "senior",
        TM = "action")
    
    body_question_1 = example_frame.insert(
        product = "바나나 우유",
        key = "달콤함, 행복함",
        copy = "[\"바나나 우유 좋아하세요? 지루한 일상에 잠깐 멈춰서 달콤한 휴식을 즐겨보는 건 어떨까요? 달콤함 가득한 바나나 우유 한 잔으로 행복한 하루를 시작해보세요! 아침 식사 대용이나 간식으로 딱 좋은 이 상품은 신선한 바나나와 고소한 우유의 조합으로 여러분을 기쁘게 만들어줄 거예요.\"]",
        gender = "male",
        age = "juvenile",
        TM = "question")
    body_question_2 = example_frame.insert(
        product = "떡볶이",
        key = "다이어트, 스트레스",
        copy = "[\"떡볶이를 먹으면 살이 찔까봐 걱정이신가요? 떡볶이는 대표적인 고칼로리 음식 중 하나이지만, 적절한 양과 방법으로 섭취하면 오히려 다이어트에 도움이 될 수 있다는 사실! 떡볶이에 들어가는 다양한 채소와 단백질이 풍부한 어묵, 계란 등을 함께 먹으면 영양 균형을 맞출 수 있고, 포만감을 높여 과식을 방지할 수 있어요. 무엇보다 맛있게 먹으며 스트레스를 해소할 수 있으니, 다이어트 한다고 무작정 참지 말고 떡볶이를 즐겨보세요!\"]",
        gender = "female",
        age = "twenties_thirties",
        TM = "question")
    body_question_3 = example_frame.insert(
        product = "냉면",
        key = "둥지",
        copy = "[\"더운 여름, 시원한 냉면 한 그릇 생각나지 않으세요? 둥지처럼 말아 올린 면 위에 새콤한 육수를 붓고, 아삭한 오이와 무절임, 삶은 계란을 올려 먹는 냉면은 여름철 최고의 별미죠. 쫄깃한 면발과 깊은 육수의 맛이 어우러져 입안 가득 행복함을 느낄 수 있답니다. 집에서 간편하게 즐길 수 있는 냉면 밀키트로 이번 여름, 시원하게 보내보세요!\"]",
        gender = "female",
        age = "forties_fifties",
        TM = "question")
    body_question_4 = example_frame.insert(
        product = "암보험",
        key = "민폐, 짐",
        copy = "[\"나이가 들면 암 보험이 부담되시나요? 암보험은 나이가 들어갈수록 점점 비싸지고 가입이 어려워집니다. 혹시라도 암에 걸리면 가족들에게 민폐만 끼칠까 걱정이신가요? 이제 그런 부담 없이 든든한 암보험 하나 들어놓으세요. 저희 상품은 저렴한 가격으로도 높은 보장을 제공하여, 암 진단 시 치료비와 생활비를 충분히 지원해드립니다. 또한, 간편한 가입 절차와 신속한 보험금 지급으로 고객님의 편의를 최우선으로 생각합니다. 언제든지 문의 주시면 친절하게 상담해드리겠습니다.\"]",
        gender = "male",
        age = "senior",
        TM = "question")
    
    body_humor_1 = example_frame.insert(
        product = "바나나 우유",
        key = "반함",
        copy = "[\"풍부한 바나나 향과 부드러운 우유의 조화, 그 누구도 거부할 수 없는 매력! 바로 '바나나 우유'입니다. 이제 당신도 그 매력에 반하게 될 거에요. 언제나 상큼한 맛으로 당신의 입맛을 사로잡을 것입니다. 바나나 우유 한 잔으로 당신의 하루를 즐겁고 활기차게 시작해보세요. 바나나 우유 마시면 나한테 반하나?\"]",
        gender = "female",
        age = "juvenile",
        TM = "humor")
    body_humor_2 = example_frame.insert(
        product = "구직 사이트",
        key = "직급",
        copy = "[\"사사건건 감시하고 고자질하는 그대는 사원인가 감사원인가? 밥만 먹으면 방전되는 그대는 대리인가 밧데리인가? 신입 때 두 달 연속 밤새웠다는 그대는 과장인가 극과장인가? 침 튀기며 설교만 하는 그대는 차장인가 세차장인가? 일만 받으면 끌어안고 묵히는 그대는 국장인가 청국장인가? 책임질 일에는 나몰라라 하는 그대는 이사인가 남이사인가? 매출 3000% 목표 달성을 외치는 그대는 사장인가 제사장인가?\"]",
        gender = "male",
        age = "twenties_thirties",
        TM = "humor")
    body_humor_3 = example_frame.insert(
        product = "와퍼",
        key = "해산물",
        copy = "[\"게 있느냐! 게 있느냐! 게 아무도 없느냐? 게... 게냐? 게살의 진미를 맛보다. 대게 맛있다. 붉은대게와퍼. 차 세워! 세우라고, 세우라니까! 그냥 새우면 안 된다. 통새우만 된다. 새우의 자존심을 세우다. 맛의 자존심을 세우다. 통새우 와퍼.\"]",
        gender = "female",
        age = "forties_fifties",
        TM = "humor")
    body_humor_4 = example_frame.insert(
        product = "연양갱",
        key = "연약함",
        copy = "[\"나이가 들수록 연약해지신다고요? 그럴 땐 연양갱이죠! 부드러운 팥앙금이 입안에서 살살 녹는 그 맛, 한 번 맛보면 빠져나올 수 없을걸요? 달콤하고 진한 연양갱으로 마음뿐만 아니라 체력까지 든든하게 채워보세요.\"]",
        gender = "male",
        age = "senior",
        TM = "humor")
    
    example_dict = {
        "head": {
            "base": [head_base_1, head_base_2, head_base_3, head_base_4],
            "review": [head_review_1, head_review_2, head_review_3, head_review_4],
            "action": [head_action_1, head_action_2, head_action_3, head_action_4],
            "question": [head_question_1, head_question_2, head_question_3, head_question_4],
            "humor": [head_humor_1, head_humor_2, head_humor_3, head_humor_4]
        },
        "body": {
            "base": [body_base_1, body_base_2, body_base_3, body_base_4],
            "review": [body_review_1, body_review_2, body_review_3, body_review_4],
            "action": [body_action_1, body_action_2, body_action_3, body_action_4],
            "question": [body_question_1, body_question_2, body_question_3, body_question_4],
            "humor": [body_humor_1, body_humor_2, body_humor_3, body_humor_4]
        }
    }
    
    return example_dict
    
# \r- 광고 카피 소비자의 주 성별은 "{control_dict["gender"][gender]}"입니다.
# \r- 광고 카피 소비자의 주 연령층은 "{control_dict["age"][age]}"입니다.
# \r- 생성할 광고 카피의 개수는 "{str(max_num)}"개 입니다.
# \r- 생성된 광고 카피는 "1." 같은 숫자를 붙여 구분합니다.
def make_command(
    control_dict:dict,
    example_dict:dict,
    # example_flag:bool,
    copy_type:str,
    product:str,
    key:str,
    gender:str,
    age:str,
    TM:str,
    # max_num:int
):
    command = f"""### 지시사항
\r- 광고 카피를 작성하는 광고 기획자입니다. {control_dict["type"][copy_type]}를 작성합니다.
\r- 광고 카피의 길이가 중요한 요소입니다. 제시된 분량을 반드시 준수하세요.
\r- 광고 카피의 톤앤매너는 "{control_dict["TM"][TM]}"입니다.
\r- {control_dict["TM_description"][TM]}
\r- 주어진 상품명을 광고 카피에 반드시 포함합니다.
\r- 주어진 키워드의 주제, 분위기를 반영합니다.
\r- 생성된 광고 카피는 리스트에 담긴 형식으로 출력합니다."""
    
    # if example_flag:
    #     examples = "\n\n".join(example_dict[copy_type][TM])
    #     example = f"""\n\n### 예시\n{examples}"""
    # else:
    #     examples = "\n\n".join([each_list for TM in example_dict[copy_type] for each_list in example_dict[copy_type][TM]])
    #     example = f"""\n\n### 예시\n{examples}"""
        
    examples = "\n\n".join(example_dict[copy_type][TM])
    example = f"""\n\n### 예시\n{examples}"""
        
    system_input = command + example
        
    example_frame = Example_frame(control_dict)
    user_input = example_frame.insert(
        product = product, 
        key = key, 
        copy = "", 
        gender = gender, 
        age = age, 
        TM = TM) + ""
    
    return system_input, user_input
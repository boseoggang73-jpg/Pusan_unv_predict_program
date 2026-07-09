from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# ==========================================
# 2025학년도 실제 입시 결과 데이터베이스
# ==========================================
raw_admission_data = {
    "교과우수전형": [
        {"department": "물리교육과", "cut_50": 78.12, "cut_70": 77.73},
        {"department": "생물교육과", "cut_50": 78.51, "cut_70": 78.43},
        {"department": "수학교육과", "cut_50": 79.12, "cut_70": 78.97},
        {"department": "지구과학교육과", "cut_50": 78.39, "cut_70": 78.28},
        {"department": "화학교육과", "cut_50": 78.42, "cut_70": 78.36},
        {"department": "건축공학과", "cut_50": 78.39, "cut_70": 78.34},
        {"department": "건축학과", "cut_50": 78.65, "cut_70": 78.58},
        {"department": "조경학과", "cut_50": 77.61, "cut_70": 77.49},
        {"department": "도시공학과", "cut_50": 78.64, "cut_70": 78.55},
        {"department": "항공우주공학과", "cut_50": 78.65, "cut_70": 78.6},
        {"department": "해양학과", "cut_50": 78.23, "cut_70": 78.22},
        {"department": "지리교육과", "cut_50": 78.04, "cut_70": 77.9},
        {"department": "미디어커뮤니케이션학과", "cut_50": 78.89, "cut_70": 78.82},
        {"department": "정치외교학과", "cut_50": 78.71, "cut_70": 78.62},
        {"department": "공공정책학부", "cut_50": 78.9, "cut_70": 78.84},
        {"department": "행정학과", "cut_50": 79.02, "cut_70": 78.8},
        {"department": "교육학과", "cut_50": 78.73, "cut_70": 78.73},
        {"department": "특수교육과", "cut_50": 78.69, "cut_70": 78.67},
        {"department": "국어교육과", "cut_50": 78.86, "cut_70": 78.81},
        {"department": "영어교육과", "cut_50": 79.01, "cut_70": 78.82},
        {"department": "윤리교육과", "cut_50": 78.76, "cut_70": 78.74},
        {"department": "역사교육과", "cut_50": 78.55, "cut_70": 78.49},
        {"department": "일반사회교육과", "cut_50": 78.87, "cut_70": 78.87},
        {"department": "조선·해양공학과", "cut_50": 78.44, "cut_70": 78.36},
        {"department": "언어정보학과", "cut_50": 78.43, "cut_70": 78.31},
        {"department": "국어국문학과", "cut_50": 78.17, "cut_70": 78.16},
        {"department": "일어일문학과", "cut_50": 78.37, "cut_70": 78.37},
        {"department": "실내환경디자인학과(인문)", "cut_50": 78.18, "cut_70": 77.88},
        {"department": "의류학과(인문)", "cut_50": 78.18, "cut_70": 78.16},
        {"department": "첨단IT자율전공", "cut_50": 78.44, "cut_70": 78.34},
        {"department": "미래도시건축환경융합전공", "cut_50": 78.21, "cut_70": 78.07},
        {"department": "첨단소재자율전공", "cut_50": 78.35, "cut_70": 78.11},
        {"department": "첨단모빌리티자율전공", "cut_50": 78.57, "cut_70": 78.54},
        {"department": "정보컴퓨터공학부(디자인테크놀로지전공)", "cut_50": 78.67, "cut_70": 78.56},
        {"department": "응용생명융합학부", "cut_50": 77.69, "cut_70": 77.6},
        {"department": "첨단융합학부 스마트시티전공", "cut_50": 78.18, "cut_70": 77.97},
        {"department": "사학과", "cut_50": 78.48, "cut_70": 78.41},
        {"department": "철학과", "cut_50": 78.36, "cut_70": 78.35},
        {"department": "자유전공학부", "cut_50": 78.84, "cut_70": 78.65},
        {"department": "경영학과", "cut_50": 78.88, "cut_70": 78.75},
        {"department": "중어중문학과", "cut_50": 77.97, "cut_70": 77.89},
        {"department": "한문학과", "cut_50": 77.96, "cut_70": 77.92},
        {"department": "영어영문학과", "cut_50": 78.47, "cut_70": 78.41},
        {"department": "독어독문학과", "cut_50": 77.73, "cut_70": 77.56},
        {"department": "노어노문학과", "cut_50": 78.06, "cut_70": 77.85},
        {"department": "불어불문학과", "cut_50": 78.27, "cut_70": 78.2},
        {"department": "문헌정보학과", "cut_50": 78.65, "cut_70": 78.55},
        {"department": "심리학과", "cut_50": 78.45, "cut_70": 78.38},
        {"department": "고고학과", "cut_50": 78.15, "cut_70": 78.08},
        {"department": "사회학과", "cut_50": 78.69, "cut_70": 78.48},
        {"department": "간호학과", "cut_50": 78.95, "cut_70": 78.93},
        {"department": "예술문화영상학과", "cut_50": 78.66, "cut_70": 78.66},
        {"department": "스포츠과학과", "cut_50": 77.82, "cut_70": 77.75},
        {"department": "아동가족학과", "cut_50": 78.11, "cut_70": 77.77},
        {"department": "식품공학과", "cut_50": 77.8, "cut_70": 77.74},
        {"department": "식품영양학과", "cut_50": 78.61, "cut_70": 78.3},
        {"department": "수학과", "cut_50": 78.25, "cut_70": 78.15},
        {"department": "바이오환경에너지학과", "cut_50": 77.63, "cut_70": 77.46},
        {"department": "유기소재시스템공학과", "cut_50": 78.59, "cut_70": 78.41},
        {"department": "재료공학부", "cut_50": 78.96, "cut_70": 78.82},
        {"department": "IT응용공학과", "cut_50": 77.85, "cut_70": 77.8},
        {"department": "의예과", "cut_50": 79.95, "cut_70": 79.94},
        {"department": "정보컴퓨터공학부 컴퓨터공학전공", "cut_50": 78.87, "cut_70": 78.71},
        {"department": "정보컴퓨터공학부 인공지능전공", "cut_50": 78.83, "cut_70": 78.78},
        {"department": "첨단융합학부", "cut_50": 78.34, "cut_70": 78.26},
        {"department": "전기전자공학부 전자공학전공", "cut_50": 79.28, "cut_70": 79.22},
        {"department": "전기전자공학부 반도체공학전공", "cut_50": 79.06, "cut_70": 79.0},
        {"department": "통계학과", "cut_50": 78.73, "cut_70": 78.64},
        {"department": "물리학과", "cut_50": 78.14, "cut_70": 78.06},
        {"department": "대기환경과학과", "cut_50": 78.39, "cut_70": 78.36},
        {"department": "지질환경과학과", "cut_50": 78.13, "cut_70": 78.1},
        {"department": "사회기반시스템공학과", "cut_50": 78.17, "cut_70": 78.09},
        {"department": "환경공학과", "cut_50": 78.64, "cut_70": 78.48},
        {"department": "전기전자공학부 전기공학전공", "cut_50": 79.1, "cut_70": 79.05},
        {"department": "의생명융합공학부", "cut_50": 78.23, "cut_70": 77.95},
        {"department": "기계공학부", "cut_50": 78.97, "cut_70": 78.85},
        {"department": "바이오산업기계공학과", "cut_50": 77.75, "cut_70": 77.68},
        {"department": "경제학부", "cut_50": 78.72, "cut_70": 78.65},
        {"department": "관광컨벤션학과", "cut_50": 77.91, "cut_70": 77.83},
        {"department": "무역학부", "cut_50": 78.63, "cut_70": 78.59},
        {"department": "사회복지학과", "cut_50": 78.35, "cut_70": 78.27},
        {"department": "국제학부", "cut_50": 78.58, "cut_70": 78.56},
        {"department": "산업공학과", "cut_50": 78.91, "cut_70": 78.8},
        {"department": "고분자공학과", "cut_50": 78.45, "cut_70": 78.3},
        {"department": "화공생명공학과", "cut_50": 79.3, "cut_70": 79.12},
        {"department": "원예생명과학과", "cut_50": 77.15, "cut_70": 77.15},
        {"department": "생명과학과", "cut_50": 78.87, "cut_70": 78.3},
        {"department": "미생물학과", "cut_50": 78.64, "cut_70": 78.56},
        {"department": "분자생물학과", "cut_50": 78.83, "cut_70": 78.67},
        {"department": "식품자원경제학과", "cut_50": 78.09, "cut_70": 78.04},
        {"department": "화학과", "cut_50": 78.68, "cut_70": 78.62}
    ],
    "교과지역전형": [
        {"department": "학석사통합과정(한의학과)", "cut_50": 79.58, "cut_70": 79.57},
        {"department": "건축학과", "cut_50": 78.57, "cut_70": 78.53},
        {"department": "항공우주공학과", "cut_50": 78.7, "cut_70": 78.7},
        {"department": "해양학과", "cut_50": 78.1, "cut_70": 78.1},
        {"department": "미디어커뮤니케이션학과", "cut_50": 78.53, "cut_70": 78.49},
        {"department": "정치외교학과", "cut_50": 78.47, "cut_70": 78.44},
        {"department": "행정학과", "cut_50": 78.95, "cut_70": 78.94},
        {"department": "조선·해양공학과", "cut_50": 78.54, "cut_70": 78.51},
        {"department": "첨단IT자율전공", "cut_50": 78.44, "cut_70": 78.23},
        {"department": "첨단모빌리티자율전공", "cut_50": 78.51, "cut_70": 78.51},
        {"department": "자유전공학부", "cut_50": 78.76, "cut_70": 78.62},
        {"department": "경영학과", "cut_50": 78.88, "cut_70": 78.79},
        {"department": "문헌정보학과", "cut_50": 78.61, "cut_70": 78.56},
        {"department": "심리학과", "cut_50": 78.7, "cut_70": 78.46},
        {"department": "사회학과", "cut_50": 78.6, "cut_70": 78.53},
        {"department": "치의예과", "cut_50": 79.74, "cut_70": 79.7},
        {"department": "간호학과", "cut_50": 79.2, "cut_70": 79.13},
        {"department": "약학부", "cut_50": 79.67, "cut_70": 79.64},
        {"department": "바이오환경에너지학과", "cut_50": 77.77, "cut_70": 77.66},
        {"department": "재료공학부", "cut_50": 78.88, "cut_70": 78.88},
        {"department": "의예과", "cut_50": 79.97, "cut_70": 79.93},
        {"department": "정보컴퓨터공학부 컴퓨터공학전공", "cut_50": 79.13, "cut_70": 78.87},
        {"department": "첨단융합학부", "cut_50": 78.37, "cut_70": 78.26},
        {"department": "전기전자공학부 전자공학전공", "cut_50": 79.16, "cut_70": 79.06},
        {"department": "전기전자공학부 반도체공학전공", "cut_50": 78.89, "cut_70": 78.85},
        {"department": "통계학과", "cut_50": 78.61, "cut_70": 78.58},
        {"department": "물리학과", "cut_50": 78.54, "cut_70": 78.53},
        {"department": "대기환경과학과", "cut_50": 78.59, "cut_70": 78.27},
        {"department": "지질환경과학과", "cut_50": 77.97, "cut_70": 77.97},
        {"department": "IT응용공학과", "cut_50": 78.24, "cut_70": 78.02},
        {"department": "생명환경화학과", "cut_50": 77.53, "cut_70": 77.53},
        {"department": "전기전자공학부 전기공학전공", "cut_50": 79.16, "cut_70": 79.12},
        {"department": "의생명융합공학부", "cut_50": 78.75, "cut_70": 78.3},
        {"department": "기계공학부", "cut_50": 78.96, "cut_70": 78.91},
        {"department": "경제학부", "cut_50": 78.75, "cut_70": 78.7},
        {"department": "관광컨벤션학과", "cut_50": 78.45, "cut_70": 78.45},
        {"department": "무역학부", "cut_50": 78.53, "cut_70": 78.49},
        {"department": "사회복지학과", "cut_50": 78.14, "cut_70": 78.05},
        {"department": "사회기반시스템공학과", "cut_50": 78.11, "cut_70": 78.05},
        {"department": "화공생명공학과", "cut_50": 79.12, "cut_70": 79.09},
        {"department": "생명과학과", "cut_50": 79.01, "cut_70": 78.87},
        {"department": "미생물학과", "cut_50": 78.51, "cut_70": 78.49},
        {"department": "분자생물학과", "cut_50": 78.59, "cut_70": 78.5},
        {"department": "화학과", "cut_50": 78.77, "cut_70": 78.74}
    ]
}

pass_data = {"교과우수전형": {}, "교과지역전형": {}}
for track, items in raw_admission_data.items():
    for item in items:
        pass_data[track][item["department"]] = {"50_cut": item["cut_50"], "70_cut": item["cut_70"]}

# 교과우수/지역전형용 새로운 변환 점수
def get_standard_converted_score(grade):
    if grade == 1: return 100.0
    elif grade == 2: return 98.0
    elif grade == 3: return 95.0
    elif grade == 4: return 90.0
    else: return 0.0

# 탐구전형용 기존 변환 점수
def get_tamgu_converted_score(grade):
    if grade == 1: return 99.5
    elif grade == 2: return 97.5
    elif grade == 3: return 94.5
    elif grade == 4: return 90.0
    else: return 0.0

import math

def calculate_probability(my_score, cut_50, cut_70):
    # 50% 컷과 70% 컷의 점수 차이 계산
    diff = cut_50 - cut_70
    
    # 50컷과 70컷이 같거나 역전된 오류 데이터일 경우를 위한 최소 간격 보정
    if diff <= 0:
        diff = 0.1 

    # 1단계: 90% 컷(합격자 하위 10% 수준) 예측
    # 50% -> 70%로 떨어질 때의 점수 격차를 한 번 더 빼서 하위권 커트라인을 예상합니다.
    cut_90 = cut_70 - diff
    
    # 2단계: 목표 확률에 대한 Z-score 고정값
    # 예상 90% 컷 = 50% 합격 확률 (Z = 0.0)
    # 50% 컷 = 90% 합격 확률 (Z = 1.2816)
    z_90_prob = 1.2816
    z_50_prob = 0.0
    
    # 3단계: 가상 분포(평균과 표준편차) 계산
    mu = cut_90  # 50% 확률이 뜨는 기준점은 이제 '예상 90% 컷'입니다.
    sigma = (cut_50 - mu) / z_90_prob
    
    # 내 점수의 Z-score 계산
    my_z = (my_score - mu) / sigma
    
    # 누적분포함수(CDF)를 통해 0~1 사이 확률 도출 후 100을 곱함
    probability = 0.5 * (1 + math.erf(my_z / math.sqrt(2)))
    final_prob = probability * 100
    
    # 확률이 0% 미만이나 100% 초과로 표기되지 않도록 범위 제한
    final_prob = max(0.0, min(100.0, final_prob))
    
    return round(final_prob, 2)

@app.route('/majors', methods=['GET'])
def get_majors():
    return jsonify({
        "교과우수전형": [item["department"] for item in raw_admission_data["교과우수전형"]],
        "교과지역전형": [item["department"] for item in raw_admission_data["교과지역전형"]]
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    selected_track = data.get('selected_track')      
    selected_weight = data.get('selected_weight')    
    selected_major = data.get('selected_major')
    grade_data = data.get('grade_data', [])
    
    if not selected_major:
        return jsonify({"success": False, "message": "지원 학과를 선택해 주세요."})
    if not grade_data:
        return jsonify({"success": False, "message": "성적을 하나 이상 입력해 주세요."})
        
    # 성적 처리 및 로직 분기
    if selected_track in ["교과우수전형", "교과지역전형"]:
        total_weighted_score = 0.0
        total_credits = 0
        
        for item in grade_data:
            grade, credit, count = int(item["grade"]), int(item["credit"]), int(item["count"])
            for _ in range(count):
                total_weighted_score += get_standard_converted_score(grade) * credit
                total_credits += credit
                
        if total_credits == 0:
            score_100, final_80_score = 0, 0
        else:
            score_100 = total_weighted_score / total_credits
            final_80_score = score_100 * 0.8
            
    else: # 탐구전형 기존 로직 유지
        subjects_data = {
            "국어": {"grades": [], "credits": [], "cnt_1st": 0},
            "수학": {"grades": [], "credits": [], "cnt_1st": 0},
            "영어": {"grades": [], "credits": [], "cnt_1st": 0},
            "사회": {"grades": [], "credits": [], "cnt_1st": 0},
            "과학": {"grades": [], "credits": [], "cnt_1st": 0},
            "국사": {"grades": [], "credits": [], "cnt_1st": 0}, # 탐구에선 미반영될 수 있음
            "기타": {"grades": [], "credits": [], "cnt_1st": 0}
        }
        total_1st = 0
        
        for item in grade_data:
            subj, grade, credit, count = item["subject"], int(item["grade"]), int(item["credit"]), int(item["count"])
            for _ in range(count):
                if subj in subjects_data:
                    subjects_data[subj]["grades"].append(grade)
                    subjects_data[subj]["credits"].append(credit)
                    if grade == 1:
                        subjects_data[subj]["cnt_1st"] += 1
                        total_1st += 1
                        
        def calc_avg(subj_key):
            g, c = subjects_data[subj_key]["grades"], subjects_data[subj_key]["credits"]
            if sum(c) == 0: return 0.0
            return sum(get_tamgu_converted_score(gv) * cv for gv, cv in zip(g, c)) / sum(c)

        avg_kor = calc_avg("국어")
        avg_mat = calc_avg("수학")
        avg_eng = calc_avg("영어")
        avg_soc = calc_avg("사회")
        avg_sci = calc_avg("과학")
        
        if selected_weight == "인문, 사회계열":
            score_A = (avg_kor * 0.3) + (avg_mat * 0.1) + (avg_eng * 0.3) + (avg_soc * 0.3)
            max_1st_count = max(subjects_data["국어"]["cnt_1st"], subjects_data["영어"]["cnt_1st"], subjects_data["사회"]["cnt_1st"])
        elif selected_weight == "자연계열":
            score_A = (avg_kor * 0.1) + (avg_mat * 0.4) + (avg_eng * 0.1) + (avg_sci * 0.4)
            max_1st_count = max(subjects_data["수학"]["cnt_1st"], subjects_data["과학"]["cnt_1st"])
        else:
            score_A, max_1st_count = 0.0, 0
            
        score_B = min(max_1st_count * 0.05, 0.5)
        score_100 = score_A + score_B
        final_80_score = score_100 * 0.8
    
    # 결과 비교
    lookup_track = "교과우수전형" if selected_track == "탐구전형" else selected_track
    try:
        cut_50 = pass_data[lookup_track][selected_major]["50_cut"]
        cut_70 = pass_data[lookup_track][selected_major]["70_cut"]
        is_dummy = False
    except KeyError:
        cut_50, cut_70 = 78.00, 77.50
        is_dummy = True
        
    prob = calculate_probability(final_80_score, cut_50, cut_70)
    
    return jsonify({
        "success": True,
        "score_100": f"{score_100:.4f}",
        "score_80": f"{final_80_score:.4f}",
        "probability": prob,
        "cut_50": cut_50,
        "cut_70": cut_70,
        "is_dummy": is_dummy
    })

if __name__ == '__main__':
    import os
    # Render가 정해주는 포트 번호를 가져오고, 없으면 기본값으로 5000을 쓴다는 뜻이야!
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0'을 붙여줘야 외부 사람들이 네 사이트에 접속할 수 있어.
    app.run(host='0.0.0.0', port=port)
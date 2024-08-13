import schedule
import time
from request_sender import send_get_request, send_post_request
from association_calculator import calculate_association
from surprise_model import build_collaborative_filtering_model, recommend_exhibitions_for_user
import configparser
import json

def job():
    # 설정 파일 읽기
    print("협업 필터링을 시작합니다.")
    config = configparser.ConfigParser()
    config.read('config.ini')

    # 사용자 정보 가져오기
    users_url = config['Endpoints']['users_url']
    user_infos = send_get_request(users_url)

    # 전시회 정보 가져오기
    exhibitions_url = config['Endpoints']['exhibitions_url']
    exhibition_infos = send_get_request(exhibitions_url)

    # 유저와 전시회 간의 연관성 계산
    association_infos = calculate_association(user_infos, exhibition_infos)

    # 협업 필터링 모델 훈련
    collaborative_filtering_model = build_collaborative_filtering_model(association_infos)

    # 결과를 저장할 리스트 초기화
    recommendations = []

    # 각 사용자에 대해 전시회 추천 받기
    for user_info in user_infos:
        user_id = user_info['user_id']
        recommended_exhibitions = recommend_exhibitions_for_user(collaborative_filtering_model, user_id)

        # 해당 사용자의 추천 전시회를 JSON 형식으로 구성하여 리스트에 추가
        user_recommendations = {
            'user_id': user_id,
            'recommendations': [{'exhibition_id': exhibition_id, 'weight': weight} for exhibition_id, weight in recommended_exhibitions]
        }
        recommendations.append(user_recommendations)

    # JSON 형태로 변환하여 Spring Boot로 결과를 전송
    recommendations_url = config['Endpoints']['recommendations_url']
    send_post_request(recommendations_url, json.dumps(recommendations))
    
    print("협업 필터링이 종료되었습니다.")

# 설정 파일에서 시간 읽기
config = configparser.ConfigParser()
config.read('config.ini')
schedule_time = config['Schedule']['time']

# 매일 설정된 시간에 job() 함수를 실행하도록 스케줄러 설정
schedule.every().day.at(schedule_time).do(job)

# 계속해서 스케줄러를 실행
while True:
    schedule.run_pending()
    print("실행중...")
    time.sleep(1)
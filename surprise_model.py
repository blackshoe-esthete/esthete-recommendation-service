from surprise import Reader, Dataset
from surprise import KNNBasic

def build_collaborative_filtering_model(association_list):
    # Surprise 데이터셋 생성
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(association_list, reader)

    # Surprise 모델 초기화 및 훈련
    model = KNNBasic(sim_options={'name': 'cosine', 'user_based': True})
    trainset = data.build_full_trainset()
    model.fit(trainset)

    return model

def recommend_exhibitions_for_user(model, userID, k=20):
    testUserInnerID = model.trainset.to_inner_uid(userID)
    sim_scores = model.sim[testUserInnerID]

    # 이웃한 사용자들의 전시회 평가 정보를 가져옴
    neighbors = model.get_neighbors(testUserInnerID, k=k)
    recommended_exhibitions = {}  # 중복된 전시회를 방지하기 위해 딕셔너리를 사용

    # 각 이웃 사용자가 선호하는 전시회를 가져와서 추천 리스트에 추가
    for neighbor in neighbors:
        neighbor_ratings = model.trainset.ur[neighbor]
        for exhibitionID, rating in neighbor_ratings:
            # 이미 추가된 전시회는 중복을 피하기 위해 가중치를 평균내어 업데이트
            if exhibitionID in recommended_exhibitions:
                recommended_exhibitions[exhibitionID].append(rating)
            else:
                recommended_exhibitions[exhibitionID] = [rating]

    # 중복된 전시회를 제거하고 각 전시회의 가중치를 평균내어 업데이트
    for exhibitionID, ratings in recommended_exhibitions.items():
        weight = sum(ratings) / len(ratings)
        # 소수 넷째 자리에서 반올림
        weight_rounded = round(weight, 4)
        recommended_exhibitions[exhibitionID] = weight_rounded

    # 추천된 전시회 리스트를 가중치 기준으로 정렬
    sorted_recommended_exhibitions = sorted(recommended_exhibitions.items(), key=lambda x: x[1], reverse=True)

    # k개의 추천 전시회만을 반환
    return sorted_recommended_exhibitions[:k]
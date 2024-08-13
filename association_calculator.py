import pandas as pd

num_tags = 11  # 전체 태그 수

def calculate_association(userInfos, exhibitionInfos):
    association_list = []

    if userInfos is not None and exhibitionInfos is not None:
        for userInfo in userInfos:
            user_id = userInfo['user_id']
            user_tags = userInfo['user_tag_names']
            for exhibitionInfo in exhibitionInfos:
                exhibition_id = exhibitionInfo['exhibition_id']
                exhibition_tags = exhibitionInfo['exhibition_tag_names']
                
                # 선택된 태그의 가중치 계산
                weight = sum(1 for tag in user_tags if tag in exhibition_tags) / num_tags

                # 결과를 리스트에 저장
                association_list.append({'user_id': user_id, 'exhibition_id': exhibition_id, 'weight': weight})

    else:
        print("Unable to calculate association between users and exhibitions.") 

    # DataFrame으로 변환하여 반환
    return pd.DataFrame(association_list)
import requests
from bs4 import BeautifulSoup

# 링크
kindofpants_url = {1: "https://search.musinsa.com/category/003002?device=&d_cat_cd=003002&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={}&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q=", 2: "https://search.musinsa.com/category/003007?device=&d_cat_cd=003007&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={}&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q=",
                   3: "https://search.musinsa.com/category/003008?device=&d_cat_cd=003008&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={}&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q=", 4: "https://search.musinsa.com/category/003004?device=&d_cat_cd=003004&brand=&rate=&page_kind=search&list_kind=small&sort=pop&sub_sort=&page={}&display_cnt=90&sale_goods=&ex_soldout=&color=&price1=&price2=&exclusive_yn=&size=&tags=&sale_campaign_yn=&timesale_yn=&q="}

# 피팅
# 스타일별 피팅 데이터
style_data_loose_semiwide = [-6, 0, 2, 2]
style_data_loose_wide = [-6, 0, 3, 3]
style_data_regular_slim = [-10, 0, 1, 1]
style_data_regular_semiwide = [-10, 0, 2, 2]
style_data_regular_wide = [-10, 0, 3, 3]
style_data_rollupthin = [-12, 0, 2, 2]
style_data_rollupthin_crop = [-15, 0, 2, 2]
style_data_rollupthick = [-17, 0, 2, 2]
style_data_crop_slim = [-13, 0, 1, 1]
style_data_crop_semiwide = [-13, 0, 2, 2]
style_data_crop_wide = [-13, 0, 3, 3]
style_data = {1: style_data_loose_semiwide, 2: style_data_loose_wide, 3: style_data_regular_slim, 4: style_data_regular_semiwide, 5: style_data_regular_wide,
              6: style_data_rollupthin, 7: style_data_rollupthin_crop, 8: style_data_rollupthick, 9: style_data_crop_slim, 10: style_data_crop_semiwide, 11: style_data_crop_wide}

# 피팅 연산 정의


def fitting(user_data, user_style_data):
    fitting_data = []
    for i in range(4):
        fitting_data.append(user_data[i] + user_style_data[i])
    return fitting_data


# 입력
user_data = list(map(int, input("내 신체치수 입력 : 기장 허리단면 허벅지단면 밑단단면 >>>").split()))
user_style_data = style_data[int(input(
    "두께감 선택 : 1.슬림 2.테이퍼드 3.레귤러 4.세미와이드 5.와이드 중 숫자 입력"))]
user_style_data = style_data[int(input(
    "기장감 선택 : 1.12부 2.10부 3.8부 4.복숭아뼈 5.1부 중 숫자 입력"))]
user_style_data = style_data[int(input("롤업여부 선택 : 1.얇게 2.두껍게 3.안함"))]
user_style_data = style_data[int(input("바지를 올려입으시겠습니까? : 1.5cm 2.3cm 3.아니요"))]
user_kindofpants_url = kindofpants_url[int(
    input("1.데님 2.코튼 3.슬랙스 4.트레이닝 중 원하는 바지종류 숫자 입력"))]

# 연산
fitting_data = fitting(user_data, user_style_data)

for i in range(1, 5):
    url = user_kindofpants_url.format(i)
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    items = soup.find_all("p", attrs={"class": "list_info"})
    # 개별 아이템 내 사이즈 탐색
    for item in items:
        linkurl = item.a["href"]
        res_item = requests.get(linkurl)
        res_item.raise_for_status()
        res_soup = BeautifulSoup(res_item.text, "lxml")
        sizeinfo = res_soup.find_all("td", attrs={"class": "goods_size_val"})

        sizelst = []
        for size in sizeinfo:
            sizelst.append(size.get_text())
            if len(sizelst) == 5:
                sizelst[0] = float(sizelst[0]) - float(sizelst[3])
                sizelst.pop(3)
                for j in range(4):
                    if abs(float(sizelst[j])-fitting_data[j]) <= 1:
                        pass
                    else:
                        break
                    if j == 3:
                        print(sizelst, linkurl)
                sizelst = []

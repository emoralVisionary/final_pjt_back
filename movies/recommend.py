"""
    recommend 함수 자체는 movies.views.py 안에 정의했었습니다. 
    적당한 url 지정해서 movies.urls.py 에 recommend 추가하면 될 것 같아요. 
    삽질해가면서 짜서 그런지 json 관련 코드가 좀 지저분합니다
    
    성북구/동대문구 기준 오늘 날씨를 받아온 뒤에 날씨 상태에 따라 장르 하나를 골라서,
    해당 장르 영화 중에 평점이 높은 영화 10개를 추천해주는 식입니다. 
    (간략하게 주석 달아논거 참고해주세요)

    응답 데이터 형식 + 어떻게 구현할 지 같이 얘기 나눠봐요!

"""
from .models import Genre
import requests, render
import json
from datetime import date

# movies.views.py 

@require_safe
# 데코레이터 부분 수정 필요할 것 같습니다. 
def recommended(request):

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params ={
        'serviceKey' : 'KcYFmGjup0o8A5fEKjpIh3+kNtnQRnb/o8ZYCeRKYhU7+PyoTGb2PnKbdwsZ9Vb8Zm4B3QpHs2WkkcznXf67yw==',
        'pageNo' : '1',
        'numOfRows' : '12', 
        'dataType' : 'JSON', 
        'base_date' : str(date.today()).replace('-',''), 
        'base_time' : '0500', 
        'nx' : '61', 
        'ny' : '127' 
    }

    response = requests.get(url, params=params)
    content = response.content.decode("utf-8").replace("'", '"')
    # 날씨 상태 나타내는 숫자 추출 (1: 맑음, 2: 구름 조금, 3: 구름 많음, 4: 흐림)
    jsondata = json.loads(content)['response']['body']['items']['item'][5]['fcstValue']

    if jsondata == '1':
        data = {
            'Msg': '맑음',
            'genre': 80
        }
    elif jsondata == '2':
        data = {
            'Msg': '구름 조금',
            'genre': 53
        }
    elif jsondata == '3':
        data = {
            'Msg': '구름 많음',
            'genre': 27
        }
    elif jsondata == '4':
        data = {
            'Msg': '흐림',
            'genre': 10749
        }
    else:
        data = {
            'Msg': 'error'
        }
    print(data)
    now_genre = Genre.objects.get(pk=data['genre'])

    # 해당 장르 영화 중에서 평점 높은 영화 10개 => movies
    movies = now_genre.movie_set.order_by('-vote_average')[:10]

    context = {
        'Msg': data['Msg'],
        'movies': movies,
    }
    return render(request, 'movies/recommended.html', context)




def recommended(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all().order_by('-release_date', 'vote_average')[:10]
        context = {
            'movies': movies,
        }
        return render(request, 'movies/recommended.html', context)
    return redirect('community:index')

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

class Review:
	def __init__(self, comment, date, star, good, bad): # 생성자
		self.comment = comment # 리뷰 내용
		self.date = date # 날짜
		self.star = star # 별점
		self.good = good # 좋아요
		self.bad = bad # 싫어요

	def show(self):
		print("내용: " + self.comment +
			"\n날짜: " + self.date +
			"\n별점: " + self.star +
			"\n좋아요: " + self.good +
			"\n싫어요: " + self.bad)

def crawl(url):
	soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")
	review_list = []
	title = soup.find('h3', class_='h_movie').find('a').text
	div = soup.find('div', class_='score_result')
	data_list = div.select("ul > li")

	for review in data_list:
		star = review.find("div", class_="star_score").text.strip()
		reply = review.find("div", class_="score_reple")
		comment = reply.find("p").text.strip()
		date = reply.select("dt > em")[1].text.strip()
		button = review.find("div", class_="btn_area")
		sympathy = button.select("strong")
		good = sympathy[0].text
		bad = sympathy[1].text
		review_list.append(Review(comment, date, star, good, bad))

	return title, review_list

def get_summary(review_list):
    star_list = []
    good_list = []
    bad_list = []

    for review in review_list:
        star_list.append(int(review.star))
        good_list.append(int(review.good))
        bad_list.append(int(review.bad))

    star_series = pd.Series(star_list)
    good_series = pd.Series(good_list)
    bad_series = pd.Series(bad_list)

    summary = pd.DataFrame({
        'Star' : star_series,
        'Good' : good_series,
        'Bad' : bad_series,
        'Score' : good_series / (good_series + bad_series)
    })

    return summary

title, review_list = crawl("https://movie.naver.com/movie/bi/mi/basic.nhn?code=189069")
print('영화 제목: ' + title)

for review in review_list:
	review.show()

print(get_summary(review_list))

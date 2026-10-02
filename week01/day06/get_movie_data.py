import requests
import csv
from lxml import html
'''爬取电影数据'''

TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = f"{TMDB_BASE_URL}/movie/top-rated"
TMDB_MOVIE_URL = f"{TMDB_BASE_URL}/discover/movie/items"


def save_movie_info(all_movies):
    with open('movies_info_200.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["名称", "上映日期", "类型", "时长", "评分", "语言", "导演", "演员", "简介"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in all_movies:
            writer.writerow(movie)

def get_movie_info(movie_url):
    response = requests.get(movie_url, timeout=60)
    response.raise_for_status()
    document = html.fromstring(response.text)
    # 电影名称
    movie_names = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    # 电影日期
    movie_dates = document.xpath('.//div[@class="facts"]/span[@class="release"]/text()')
    # 电影类型
    movie_genres = document.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a/text()')
    # 电影时长
    movie_runtime = document.xpath('.//div[@class="facts"]/span[@class="runtime"]/text()')
    # 电影评分
    movie_ratings = document.xpath('.//div[@data-percent]/@data-percent')
    # 电影语言
    movie_languages = document.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
    # 电影导演
    movie_directors = document.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li/p[contains(normalize-space(text()), "Director")]/preceding-sibling::p[1]/a/text()')
    # 电影演员
    movie_casts = document.xpath('//*[@id="cast_scroller"]/ol/li/p/a/text()')
    # 电影简介
    movie_overviews = document.xpath('.//div[@class="overview"]/p/text()')

    movie_info = {
        "名称": movie_names[0].strip() if movie_names else '',
        "上映日期": movie_dates[0].strip() if movie_dates else '',
        "类型": ",".join(movie_genres).strip() if movie_genres else '',
        "时长": movie_runtime[0].strip() if movie_runtime else '',
        "评分": movie_ratings[0] if movie_ratings else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ",".join(movie_directors).strip() if movie_directors else '',
        "演员": ",".join(movie_casts).strip() if movie_casts else '',
        "简介": movie_overviews[0].strip() if movie_overviews else '',
    }
    return movie_info

def get_top_movies():
    all_movies = []
    for page in range(1, 11):  # 爬取前10页的电影数据
        if page == 1:
            response = requests.get(TMDB_TOP_URL, timeout=60)
        else:
            response = requests.post(TMDB_MOVIE_URL,
                                     f"air_date.gte=&air_date.lte=&certification=&certification_country=US&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-04-02&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=US&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated",
                                      timeout=60)
        response.raise_for_status()
        # 获取电影列表
        document = html.fromstring(response.text)
        movie_list = document.xpath('//div[@class="media-list-results contents"]/div')

        for movie in movie_list:
            movie_urls = movie.xpath('.//a[@class="flex w-full"]/@href')
            if movie_urls:
                movie_url = f"{TMDB_BASE_URL}{movie_urls[0]}"
                movie_info = get_movie_info(movie_url)
                all_movies.append(movie_info)

    save_movie_info(all_movies)
    

if __name__ == "__main__":
    get_top_movies()
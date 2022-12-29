import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request

app = Flask(__name__)

# 데이터 전처리
df = pd.read_csv('/Users/mingeuni/molva/molva-dataset/movie.csv')
df = df[['code', 'genre_list']]
print(df)
df['code'] = df['code'].apply(lambda x: str(x))
df['genre_list'] = df['genre_list'].apply(lambda x: list(str(x).split(',')))
df['genre_list'] = df['genre_list'].apply(lambda x: ' '.join(x))

# 유사도 행렬 생성
count_vect = CountVectorizer(min_df=0, ngram_range=(1, 2))
genre_mat = count_vect.fit_transform(df['genre_list'])
genre_sim = cosine_similarity(genre_mat, genre_mat)


@app.route('/')
def hello():
    return 'Hello, World!'


def find_sim_movie(src_df, sim_matrix, code, top_n=600):
    print(src_df['code'])
    code_movie = src_df[src_df['code'] == str(code)]
    print(code)
    print(type(code))
    print(type(src_df['code'].values))
    print(code_movie)

    code_idx = code_movie.index.values

    src_df['similarity'] = sim_matrix[code_idx, :].reshape(-1, 1)

    temp = src_df.sort_values(by="similarity", ascending=False)
    final_index = temp.index.values[: top_n]

    return src_df.iloc[final_index]


@app.route('/recommend', methods=['POST'])
def recommend_movies():
    if request.method == 'POST':
        # 비슷한 영화 받아오기
        temp = df.copy()
        temp['score'] = 0.0

        body = request.json
        if body is None:
            return temp['code'].values.tolist()
        code_list = str(body).replace(' ', '')[1:-1].split(',')

        for i in code_list:
            if i == '':
                return temp['code'].values.tolist()
            similar_movies = find_sim_movie(temp, genre_sim, i)
            for j, row in similar_movies.iterrows():
                target = temp[temp['code'] == row['code']]
                old_val = temp._get_value(target.index.values[0], 'score')
                temp._set_value(target.index.values[0], 'score', target.similarity.values + old_val)

        # 중복 제거 및 반환
        exists = []
        for i, row in temp.iterrows():
            if row['code'] in code_list:
                exists.append(i)
        temp = temp.drop(exists)
        temp = temp.sort_values(by="score", ascending=False)

        return temp['code'].values.tolist()

    else:
        return 'error'


if __name__ == '__main__':
    app.run(debug=True)




from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
df_cd = pickle.load(open('df_cd.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list( popular_df['avg_rating'].values.round(2))
                           )
# print(round(3.45678,2))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

# @app.route('/recommend_books',methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     # if((pt.index==user_input)[0][0]==False):
#     #  return "not found"
#     index = np.where(pt.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = df_cd[df_cd['Book-Title'] == pt.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['avg_rating'].values.round(2)))
#         data.append(item)

#     print(data)

#     return render_template('recommend.html',data=data)


@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    try:
        index = pt.index.get_loc(user_input)
    except KeyError:
        error_message = f"{user_input} not found in the book data"
        return render_template('recommend.html', error_message=error_message)
    try:
        similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:6]
    except IndexError:
        error_message = f"Not enough similar books found for {user_input}"
        return render_template('recommend.html', error_message=error_message)
    data = []
    for i in similar_items:
        item = []
        temp_df = df_cd[df_cd['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['avg_rating'].values.round(2)))
        data.append(item)
    return render_template('recommend.html',data=data)


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
import pandas as pd
from wordcloud import WordCloud # 워드클라우드 제작 라이브러리
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('Agg')


def wordcloud(category1, category2):
    category2 = category2+' '
    df = pd.read_csv('recommendation/data/data_ver2_new_wordsplit.csv')
    print(df)
    category1_review = df[['category1', 'category2', 'clean_review_contents']].copy()
    
    category1_review['clean_review_contents'] = category1_review['clean_review_contents'].apply(lambda x: ' '.join([word.strip(" '[]") for word in x.split(',') if len(word) >= 2]))
    
    grouped_df = category1_review.groupby(['category1', 'category2'])['clean_review_contents'].apply(lambda x: ' '.join(x)).reset_index()
   
    df = grouped_df[(grouped_df['category1'] == category1) & (grouped_df['category2'] == category2)]
    
    text_combined = ' '.join(df['clean_review_contents'])  # Combine all texts into a single string

    word_freq = pd.Series(text_combined.split()).value_counts()[:20]#.head(20)
    print(word_freq)
    font_path = '/home/lab04/final_project/coupang/static/fonts/NanumGothic-Bold.ttf'

    # font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate_from_frequencies(word_freq)
  
    #Plot the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    print('word')
    image_name='wordcloud.png'    # 변경
    image_path = 'static/images/'+image_name #변경

    plt.savefig(image_path)

    return image_name # 변경
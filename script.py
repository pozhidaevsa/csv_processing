import pandas as pd
from pathlib import Path
import itertools
#from stop_words import get_stop_words

PATH_TO_DATA = Path('data')
data = pd.read_csv(PATH_TO_DATA / 'keywords_.csv', sep=';', usecols=[0, 3],
                   names=['AdGroupId', 'Keyword'], header=0)

# апострофы
data['Keyword'] = data['Keyword'].str.replace("'", "")
# слова начинающиеся с -
data['Keyword'] = data['Keyword'].replace(['-[^, ]*'], '', regex=True)
# скобки
data['Keyword'] = data['Keyword'].replace(['\[', '\]'], '', regex=True)
# лишние пробелы
data['Keyword'] = data['Keyword'].replace('\s+', ' ', regex=True)
data['Keyword'] = data['Keyword'].str.rstrip()
# нижний регистр
data['Keyword'] = data['Keyword'].str.lower()

#stop_words_ru = set(get_stop_words('russian'))
#stop_words_en = set(get_stop_words('english'))

#stop_words = stop_words_ru.union(stop_words_en)

intersections = []
for i, j in itertools.product(data.index, repeat=2):
    if data['AdGroupId'][i] != data['AdGroupId'][j]:
        words1 = set(str(data['Keyword'][i]).split())
        words2 = set(str(data['Keyword'][j]).split())
        #words1.difference_update(stop_words)
        #words2.difference_update(stop_words)
        matching_words = list(words2.intersection(words1))
        if len(matching_words) >= 2:
            intersections.append({'Keyword_x': data['Keyword'][i],
                                  'AdGroupId_x': data['AdGroupId'][i],
                                  'Keyword_y': data['Keyword'][j],
                                  'AdGroupId_y': data['AdGroupId'][j],
                                  'crossed': ', '.join(matching_words)})

final = pd.DataFrame(intersections)
final.to_csv('keywords_ext.csv', index=False, sep=';')

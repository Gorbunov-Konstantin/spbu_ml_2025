import pandas as pd

# Пути к файлам
file_train = 'data/Real estate.csv'
file_test = 'data/prices_test.csv'

# Загрузка данных
df_train = pd.read_csv(file_train)
df_test = pd.read_csv(file_test)

# Просмотр первых строк таблиц
df_train.head(), df_test.head()

# Удаляем лишние столбцы
df_test = df_test.drop(columns=['Unnamed: 0'], errors='ignore')

# Ключи для объединения
keys = [
    'X1 transaction date', 'X2 house age', 'X3 distance to the nearest MRT station',
    'X4 number of convenience stores', 'X5 latitude', 'X6 longitude'
]

# Пустой DataFrame для результата
result = []

# Проходим по каждой строке тестовой таблицы
for _, row in df_test.iterrows():
    # Оставляем только ненулевые значения в текущей строке
    filter_conditions = {key: row[key] for key in keys if not pd.isna(row[key])}
    
    # Ищем в train-таблице совпадения по доступным значениям
    match = df_train
    for key, value in filter_conditions.items():
        match = match[match[key] == value]
    
    # Если нашли совпадение, добавляем к результату
    if not match.empty:
        merged_row = row.to_dict()
        merged_row['Y house price of unit area'] = match['Y house price of unit area'].values[0]
        result.append(merged_row)

# Создаём итоговую таблицу
df_merged = pd.DataFrame(result)

# Сохраняем результат в файл
df_merged.to_csv('merged_result.csv', index=False)

print(len(df_merged))
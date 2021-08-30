import pandas as pd

with open("tabak.txt", "r") as f:
    original_data = f.read()


def get_data(row, name_data):
    for i in row:
        if i.count(name_data) != 0:
            i = i.split(':')
            if len(i) > 1:
                return i[1]
            else:
                return "не указан"
    return "не указан"


data = [i.split('|') for i in original_data.split('\n')]
data.pop()
for i in range(len(data)):

    adr = get_data(data[i], 'Адрес')
    telephone = get_data(data[i], 'Телефон')
    e_mail = get_data(data[i], 'e-mail')
    name = data[i][-1]

    data[i] = [adr, telephone, e_mail, name]

for i in range(len(data)):
    # print(original_data.split('\n')[i])
    print(data[i], i)

columns = ['Адрес', 'Телефон', 'Почта', 'Название']
df = pd.DataFrame(data, columns=columns)
df = df[(df['Телефон'] != 'не указан') | (df['Почта'] != 'не указан')]
df.to_csv('tabak.csv')

print(original_data)

# Импортируем нужные модули
from urllib.request import urlretrieve
import vk, os, time, math
from datetime import datetime
from collections import Counter
import numpy as np




import matplotlib.pyplot as plt
plt.style.use(plt.style.available[4])

today = datetime.today()
days_in_year = 365.2425    
def getAge(birth_date):
    return int((today - birth_date).days / days_in_year)


def getMetriks(subs, groupName):
    girls=0
    boys=0
    for sub in subs:
      
      if sub['sex']==1:
        girls+=1
      else:
        boys+=1
      try:
          sub['age'] = getAge(datetime.strptime(sub['bdate'],'%d.%m.%Y'))
      except:
        pass # print('Не удалось вычислить возраст')
    ages = Counter([sub['age'] for sub in subs if ('age' in sub)])
    countries = Counter([sub['country']['title'] for sub in subs if ('country' in sub)])
    print('///////////\n Метрики по группе: '+groupName+'\n////////////')
    print('Возраст пользователей', ages)
    sumAge = 0
    for elem in ages:
      sumAge+=ages[elem]*elem
    print('Средний возраст пользователей: ',  sumAge/sum(ages.values()))
    print('/////////////')
    print('Регион пользователей: ', countries)
    
def getIntersection(group1, group2):
    group1 = set((tuple(i) for i in group1))
    group2 = set((tuple(i) for i in group2))
    intersection = group1.intersection(group2)
    all_members = len(group1) + len(group2) - len(intersection)  
    result = len(intersection)/all_members * 100  # Высчитываем пересечение в процентах
    print("\n////////\nПересечение аудиторий: ", round(result,2), "%", sep="") 
    print('\nПересечение: ',intersection)

def union_members(group1, group2):
    group1 = set(group1)  
    group2 = set(group2)  
    union = group1.union(group2)  # Объединяем два множества
    return list(union) 

def getMembers(group_id):
    return vkapi.groups.getMembers(group_id = group_id,count = 1000, fields = ['id','first_name','last_name','sex','bdate','city','country',])
session = vk.Session(access_token='59ef803926baf56aa845b40185d09a3038ea3ca349ed123be1db70f81e3fad647510d9405d6ecab162261')
vkapi = vk.API(session, v='5.81')

def barChart(dict1,dict2):

    x1 = list(dict1.keys())
    y1 = list(dict1.values())
    plt.bar(x1,y1)
    plt.title("Первая группа")
    plt.show()
    x2 = list(dict2.keys())
    y2 = list(dict2.values())
    plt.bar(x2,y2)
    plt.title("Вторая группа")
    plt.show()
    width = 0.20
    columns = list(set(x1) & set(x2))
    y1Cleaned =[dict1[i] for i in list(set(columns) & set(x1))]
    y2Cleaned =[dict2[i] for i in list(set(columns) & set(x1))]
    if(all(isinstance(n, int) for n in columns)):
      plt.bar(columns, y1Cleaned, width = 0.2)
      plt.bar([i+0.2 for i in columns], y2Cleaned, width = 0.2)
      plt.title("Сравнение возрастов целевой аудитории")
      plt.xlabel("Возраст")
      plt.ylabel("Количество")
      plt.show()


group1_id = 'https://vk.com/extreme_park'
group2_id =  'https://vk.com/skvot_perm'

subs1 = getMembers('extreme_park')['items']
subs2 =  getMembers('skvot_perm')['items']

getMetriks(subs1,group1_id)
getMetriks(subs2,group2_id)



fitInfo1 = [[sub['id'],sub['first_name'],sub['last_name']] for sub in subs1  if (sub['first_name']!='DELETED')]
fitInfo2 = [[sub['id'],sub['first_name'],sub['last_name']] for sub in subs2  if (sub['first_name']!='DELETED')]

getIntersection(fitInfo1,fitInfo2)

#Визуализация 
agesdict1 = Counter([sub['age'] for sub in subs1 if ('age' in sub)])
agesdict2 = Counter([sub['age'] for sub in subs2 if ('age' in sub)])

barChart(agesdict1,agesdict2 )

countries1 = Counter([sub['country']['title'] for sub in subs1 if ('country' in sub)])
countries2 = Counter([sub['country']['title'] for sub in subs2 if ('country' in sub)])
barChart(countries1,countries2)
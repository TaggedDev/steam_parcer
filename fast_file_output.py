import MySteamParcer
import csv


count = 1

with open('Steam.csv','r', encoding='utf-8', ) as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)
    
    for line in reader:
    
        if count < 6:
            print(line)
            count += 1
        else:
            break
    print('End')  
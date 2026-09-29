#csv操作
import csv

#写入csv文件
with open('../data.csv', 'w',encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Age', 'City'])
    writer.writeheader()
    writer.writerow({'Name': 'Alice', 'Age': 30, 'City': 'New York'})
    writer.writerow({'Name': 'Bob', 'Age': 25, 'City': 'Los Angeles'})
    writer.writerow({'Name': 'Charlie', 'Age': 35, 'City': 'Chicago'})

#读取csv文件
with open('../data.csv', 'r',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Name'], row['Age'], row['City'])
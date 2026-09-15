'''
筛选所有“就业”政策并按年份排序
'''

policy_file1={'name': '高校毕业生基层就业补贴通知', 'year': 2021, 'department': '市人力资源和社会保障局'}
policy_file2={'name': '关于进一步做好高校毕业生就业创业工作的通知', 'year': 2020, 'department': '市教育局'}
policy_file3={'name': '灵活就业人员社保衔接管理办法', 'year': 2022, 'department': '省人力资源和社会保障厅'}
policy_file4={'name': '退役军人就业创业扶持指导意见', 'year': 2023, 'department': '市退役军人事务局'}
policy_file5={'name': '青年就业见习基地管理办法', 'year': 2024, 'department': '市人力资源和社会保障局'}

policy_list=[policy_file1, policy_file2, policy_file3, policy_file4, policy_file5]
sorted_policies = sorted(policy_list, key=lambda x: x['year'])
print("按年份排序后的政策列表:")
for policy in policy_list:
    print(f"政策名称: {policy['name']}, 年份: {policy['year']}, 部门: {policy['department']}")
# print(policy_list)


list1 = [1, 2, 3, 4, 5,6,7]
list2 = [4,5,6, 7, 8, 9, 10]

new_list = list1 + list2
# new_list = [*list1, *list2]
print("合并后的列表:", new_list)

new_list = list(set(new_list))
print("去重后的列表:", new_list)


list3=[33,44,56,77,73,89,72,31,43]
res=[i**2 for i in list3 if i%2==0]
print("列表中偶数的平方:", res)
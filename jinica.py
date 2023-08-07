import pandas as pd
import matplotlib.pyplot as plt

jinshi_pd = pd.read_excel('input-tang-jinshi.xlsx', sheet_name='Sheet1')
jinshi_pd = jinshi_pd.dropna(subset=['Entry Year'])
jinshi_pd = jinshi_pd[jinshi_pd['Entry Year'] != 0]
# print(jinshi_pd.head())

mca = pd.read_excel('input-tang-mca.xlsx', sheet_name='Sheet1')
mca = mca.dropna(subset=['节镇在任时间'])
# print(mca.head())

nianhao_dic = {}
nianhao_pd = pd.read_excel('dic-tang-nianhao.xlsx', sheet_name='data')
for index, row in nianhao_pd.iterrows():
    nianhao_dic[row['reign_complete']] = row['year']
# print(list(nianhao_dic.items())[:5])

shizuzhi_list = []
with open('dic-shizuzhi.txt', 'r', encoding='utf-8') as f:
    for line in f:
        shizuzhi_list.append(line.strip())
print(shizuzhi_list[:5])

jinshi_shizuzhi_pd = pd.DataFrame(columns=jinshi_pd.columns)
for index, row in jinshi_pd.iterrows():
    if row['姓名'][:2] in shizuzhi_list:
        jinshi_shizuzhi_pd = jinshi_shizuzhi_pd.append(row, ignore_index=True)
        continue
    if row['姓名'][:1] in shizuzhi_list:
        jinshi_shizuzhi_pd = jinshi_shizuzhi_pd.append(row, ignore_index=True)

print(jinshi_shizuzhi_pd.head())

# draw a line chart base on (column Entry Year of jinshi_shizuzhi_pd)/(column Entry Year of jinshi_p), group by 10 years

group_num = 30
jinshi_pd['Entry Year'] = jinshi_pd['Entry Year'].astype(int)
jinshi_shizuzhi_pd['Entry Year'] = jinshi_shizuzhi_pd['Entry Year'].astype(int)
jinshi_pd_groupby = jinshi_pd.groupby(jinshi_pd['Entry Year'] // group_num * group_num).size().to_dict()
print(jinshi_pd_groupby)
jinshi_shizuzhi_pd_groupby = jinshi_shizuzhi_pd.groupby(jinshi_shizuzhi_pd['Entry Year'] // group_num * group_num).size().to_dict()
print(jinshi_shizuzhi_pd_groupby)


# year_begin = 0
year_begin = 680
year_end = 880

year_ratio_dic = {}
for key in jinshi_pd_groupby.keys():
    if year_begin != 0:
        if key < year_begin or key > year_end:
            continue
    if key in jinshi_shizuzhi_pd_groupby.keys():
        year_ratio_dic[key] = jinshi_shizuzhi_pd_groupby[key] / jinshi_pd_groupby[key]
    else:
        year_ratio_dic[key] = 0
   
# visualization
plt.figure(figsize=(20, 10))
plt.plot(list(year_ratio_dic.keys()), list(year_ratio_dic.values()), color='blue', linewidth=2.0, linestyle='-')
plt.xlabel('Year')
plt.ylabel('Ratio')
plt.title('Ratio of Shizuzhi Jinshi')
plt.show()
plt.close()


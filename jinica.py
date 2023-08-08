import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

jinshi_pd = pd.read_excel('input-tang-jinshi-raw.xlsx', sheet_name='Sheet1')
jinshi_pd = jinshi_pd.dropna(subset=['Entry Year'])
jinshi_pd = jinshi_pd[jinshi_pd['Entry Year'] != 0]
# print(jinshi_pd.head())

nianhao_dic = {}
nianhao_pd = pd.read_excel('dic-tang-nianhao.xlsx', sheet_name='data')
for index, row in nianhao_pd.iterrows():
    nianhao_dic[row['reign_complete']] = row['year']
# print(list(nianhao_dic.items())[:5])

mca_pd = pd.read_excel('input-tang-mca.xlsx', sheet_name='Sheet1')
# drop the records when 僚佐名字 is null
mca_pd = mca_pd.dropna(subset=['僚佐名字'])
mca_pd = mca_pd.dropna(subset=['节镇在任时间'])
mca_pd["year_chn"] = mca_pd["节镇在任时间"].str.split("——", n = 1, expand = True)[0]
mca_pd["year"] = mca_pd["year_chn"].map(nianhao_dic)

print(mca_pd.head())

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

group_num = 10
jinshi_pd['Entry Year'] = jinshi_pd['Entry Year'].astype(int)
jinshi_shizuzhi_pd['Entry Year'] = jinshi_shizuzhi_pd['Entry Year'].astype(int)
jinshi_pd_groupby = jinshi_pd.groupby(jinshi_pd['Entry Year'] // group_num * group_num).size().to_dict()
print(jinshi_pd_groupby)
jinshi_shizuzhi_pd_groupby = jinshi_shizuzhi_pd.groupby(jinshi_shizuzhi_pd['Entry Year'] // group_num * group_num).size().to_dict()
print(jinshi_shizuzhi_pd_groupby)


year_begin = 0
# year_begin = 680
year_end = 880

jinshi_year_ratio_dic = {}
for key in jinshi_pd_groupby.keys():
    if year_begin != 0:
        if key < year_begin or key > year_end:
            continue
    if key in jinshi_shizuzhi_pd_groupby.keys():
        jinshi_year_ratio_dic[key] = jinshi_shizuzhi_pd_groupby[key] / jinshi_pd_groupby[key]
    else:
        jinshi_year_ratio_dic[key] = 0



mca_shizuzhi_pd = pd.DataFrame(columns=mca_pd.columns)
for index, row in mca_pd.iterrows():
    if row['僚佐名字'][:2] in shizuzhi_list:
        mca_shizuzhi_pd = mca_shizuzhi_pd.append(row, ignore_index=True)
        continue
    if row['僚佐名字'][:1] in shizuzhi_list:
        mca_shizuzhi_pd = mca_shizuzhi_pd.append(row, ignore_index=True)

mca_pd_groupby = mca_pd.groupby(mca_pd['year'] // group_num * group_num).size().to_dict()
print(mca_pd_groupby)
mca_shizuzhi_pd_groupby = mca_shizuzhi_pd.groupby(mca_shizuzhi_pd['year'] // group_num * group_num).size().to_dict()
print(mca_shizuzhi_pd_groupby)


mca_year_ratio_dic = {}
for key in mca_pd_groupby.keys():
    if year_begin != 0:
        if key < year_begin or key > year_end:
            continue
    if key in mca_shizuzhi_pd_groupby.keys():
        mca_year_ratio_dic[key] = mca_shizuzhi_pd_groupby[key] / mca_pd_groupby[key]
    else:
        mca_year_ratio_dic[key] = 0

# remove the keys in jinshi_year_ratio_dic and mca_year_ratio_dic when the other one doesn't have
for key in list(jinshi_year_ratio_dic.keys()):
    if key not in mca_year_ratio_dic.keys():
        jinshi_year_ratio_dic.pop(key)
for key in list(mca_year_ratio_dic.keys()):
    if key not in jinshi_year_ratio_dic.keys():
        mca_year_ratio_dic.pop(key)

# draw jinshi_year_ratio_dic and mca_year_ratio_dic on the same chart
plt.plot(list(jinshi_year_ratio_dic.keys()), list(jinshi_year_ratio_dic.values()), label='jinshi')
plt.plot(list(mca_year_ratio_dic.keys()), list(mca_year_ratio_dic.values()), label='mca')
plt.xlabel('Year')
plt.ylabel('Shizupu Ratio')
plt.title('Shizupu Ratio of Jinshi and MCA')
plt.legend()
plt.show()

# Draw regression line
plt.plot(list(jinshi_year_ratio_dic.keys()), list(jinshi_year_ratio_dic.values()), 'o', label='jinshi')
plt.plot(list(mca_year_ratio_dic.keys()), list(mca_year_ratio_dic.values()), 'o', label='mca')

# calculate regression line for jinshi_year_ratio_dic
x_jinshi = np.array(list(jinshi_year_ratio_dic.keys()))
y_jinshi = np.array(list(jinshi_year_ratio_dic.values()))
m_jinshi, b_jinshi = np.polyfit(x_jinshi, y_jinshi, 1)
plt.plot(x_jinshi, m_jinshi*x_jinshi + b_jinshi, '-', label='jinshi regression')

# calculate regression line for mca_year_ratio_dic
x_mca = np.array(list(mca_year_ratio_dic.keys()))
y_mca = np.array(list(mca_year_ratio_dic.values()))
m_mca, b_mca = np.polyfit(x_mca, y_mca, 1)
plt.plot(x_mca, m_mca*x_mca + b_mca, '-', label='mca regression')

plt.xlabel('Year')
plt.ylabel('Shizupu Ratio')
plt.title('Shizupu Ratio of Jinshi and MCA')

plt.legend()
plt.show()




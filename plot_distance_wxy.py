
# 步骤 1: 导入必要的库
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

names = ["annealing_cubic_WGR2H@20_WGE2H@20_ION@15_box8_1"]
labels = {"annealing_cubic_WGR2H@20_WGE2H@20_ION@15_box8_1": "R2H + E2H"}

result_df = pd.DataFrame()
for name in names:
    csvpath = f"data/{name}.csv"

    # 步骤 2: 读取 CSV 文件
    df = pd.read_csv(csvpath,header=None)
    df.rename(columns={df.columns[0]: "frame", df.columns[1]: "trjname"}, inplace=True)
    df = df[df["frame"] > 100]
    df.insert(0, "name", labels[name])
    result_df = pd.concat([result_df, df], ignore_index=True)

df = result_df
import seaborn as sns  # Import seaborn for a color palette

# Assuming df is your DataFrame

# Get a color palette with the number of unique 'name' values
palette = sns.color_palette("husl", n_colors=len(df['name'].unique()))

# Create a dictionary to map 'name' values to colors
color_dict = dict(zip(df['name'].unique(), palette))

# 遍历不同的 'name' 值
for label2_value, group_df in df.groupby('name'):
    # 将每组的数据合并为一维数组
    group_data = group_df.iloc[:, 3:].values.flatten()
    
    # 使用不同的颜色区分每个 'name' 值
    sns.histplot(group_data, bins=100)

# 添加标题和标签
plt.title('Density Distribution of Distance between His\'s CA')
plt.xlabel('Distance')
plt.ylabel('Density')

# 显示图例，用于区分不同的 'name' 值
plt.legend()
plt.xlim(0, 15)

# 显示图形
plt.show()

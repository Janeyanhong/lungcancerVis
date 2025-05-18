# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import shutil
import os

# ====== 1. 强制清除Matplotlib字体缓存 ======
# 自动获取用户名
username = os.getenv('USERNAME')
cache_dir = rf"C:\Users\{username}\.matplotlib"
try:
    shutil.rmtree(cache_dir)
    print(f"已清除缓存目录：{cache_dir}")
except Exception as e:
    print(f"缓存清除失败（可能无需操作）: {e}")

# ====== 2. 精准设置微软雅黑字体 ======
# 根据您的字体库截图，选择合适的字体文件
font_path = 'C:/Windows/Fonts/微软雅黑.ttf'  # 尝试使用微软雅黑TTF格式
if not os.path.exists(font_path):
    font_path = 'C:/Windows/Fonts/msyh.ttf'  # 备选文件名
    if not os.path.exists(font_path):
        font_path = 'C:/Windows/Fonts/simhei.ttf'  # 备选黑体
        if not os.path.exists(font_path):
            font_path = 'C:/Windows/Fonts/simsun.ttc'  # 备选宋体

font_name = 'Microsoft YaHei'  # 默认字体名称

# 注册字体
try:
    font_prop = fm.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = font_name
    print(f"✓ 成功加载字体：{font_name}")
except Exception as e:
    print(f"字体加载失败: {e}")
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    # 字体加载失败时不改变font_name变量，保持默认值

plt.rcParams['axes.unicode_minus'] = False

# ====== 3. 验证字体设置 ======
fig, ax = plt.subplots()
ax.set_title('中文测试: 微软雅黑')
ax.text(0.5, 0.5, '成功显示中文!', ha='center')
plt.close(fig)
print("✓ 中文测试通过")

# ====== 4. 加载数据（保持原代码）=====
try:
    data = pd.read_csv('Churn Modeling.csv')
except FileNotFoundError:
    print("错误：文件未找到！请确认：")
    print("1. 文件名为 'Churn Modeling.csv'")
    print("2. 文件放在当前代码目录下")
    exit()

# ====== 5. 可视化配置（增加强制字体设置）=====
# 使用新的样式名称
try:
    plt.style.use('seaborn-v0_8')  # 更新为新的样式名称
except:
    plt.style.use('default')  # 如果失败则使用默认样式
colors = ['#4C72B0', '#DD8452']

# 在每次绘图前显式设置字体
def set_font():
    plt.rcParams['font.family'] = font_name
    plt.rcParams['font.size'] = 12

# ==================== 图表1：流失率饼图 ====================
set_font()
plt.figure(figsize=(8, 6))
data['Exited'].value_counts().plot(
    kind='pie',
    labels=['未流失', '流失'],
    autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',  # 小数值隐藏
    startangle=90,
    colors=colors,
    wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
)
plt.title('客户整体流失率分布', fontsize=14, pad=20)
plt.ylabel('')
plt.show()


# ==================== 图表2：国家与流失关系 ====================
plt.figure(figsize=(10, 6))
country_data = pd.crosstab(data['Geography'], data['Exited'])
country_data.columns = ['未流失', '流失']  # 重命名列
country_data.plot(
    kind='bar',
    stacked=True,
    color=colors,
    edgecolor='black'
)
plt.title('分国家客户流失情况', fontsize=14)
plt.xlabel('国家', fontsize=12)
plt.ylabel('客户数量', fontsize=12)
plt.xticks(rotation=0)  # 水平显示国家标签
plt.legend(title='状态')
plt.tight_layout()
plt.show()

# ==================== 图表3：年龄分布小提琴图 ====================
plt.figure(figsize=(10, 6))
sns.violinplot(
    x='Exited',
    y='Age',
    data=data,
    palette=colors,
    split=True,
    inner='quartile'  # 显示四分位数线
)
plt.title('流失客户的年龄分布', fontsize=14)
plt.xticks([0, 1], ['未流失', '流失'])
plt.xlabel('客户状态', fontsize=12)
plt.ylabel('年龄', fontsize=12)
plt.show()

# ==================== 图表4：信用评分箱线图 ====================
plt.figure(figsize=(10, 6))
sns.boxplot(
    x='Exited',
    y='CreditScore',
    data=data,
    palette=colors,
    width=0.5,
    showmeans=True,  # 显示均值标记
    meanprops={'marker':'o', 'markerfacecolor':'white'}
)
plt.title('信用评分与流失关系', fontsize=14)
plt.xticks([0, 1], ['未流失', '流失'])
plt.xlabel('客户状态', fontsize=12)
plt.ylabel('信用评分', fontsize=12)
plt.show()

# ==================== 图表5：账户余额 vs 估计工资（散点图） ====================
sns.scatterplot(x='Balance', y='EstimatedSalary', hue='Exited', data=data, alpha=0.5)
plt.title('账户余额与工资的关系')
plt.show()


# ==================== 图表7：产品数量分布（条形图） ====================
data['NumOfProducts'].value_counts().sort_index().plot(kind='bar')
plt.title('客户持有产品数量分布')
plt.xlabel('产品数量')
plt.ylabel('频次')
plt.show()
# 可以尝试的其他中文字体（从您的截图中看到的）
# 'C:/Windows/Fonts/simkai.ttf'  # 楷体
# 'C:/Windows/Fonts/simfang.ttf'  # 仿宋
# 'C:/Windows/Fonts/华文细黑.ttf'  # 华文细黑
# 'C:/Windows/Fonts/华文宋体.ttf'  # 华文宋体

print("所有图表已生成！关闭最后一个窗口后程序结束。")
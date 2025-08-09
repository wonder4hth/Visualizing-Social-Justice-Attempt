import pandas as pd
from graphviz import Digraph
from PIL import Image
import matplotlib.pyplot as plt

# 加载状态转换数据集
transition_df = pd.read_csv('Ideology states analysis - transitions.csv')

# 加载状态名称数据集
name_df = pd.read_csv('Ideology states analysis - state repository.csv')

# 统计每个状态成为 to state 的次数
to_state_counts = transition_df['to state'].value_counts()

# 计算四分位数
q1 = to_state_counts.quantile(0.25)
q3 = to_state_counts.quantile(0.75)

# 定义颜色映射 - 蓝色为正向，红色为反向，灰色为低权重
color_mapping = {
    '+': '#0000FF',  # 蓝色表示正向影响
    '-': '#FF0000',  # 红色表示反向影响
    'low_weight': '#C9C5C5'  # 灰色表示权重≤1的关系
}

# 创建一个有向图对象
dot = Digraph(comment='State Machine', node_attr={'fontname': 'WenQuanYi Zen Hei', 'fontsize': '20'},
              edge_attr={'fontname': 'WenQuanYi Zen Hei'})

# 设置分辨率为 300 dpi
dot.attr(dpi='300')

# 添加节点（状态），使用英文名称，并根据四分位数分类设置样式
for index, row in name_df.iterrows():
    state_number = row['state number']
    state_name_en = row['state description']
    count = to_state_counts.get(state_number, 0)
    if count <= q1:
        dot.node(str(state_number), state_name_en, fontweight='bold')  # Q1以下，字体加粗
    elif count >= q3:
        dot.node(str(state_number), state_name_en, fontcolor='#C9C5C5')  # Q3以上，字体灰色
    else:
        dot.node(str(state_number), state_name_en)  # 中间

# 添加边（状态转换），设置颜色
for index, row in transition_df.iterrows():
    # 判断权重是否≤1，决定是否使用灰色
    if row['weight'] <= 1:
        color = color_mapping['low_weight']
    else:
        # 根据+/-符号选择红蓝颜色
        color = color_mapping.get(row['+/-'], 'black')
    dot.edge(str(row['0']), str(row['to state']), color=color)

# 渲染图形
img_path = 'state_machine_with_gray_low_weight'
dot.render(img_path, format='png', cleanup=True, view=False)

# 使用 matplotlib 显示图像
img = Image.open(f'{img_path}.png')
plt.rcParams['figure.dpi'] = 300
plt.imshow(img)
plt.axis('off')
plt.show()
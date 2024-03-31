import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tkinter
from tkinter import filedialog


class Graph(object):
    def __init__(self):
        self.excel_path = 'D:\\工作\\深圳智慧医学\\数据对接\\医惠his系统数据字典-清洗-子集.xlsx'

    def read_data(self):
        self.data = pd.read_excel(self.excel_path, header=0)

    def explore(self):
        pattern = self.data['表中文名'].str.contains('费', case=False, na=False)
        self.data_graph = self.data[pattern]

    def infer_table_relationships(self):
        self.G = nx.Graph()
        tables = self.data_graph['表中文名'].unique()
        for num, table1 in enumerate(tables):
            data_table1 = self.data_graph[self.data_graph['表中文名']==table1]
            for table2 in tables[num+1:]:
                data_table2 = self.data_graph[self.data_graph['表中文名']==table2]
                common_fields = set(data_table1['字段名称']) & set(data_table2['字段名称'])
                if common_fields:
                    common_fields_ch = []
                    for field in common_fields:
                        field_ch = data_table1.loc[data_table1['字段名称']==field, '字段名称']
                        common_fields_ch.append(field_ch)
                    common_fields_new = [i+':'+j for i,j in zip(common_fields, common_fields_ch)]
                    common_fields_new = '\n'.join(list(common_fields_new))
                    self.G.add_edge(table1, table2, weight=len(common_fields), common_fields=str(common_fields_new))

    def visualize_graph(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为SimHei显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
        pos = nx.circular_layout(self.G)  # 使用spring_layout进行布局
        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', node_size=2000, edge_color='gray', font_size=10)
        labels = nx.get_edge_attributes(self.G, 'common_fields')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        # 将图保存为GraphML文件
        # nx.write_graphml(G, "d:\\dbbrain\\yhdb.graphml")
        plt.show()

    def main(self, excel_path, search):
        self.explore()
        self.infer_table_relationships()
        self.visualize_graph()
    def entry(self):
        input = entry.get()
        if len(input) > 0:
            main(input)
        entry_2.delete(0,t2)

def open_file():
    global input_file
    input_file = filedialog.askopenfilename()
    print(f"打开文件: {input_file}")

# 运行主函数，提供Excel文件路径作为参数
if __name__ == '__main__':
    input_file = ''
    tk = tkinter.Tk()
    tk.title('dbbrain')
    menubar = tkinter.Menu(tk)
    # 创建一个文件菜单
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label="打开文件", command=open_file)
    filemenu.add_separator()
    filemenu.add_command(label="退出", command=tk.quit)
    # 将文件菜单添加到菜单栏
    menubar.add_cascade(label="文件", menu=filemenu)
    # 将菜单栏设置为主窗口的菜单
    tk.config(menu=menubar)

    frame = tkinter.Frame(tk, width=260, height=400)
    frame.grid(row=0, column=0, sticky='w')
    entry = tkinter.Entry(frame)
    entry.grid(row=0, column=0, sticky='w')
    botton = tkinter.Button(frame, text='查询', font=('宋体',12,'normal'), command=search_data)
    botton.grid(row=0, column=1, sticky='e')

    #开始消息循环
    tk.mainloop()

    main(excel_path)
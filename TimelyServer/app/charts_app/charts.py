'''
    图表模块： 绘画图表，柱状图，折线图，生成pdf文件
'''
from app.charts_app.config_charts import Config_Charts
import datetime
import os 
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing
import random
import time


__slots__ = ['Generate_Report',]


# 注册字体
pdfmetrics.registerFont(
    TTFont(Config_Charts.typeface, Config_Charts.typefacefile))


def getLimitSteps(num):
    '''动态设置纵坐标的最大值'''
    if not num:
        return 100, 10
    tmp = num / 2 * 3
    return tmp, round(tmp/10, 0)


class Graphs:
    '''图形类'''
    def __init__(self):
        pass

    @staticmethod
    def draw_title(topic='日度报告'):
        '''绘制标题'''
        style = getSampleStyleSheet()
        ct = style['Normal']
        ct.fontName = Config_Charts.typeface
        ct.fontSize = 18
        # 设置行距
        ct.leading = 50
        # 颜色
        ct.textColor = Config_Charts.chose_colors[62]
        # 居中 
        ct.alignment = 1
        # 添加标题并居中 
        title = Paragraph(topic, ct)
        return title

    @staticmethod
    def draw_text(represent='时间段统计每天用户访问量，扫描的次数，验伪的次数'):
        '''绘制副标题'''
        style = getSampleStyleSheet()
        # 常规字体(非粗体或斜体) 
        ct = style['Normal']
        # 使用的字体s 
        ct.fontName = Config_Charts.typeface
        ct.fontSize = 14
        # 设置自动换行 
        ct.wordWrap = 'CJK'
        # 居左对齐 
        ct.alignment = 0
        # 第一行开头空格 
        ct.firstLineIndent = 32
        # 设置行距 
        ct.leading = 30
        text = Paragraph(represent, ct)
        return text

    @staticmethod
    def draw_table(*args):
        '''绘制表格'''
        col_width = 60
        style = [
            ('FONTNAME', (0, 0), (-1, -1), Config_Charts.typeface),  #  字体
            ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  #  设置第一行背景颜色
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  #  对齐
            ('VALIGN', (-1, 0), (-2, 0), 'MIDDLE'),  #  对齐 
            #  设置表格框线为grey色，线宽为0.5
            ('GRID', (0, 0), (-1, -1), 0.5, Config_Charts.chose_colors[61]),
        ]
        table = Table(args, colWidths=col_width, style=style)
        return table

    @staticmethod
    def draw_bar(bar_data=[], ax=[], items=[], limit_step=(100, 10), draw_weight=500, draw_height=250):
        '''绘制柱状图'''
        drawing = Drawing(draw_weight, draw_height)
        bc = VerticalBarChart()
        bc.x = 35
        bc.y = 100
        bc.height = 120
        bc.width = 350
        bc.data = bar_data
        bc.strokeColor = Config_Charts.chose_colors[15]
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = limit_step[0]
        bc.valueAxis.valueStep = limit_step[1]
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -10
        bc.categoryAxis.labels.angle = 20
        bc.categoryAxis.categoryNames = ax
        bc.bars.strokeColor = Config_Charts.chose_colors[148]
        for index, item in enumerate(items):
            bc.bars[index].fillColor = item[0]
        # 图示 
        leg = Legend()
        leg.fontName = Config_Charts.typeface
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 465
        leg.y = 220
        leg.dxTextSpace = 0
        leg.columnMaximum = 10
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(bc)
        return drawing

    @staticmethod
    def draw_line(line_data=[], ax=[], items=[], limit_step=(100, 10), draw_weight=500, draw_height=150):
        '''绘制折线图'''
        drawing = Drawing(draw_weight, draw_height)
        lc = SampleHorizontalLineChart()
        lc.x = 35
        lc.y = 100
        lc.height = 120
        lc.width = 350
        lc.data = line_data
        lc.strokeColor = Config_Charts.chose_colors[15]
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = limit_step[0]
        lc.valueAxis.valueStep = limit_step[1]
        lc.categoryAxis.labels.dx = 8
        lc.categoryAxis.labels.dy = -10
        lc.categoryAxis.labels.angle = 20
        lc.categoryAxis.categoryNames = ax
        for index, item in enumerate(items):
            lc.lines[index].strokeColor = item[0]
        # 图示 
        leg = Legend()
        leg.fontName = Config_Charts.typeface
        leg.alignment = 'right'
        leg.boxAnchor = 'ne'
        leg.x = 465
        leg.y = 200
        leg.dxTextSpace = 0
        leg.columnMaximum = 10
        leg.colorNamePairs = items
        drawing.add(leg)
        drawing.add(lc)
        return drawing


class Generate_Report:
    '''生成pdf类'''
    def __init__(self, title, notes, pagesize=Config_Charts.pagesize):
        self._pagesize = pagesize  # 设置纸张的大小
        now = datetime.datetime.now()
        self._report_name = 'report%s.pdf' % now.strftime(
            '%Y%m%d%H%M%S')  # 报表的名称
        self.title = title   # 报表的题目
        self.notes = notes   # 类型是tuple , 题目下面的注释
        self.content = []
        self.content.append(Graphs.draw_title(self.title))  #  添加标题  
        self.content.append(Graphs.draw_text(self.notes))  # 添加副标题

    def Template_1(self, g_data, desc,draw_table=True,draw_bar = True,draw_line=True, isdraw=False):
        '''
        模板1, 模板可扩展
        param g_data ： 传入的tuple 数据
        param desc ： 文本描述 
        param draw_table :  是否绘制 图表 
        param draw_bar ： 是否绘制 柱状图 
        param draw_line : 是否绘制 折线图
        param isdraw ： 是否开始绘制  只有isdraw 为True 时才绘制pdf,因此可以多次调用该模板增加内容
        '''
        max_num = 0
        if not g_data:
            raise 'TypeError: NoneType object is not iterable'
        t_data, b_data, ax_data, leg_items = g_data

        for ii in b_data:
            tmp = max(ii)
            if tmp > max_num:
                max_num = tmp
        self.content.append(Graphs.draw_text(represent=desc))  #  添加段落
        if draw_table:
            self.content.append(Graphs.draw_table(*t_data))  #  添加表格数据
        if draw_bar:
            self.content.append(Graphs.draw_bar(
                b_data, ax_data, leg_items, getLimitSteps(max_num)))  # 添加直方图
        if draw_line:
            if len(b_data[0]) != 1:
                self.content.append(Graphs.draw_line(
                    b_data, ax_data, leg_items, getLimitSteps(max_num)))  # 添加折线图
        if isdraw:
            self.pdf()

    def pdf(self):
        '''生成pdf'''
        pdf_path = os.path.dirname(os.getcwd())+  '/report/'
        if not os.path.exists(pdf_path):
            os.mkdir(pdf_path)
        log_name = pdf_path + self._report_name
        doc = SimpleDocTemplate(
            log_name, pagesize=self._pagesize)  #  生成pdf文件
        doc.build(self.content)

    # 获取报表的名称
    @property
    def report_name(self):
        '''获取报表名的属性'''
        return self._report_name


if __name__ == "__main__":
    # content = list()  #  添加标题 
    # b_data = [(50, 80, 60, 35, 40, 45),
    #           (25, 60, 55, 45, 60, 80),
    #           (30, 90, 75, 80, 50, 46)]
    # ax_data = ['2019-1', '2019-2', '2019-3', '2019-4', '2019-5', '2019-6']
    # leg_items = [
    #     (Config_Charts.chose_colors[124], '开发'),
    #     (Config_Charts.chose_colors[62], '编程'),
    #     (Config_Charts.chose_colors[17], '敲代码')]
    # content.append(Graphs.draw_line(b_data, ax_data, leg_items))  #  生成pdf文件
    # doc = SimpleDocTemplate('123.pdf')  #  生成pdf文件
    # doc.build(content)

     # t_data = [('开发',50, 80, 60, 35, 40, 45),
    #           ('编程',25, 60, 55, 45, 60, 80),
    #           ('敲代码',30, 90, 75, 80, 50, 46)]

    # gr = Generate_Report('程序员的一天','程序员的一天在干了什么')
    # from reportlab.lib.colors import  Color

    # per_res = ([('统计日期', 'morning', 'forenoon', 'noon', 'afternoon', 'evening'), ('访问次数', 357, 5610, 4599, 6607, 8751), ('扫码次数', 18, 390, 342, 550, 513), ('验伪次数', 33, 548, 526, 803, 1127)], [(357, 5610, 4599, 6607, 8751), (18, 390, 342, 550, 513), (33, 548, 526, 803, 1127)], ('morning', 'forenoon', 'noon', 'afternoon', 'evening'), [(Color(1,.854902,.72549,1), '访问次数'), (Color(.576471,.439216,.858824,1), '扫码次数'), (Color(.980392,.980392,.823529,1), '验伪次数')])
    # gr.Template_1(per_res,'time_period',isdraw=False)
    # day_res = ([('统计日期', '2019-08-06', '2019-08-07'), ('访问次数', 4493, 4483), ('扫码次数', 1825, 1813), ('验伪次数', 2822, 3037)], [(4493, 4483), (1825, 1813), (2822, 3037)], ('2019-08-06', '2019-08-07'), [(Color(.545098,.270588,.07451,1), '访问次数'), (Color(.2,.4,.8,1), '扫码次数'), (Color(.858824,.439216,.576471,1), '验伪次数')])
    # gr.Template_1(day_res,'time_day',isdraw=True)

    pass
    

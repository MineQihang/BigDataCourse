#!/usr/bin/env python3
#coding: UTF-8
"""
@author: huangwanghui
@time: 2020/1/25 22:14
"""

import os
from wordcloud import WordCloud
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Funnel, Scatter

# 解决错误：Running as root without --no-sandbox is not supported.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

SAVAPATH = '/home/hadoop/Experiment/Ex2_WordCount/results/'

class visualize:

    def rdd2dic(self,resRdd,topK):
        """
        将RDD转换为Dic，并截取指定长度topK
        :param resRdd: 词频统计降序排序结果RDD
        :param topK: 截取的指定长度
        :return:
        """

        # 提示：SparkRdd有函数可直接转换
        # 【现在你应该完成下面函数编码】
        resDic = resRdd.collectAsMap()
        # 截取字典前K个
        K = 0
        wordDicK = {}
        for key, value in resDic.items():
            # 完成循环截取字典
            if K >= topK:
                break
            wordDicK[key] = value
            K += 1
        return wordDicK

    def drawWorcCloud(self, wordDic):
        """
        根据词频字典，进行词云可视化
        :param wordDic: 词频统计字典
        :return:
        """
        # 生成词云
        wc = WordCloud(font_path='/usr/share/fonts/wqy-microhei/wqy-microhei.ttc',
                       background_color='white',
                       max_words=2000,
                       width=1920, height=1080,
                       margin=5)
        wc.generate_from_frequencies(wordDic)
        # 保存结果
        if not os.path.exists(SAVAPATH):
            os.makedirs(SAVAPATH)
        wc.to_file(os.path.join(SAVAPATH, '词云可视化.png'))

    def drawPie(self, wordDic):
        """
        饼图可视化
        :param wordDic: 词频统计字典
        :return:
        """
        key_list = wordDic.keys()      # wordDic所有key组成list
        value_list= wordDic.values()   # wordDic所有value组成list
        def pie_position() -> Pie:
            c = (
                Pie()
                    .add
                    (
                    "",
                    [list(z) for z in zip(key_list, value_list)], # dic -> list
                    center=["35%", "50%"],
                    )
                    .set_global_opts
                    (
                    title_opts=opts.TitleOpts(title='饼图可视化'), # 设置标题
                    legend_opts=opts.LegendOpts(pos_left="15%"),
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            return c
        # 保存结果
        make_snapshot(snapshot, pie_position().render(), SAVAPATH + '饼图可视化.png')

    def drawBar(self, wordDic):
        """
        柱状图可视化
        :param wordDic: 词频统计字典
        :return:
        """
        key_list = wordDic.keys()      # wordDic所有key组成list
        value_list= wordDic.values()   # wordDic所有value组成list
        def bar_position() -> Bar:
            bar = (
                Bar()
                    .add_xaxis(list(key_list))
                    .add_yaxis("次数", list(value_list))
                    .set_global_opts
                    (
                    title_opts=opts.TitleOpts(title='柱状图可视化'), # 设置标题
                    legend_opts=opts.LegendOpts(pos_left="15%"),
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
            return bar
        # 保存结果
        make_snapshot(snapshot, bar_position().render(), SAVAPATH + '柱状图可视化.png')

    def drawFunnel(self, wordDic):
        """
        漏斗图可视化
        :param wordDic: 词频统计字典
        :return:
        """
        key_list = list(wordDic.keys())      # wordDic所有key组成list
        value_list= list(wordDic.values())   # wordDic所有value组成list
        data = [[key_list[i],value_list[i]]for i in range(len(key_list))]
        def funnel_position() -> Funnel:
            funnel = (
                Funnel()
                    .add(
                        series_name="",
                        data_pair=data,
                        gap=2,
                        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
                        label_opts=opts.LabelOpts(is_show=True, position="inside"),
                        itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
                    )
                    .set_global_opts(title_opts=opts.TitleOpts(title="漏斗图"))
            )
            return funnel
        # 保存结果
        make_snapshot(snapshot, funnel_position().render(), SAVAPATH + '漏斗图可视化.png')

    def drawScatter(self, wordDic):
        """
        散点图可视化
        :param wordDic: 词频统计字典
        :return:
        """
        key_list = list(wordDic.keys())      # wordDic所有key组成list
        value_list= list(wordDic.values())   # wordDic所有value组成list
        def scatter_position() -> Funnel:
            scatter = (
                Scatter()
                    .add_xaxis(key_list)
                    .add_yaxis("次数", value_list)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title="Scatter-VisualMap(Size)"),
                        visualmap_opts=opts.VisualMapOpts(type_="size", max_=150, min_=20),
                    )
            )
            return scatter
        # 保存结果
        make_snapshot(snapshot, scatter_position().render(), SAVAPATH + '散点图可视化.png')


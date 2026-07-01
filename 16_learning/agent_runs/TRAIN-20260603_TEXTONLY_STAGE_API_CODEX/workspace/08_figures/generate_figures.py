#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表生成脚本
运行环境：Python 3.8+, matplotlib, pandas, numpy
输入：07_results/ 中的冻结结果 CSV
输出：08_figures/ 中的 SVG/PNG 图表
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 中文字体配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

RESULTS_DIR = os.path.join('..', '07_results')
FIG_DIR = '.'

def load_csv(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"结果文件 {path} 不存在，请先运行相应上游阶段。")
    return pd.read_csv(path, encoding='utf-8')

def plot_weight_heatmap(weights_df, output='fig1_weight_heatmap'):
    """FIG001: 指标权重热力图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # weights_df: 行=城市/方案，列=指标
    cmap = plt.cm.RdYlBu_r  # 类似 teal_orange_diverging
    im = ax.imshow(weights_df.values, aspect='auto', cmap=cmap)
    ax.set_xticks(range(len(weights_df.columns)))
    ax.set_xticklabels(weights_df.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(weights_df.index)))
    ax.set_yticklabels(weights_df.index)
    ax.set_title('指标权重热力图', fontsize=16)
    plt.colorbar(im, ax=ax, label='权重值')
    plt.tight_layout()
    plt.savefig(f'{output}.svg', dpi=150)
    plt.savefig(f'{output}.png', dpi=150)
    plt.close()
    print(f'FIG001 保存至 {output}.svg/png')

def plot_score_ranking(scores_df, output='fig2_score_ranking'):
    """FIG002: 综合得分排序图"""
    fig, ax = plt.subplots(figsize=(8, 5))
    scores = scores_df.set_index('city')['score'].sort_values()
    colors = ['#3A7CA5'] * len(scores)
    ax.barh(scores.index, scores.values, color=colors, edgecolor='#D4A373', linewidth=1.2)
    ax.set_xlabel('综合得分')
    ax.set_title('城市综合得分排序', fontsize=16)
    for i, v in enumerate(scores.values):
        ax.text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(f'{output}.svg', dpi=150)
    plt.savefig(f'{output}.png', dpi=150)
    plt.close()
    print(f'FIG002 保存至 {output}.svg/png')

def plot_sensitivity(sensitivity_df, output='fig3_sensitivity'):
    """FIG003: 敏感性分析热力图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.bwr
    im = ax.imshow(sensitivity_df.values, aspect='auto', cmap=cmap, vmin=-1, vmax=1)
    ax.set_xticks(range(len(sensitivity_df.columns)))
    ax.set_xticklabels(sensitivity_df.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(sensitivity_df.index)))
    ax.set_yticklabels(sensitivity_df.index)
    ax.set_title('参数敏感性热力图', fontsize=16)
    plt.colorbar(im, ax=ax, label='排名变化相关系数')
    plt.tight_layout()
    plt.savefig(f'{output}.svg', dpi=150)
    plt.savefig(f'{output}.png', dpi=150)
    plt.close()
    print(f'FIG003 保存至 {output}.svg/png')

if __name__ == '__main__':
    try:
        weights = load_csv('weights.csv')
        plot_weight_heatmap(weights)
    except FileNotFoundError as e:
        print(f'权重图生成跳过：{e}')
    try:
        scores = load_csv('scores.csv')
        plot_score_ranking(scores)
    except FileNotFoundError as e:
        print(f'得分图生成跳过：{e}')
    try:
        sensitivity = load_csv('sensitivity.csv')
        plot_sensitivity(sensitivity)
    except FileNotFoundError as e:
        print(f'敏感性图生成跳过：{e}')
    print('图表生成脚本执行完毕。')

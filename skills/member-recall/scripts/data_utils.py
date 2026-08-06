#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
member-recall 数据处理工具
仅包含确定性数据处理逻辑，无外部LLM调用。
由 Claude 在执行 skill 过程中按需调用。
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


def _ensure_utf8_streams() -> None:
    """Re-wrap stdout/stderr as utf-8 so print() of ✓/⚠/中文 never crashes on GBK terminals."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'buffer') and stream.encoding and stream.encoding.lower() != 'utf-8':
            stream.reconfigure(encoding='utf-8', errors='replace')


_ensure_utf8_streams()


# ─────────────────────────────────────────────
# 敏感词库
# ─────────────────────────────────────────────
SENSITIVE_WORDS = {
    '违禁词': [
        {'word': '最高', 'replacement': '高品质'},
        {'word': '国家级', 'replacement': ''},
        {'word': '最佳', 'replacement': '优质'},
        {'word': '第一', 'replacement': '领先'},
        {'word': '顶级', 'replacement': '高端'},
        {'word': '顶尖', 'replacement': '卓越'},
        {'word': '绝对', 'replacement': '非常'},
        {'word': '100%', 'replacement': '高品质'},
    ],
    '极限词': [
        {'word': '唯一', 'replacement': '仅有'},
        {'word': '首选', 'replacement': '推荐'},
        {'word': '首家', 'replacement': '较早推出'},
        {'word': '最先进', 'replacement': '先进'},
    ],
    '诱导性词': [
        {'word': '立即抢购', 'warning': True},
        {'word': '过期不候', 'warning': True},
        {'word': '马上领取', 'warning': True},
        {'word': '不容错过', 'warning': True},
        {'word': '最后机会', 'warning': True},
        {'word': '限时优惠', 'warning': True},
    ],
    '个人信息暗示': [
        {'word': '身份证', 'warning': True},
        {'word': '银行卡', 'warning': True},
        {'word': '密码', 'warning': True},
        {'word': '验证码', 'warning': True},
    ],
    '虚假宣传': [
        {'word': '保证收益', 'warning': True},
        {'word': '无风险', 'warning': True},
        {'word': '100%有效', 'warning': True},
        {'word': '根治', 'warning': True},
        {'word': '彻底治愈', 'warning': True},
    ],
}

REQUIRED_FIELDS = [
    'member_id', 'last_purchase_days', 'total_purchase_count',
    'total_spend', 'coupon_usage_rate', 'avg_order_value', 'days_since_register',
]

GENERIC_COPY = '亲爱的会员，我们一直想念您，期待您的归来。'


# ─────────────────────────────────────────────
# 数据加载与验证
# ─────────────────────────────────────────────
def load_member_data(filepath: str) -> pd.DataFrame:
    """加载会员数据并验证必需字段。"""
    df = pd.read_csv(filepath)
    if len(df) == 0:
        print("⚠️ 输入文件没有数据行", file=sys.stderr)
        sys.exit(1)
    missing = [f for f in REQUIRED_FIELDS if f not in df.columns]
    if missing:
        print(f"⚠️ 缺少必需字段: {', '.join(missing)}", file=sys.stderr)
        print(f"   文件实际字段: {', '.join(df.columns.tolist())}", file=sys.stderr)
        sys.exit(1)
    print(f"✓ 已加载 {len(df)} 条会员记录，字段验证通过")
    return df


# ─────────────────────────────────────────────
# 数据画像（供 Claude 进行动机洞察使用）
# ─────────────────────────────────────────────
def compute_data_profile(df: pd.DataFrame) -> dict:
    """计算会员行为画像，输出结构化摘要供动机洞察分析。"""

    profile = {}
    profile['total_members'] = len(df)

    # ── RFM 分层 ──
    # 沉睡时长分布
    recency_bins = [0, 30, 90, 180, 365, float('inf')]
    recency_labels = ['<30天', '30-90天', '90-180天', '180-365天', '365天以上']
    df['_recency_seg'] = pd.cut(df['last_purchase_days'], bins=recency_bins, labels=recency_labels, right=False)
    profile['recency_distribution'] = df['_recency_seg'].value_counts().sort_index().to_dict()

    # 购买频次分布
    freq_bins = [0, 1, 5, 20, float('inf')]
    freq_labels = ['1次', '2-5次', '6-20次', '20次以上']
    df['_freq_seg'] = pd.cut(df['total_purchase_count'], bins=freq_bins, labels=freq_labels, right=False)
    profile['frequency_distribution'] = df['_freq_seg'].value_counts().sort_index().to_dict()
    # 消费金额分层
    spend_quartiles = df['total_spend'].quantile([0.25, 0.5, 0.75, 0.9]).to_dict()
    profile['spend_quartiles'] = {f'P{int(k*100)}': round(v, 2) for k, v in spend_quartiles.items()}

    # 高价值用户占比
    p90 = df['total_spend'].quantile(0.9)
    top10pct = df[df['total_spend'] >= p90]
    profile['top10pct_revenue_share'] = round(top10pct['total_spend'].sum() / df['total_spend'].sum() * 100, 1)

    # ── 优惠券行为 ──
    profile['coupon_usage'] = {
        'mean': round(df['coupon_usage_rate'].mean(), 3),
        'median': round(df['coupon_usage_rate'].median(), 3),
        'pct_above_75': round((df['coupon_usage_rate'] > 0.75).mean() * 100, 1),
        'pct_above_50': round((df['coupon_usage_rate'] > 0.5).mean() * 100, 1),
        'pct_zero': round((df['coupon_usage_rate'] == 0).mean() * 100, 1),
    }

    # ── 会员生命周期 ──
    profile['tenure'] = {
        'mean_days': round(df['days_since_register'].mean(), 0),
        'median_days': round(df['days_since_register'].median(), 0),
        'pct_under_180d': round((df['days_since_register'] < 180).mean() * 100, 1),
        'pct_over_730d': round((df['days_since_register'] > 730).mean() * 100, 1),
    }

    # 平均订单金额分布
    profile['aov'] = {
        'mean': round(df['avg_order_value'].mean(), 2),
        'median': round(df['avg_order_value'].median(), 2),
        'p25': round(df['avg_order_value'].quantile(0.25), 2),
        'p75': round(df['avg_order_value'].quantile(0.75), 2),
    }

    # ── 交叉分析 ──
    # 高优惠券使用 + 低消费 → 价格敏感
    price_sensitive = df[(df['coupon_usage_rate'] > 0.7) & (df['total_spend'] < df['total_spend'].median())]
    profile['segment_hints'] = {
        'price_sensitive_count': len(price_sensitive),
        'price_sensitive_pct': round(len(price_sensitive) / len(df) * 100, 1),
    }

    # 高客单 + 低优惠券 → 品质追求
    quality_seeker = df[(df['coupon_usage_rate'] < 0.3) & (df['avg_order_value'] > df['avg_order_value'].quantile(0.75))]
    profile['segment_hints']['quality_seeker_count'] = len(quality_seeker)
    profile['segment_hints']['quality_seeker_pct'] = round(len(quality_seeker) / len(df) * 100, 1)

    # 高频但近期停止 → 习惯中断
    habitual = df[(df['total_purchase_count'] > 10) & (df['last_purchase_days'] > 90)]
    profile['segment_hints']['habitual_interrupted_count'] = len(habitual)
    profile['segment_hints']['habitual_interrupted_pct'] = round(len(habitual) / len(df) * 100, 1)

    # 低频次低消费 → 低参与
    low_engagement = df[(df['total_purchase_count'] <= 2) & (df['total_spend'] < df['total_spend'].quantile(0.25))]
    profile['segment_hints']['low_engagement_count'] = len(low_engagement)
    profile['segment_hints']['low_engagement_pct'] = round(len(low_engagement) / len(df) * 100, 1)

    # 清理临时列（不改变调用方的 DataFrame）
    df = df.drop(columns=['_recency_seg', '_freq_seg'], errors='ignore')

    return profile


# ─────────────────────────────────────────────
# 敏感词检测
# ─────────────────────────────────────────────
def check_sensitive_words(copy_library: dict) -> tuple:
    """
    检测文案库中的敏感词。
    返回 (处理后的文案库, 警告列表)。
    """
    warnings = []

    def process_text(text, motivation, copy_id):
        processed = text
        local_warnings = []
        for category, words in SENSITIVE_WORDS.items():
            for item in words:
                word = item['word']
                if word in processed:
                    if 'replacement' in item and item['replacement']:
                        processed = processed.replace(word, item['replacement'])
                    local_warnings.append({
                        'category': category,
                        'word': word,
                        'motivation': motivation,
                        'copy_id': copy_id,
                        'suggestion': item.get('replacement', '请修改'),
                        'auto_fixed': 'replacement' in item and bool(item['replacement']),
                    })
        return processed, local_warnings

    processed_library = {}
    for motivation, copies in copy_library.items():
        processed_library[motivation] = {}
        if isinstance(copies, dict):
            for copy_id, text in copies.items():
                processed_text, local_warnings = process_text(text, motivation, copy_id)
                processed_library[motivation][copy_id] = processed_text
                warnings.extend(local_warnings)
        else:
            processed_library[motivation] = copies

    return processed_library, warnings


# ─────────────────────────────────────────────
# 启发式匹配
# ─────────────────────────────────────────────
def _get_style_from_id(copy_id: str) -> str:
    if 'StyleA' in copy_id or 'Premium' in copy_id:
        return 'Premium'
    if 'StyleB' in copy_id or 'Benefit' in copy_id:
        return 'Benefit'
    if 'StyleC' in copy_id or 'Emotional' in copy_id:
        return 'Emotional'
    return 'Standard'


def _segment_users(df: pd.DataFrame) -> pd.Series:
    """Segment users into HighValue / PriceSensitive / Standard based on data thresholds.

    HighValue (P90 spend) takes priority over PriceSensitive (P75 coupon) so a high-spending
    user is never downgraded to a benefit-driven message.
    """
    high_value_threshold = df['total_spend'].quantile(0.90)
    price_sensitive_threshold = df['coupon_usage_rate'].quantile(0.75)
    conditions = [
        df['total_spend'] >= high_value_threshold,            # HighValue 优先
        df['coupon_usage_rate'] >= price_sensitive_threshold,  # 然后 PriceSensitive
    ]
    choices = ['HighValue', 'PriceSensitive']
    return pd.Series(np.select(conditions, choices, default='Standard'), index=df.index)


def heuristic_matching(df: pd.DataFrame, approved_copy: dict) -> pd.DataFrame:
    """基于专家规则的冷启动匹配。"""
    df = df.copy()
    # 确保每行都有动机标签（match 独立调用时输入 CSV 无该列）
    if 'llm_motivation_label' not in df.columns:
        motivation_keys = [k for k in approved_copy.keys() if approved_copy.get(k)]
        if not motivation_keys:
            motivation_keys = list(approved_copy.keys())
        if motivation_keys:
            df['llm_motivation_label'] = np.random.choice(motivation_keys, len(df))
        else:
            df['llm_motivation_label'] = 'A'
    df['user_segment'] = _segment_users(df)

    rng = random.Random(42)  # local instance, no global state pollution

    def match_copy(row):
        motivation = row.get('llm_motivation_label', 'A')
        segment = row['user_segment']
        available = approved_copy.get(motivation, {})
        if not available:
            for m, c in approved_copy.items():
                if c:
                    available = c
                    break
        if not available:
            return pd.Series(['期待您再度尊享我们的服务。', 'DEFAULT-01'])

        if segment == 'HighValue':
            premium = {k: v for k, v in available.items() if _get_style_from_id(k) == 'Premium'}
            if premium:
                cid = rng.choice(list(premium.keys()))
                return pd.Series([premium[cid], cid])
        if segment == 'PriceSensitive':
            benefit = {k: v for k, v in available.items() if _get_style_from_id(k) == 'Benefit'}
            if benefit:
                cid = rng.choice(list(benefit.keys()))
                return pd.Series([benefit[cid], cid])

        cid = rng.choice(list(available.keys()))
        return pd.Series([available[cid], cid])

    df[['assigned_copy_text', 'assigned_copy_id']] = df.apply(match_copy, axis=1)
    return df


# ─────────────────────────────────────────────
# A/B 分组
# ─────────────────────────────────────────────
def generate_ab_groups(
    df: pd.DataFrame,
    approved_copy: dict,
    motivations: dict,
    test_ratio: float = 0.5,
    generic_copy: str = GENERIC_COPY,
) -> tuple:
    """生成 A/B 测试人群包。"""
    df = df.copy()
    motivation_keys = list(motivations.keys())
    df['llm_motivation_label'] = np.random.choice(motivation_keys, len(df))
    df['user_segment'] = _segment_users(df)

    control_idx = df.sample(frac=test_ratio, random_state=42).index
    ai_group = df.drop(control_idx).copy()
    control_group = df.loc[control_idx].copy()

    ai_group = heuristic_matching(ai_group, approved_copy)
    ai_group['ab_group'] = 'AI'

    control_group['assigned_copy_text'] = generic_copy
    control_group['assigned_copy_id'] = 'GENERIC-01'
    control_group['ab_group'] = 'CONTROL'

    return ai_group, control_group


# ─────────────────────────────────────────────
# 测试数据生成
# ─────────────────────────────────────────────
def generate_test_data(output_file: str, num_records: int = 10000):
    """生成测试用会员数据。"""
    np.random.seed(42)
    data = {
        'member_id': [f'M{i:08d}' for i in range(1, num_records + 1)],
        'last_purchase_days': np.random.randint(30, 365, num_records),
        'total_purchase_count': np.random.randint(1, 50, num_records),
        'total_spend': np.random.exponential(5000, num_records).round(2),
        'coupon_usage_rate': np.random.beta(2, 5, num_records).round(3),
        'avg_order_value': np.random.exponential(200, num_records).round(2),
        'days_since_register': np.random.randint(90, 1000, num_records),
    }
    df = pd.DataFrame(data)
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✓ 已生成 {num_records} 条测试数据: {output_file}")
    return df


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='member-recall 数据处理工具')
    parser.add_argument('--action', required=True,
                        choices=['profile', 'sensitive-check', 'match', 'ab-split', 'generate-test'],
                        help='执行的操作')
    parser.add_argument('--input', type=str, help='输入文件路径 (CSV 或 JSON)')
    parser.add_argument('--copy', type=str, help='文案库 JSON 文件路径')
    parser.add_argument('--motivations', type=str, help='动机 JSON 文件路径')
    parser.add_argument('--ratio', type=float, default=0.5, help='对照组比例 (默认 0.5)')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--num', type=int, default=10000, help='测试数据条数 (默认 10000)')
    args = parser.parse_args()

    if args.action == 'generate-test':
        out = args.output or 'data/test_members.csv'
        generate_test_data(out, args.num)

    elif args.action == 'profile':
        if not args.input:
            parser.error('--input is required for profile')
        df = load_member_data(args.input)
        profile = compute_data_profile(df)
        print(json.dumps(profile, ensure_ascii=False, indent=2))

    elif args.action == 'sensitive-check':
        if not args.copy:
            parser.error('--copy is required for sensitive-check')
        with open(args.copy, 'r', encoding='utf-8') as f:
            copy_lib = json.load(f)
        processed, warnings = check_sensitive_words(copy_lib)
        result = {'processed_library': processed, 'warnings': warnings}
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == 'match':
        if not args.input or not args.copy:
            parser.error('--input and --copy are required for match')
        df = load_member_data(args.input)
        with open(args.copy, 'r', encoding='utf-8') as f:
            copy_lib = json.load(f)
        # 可选：用户提供的动机分布覆盖默认随机分配
        if args.motivations:
            with open(args.motivations, 'r', encoding='utf-8') as f:
                motivations = json.load(f)
            motivation_keys = [k for k in motivations.keys() if copy_lib.get(k)]
            if motivation_keys:
                df['llm_motivation_label'] = np.random.choice(motivation_keys, len(df))
        result = heuristic_matching(df, copy_lib)
        out = args.output or 'data/matched.csv'
        result.to_csv(out, index=False, encoding='utf-8-sig')
        print(f"✓ 匹配完成: {out} ({len(result)} 条)")

    elif args.action == 'ab-split':
        if not args.input or not args.copy or not args.motivations:
            parser.error('--input, --copy, and --motivations are required for ab-split')
        df = load_member_data(args.input)
        with open(args.copy, 'r', encoding='utf-8') as f:
            copy_lib = json.load(f)
        with open(args.motivations, 'r', encoding='utf-8') as f:
            motivations = json.load(f)
        ai_group, control_group = generate_ab_groups(df, copy_lib, motivations, args.ratio)
        today = datetime.now().strftime('%Y%m%d')
        out_dir = Path(args.output or 'data')
        out_dir.mkdir(parents=True, exist_ok=True)
        ai_file = out_dir / f'ai_group_{today}.csv'
        ctrl_file = out_dir / f'control_group_{today}.csv'
        ai_group.to_csv(ai_file, index=False, encoding='utf-8-sig')
        control_group.to_csv(ctrl_file, index=False, encoding='utf-8-sig')
        print(f"✓ AI组: {len(ai_group)} 人 -> {ai_file}")
        print(f"✓ 对照组: {len(control_group)} 人 -> {ctrl_file}")


if __name__ == '__main__':
    main()

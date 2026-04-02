# production_crm_assistant.py
# 版本 4.0 - 生产级/交互式/冷启动/含敏感词检测/对照组通用文案

import pandas as pd
import numpy as np
import json
import random
import time
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 尝试导入anthropic，如果不可用则使用openai
try:
    import anthropic
    USE_ANTHROPIC = True
except ImportError:
    import openai
    USE_ANTHROPIC = False


# --- 工具函数: 生成测试数据 ---
def generate_test_data(output_file: str, num_records: int = 10000):
    """
    生成测试会员数据
    """
    np.random.seed(42)

    data = {
        'member_id': [f'M{i:08d}' for i in range(1, num_records + 1)],
        'last_purchase_days': np.random.randint(30, 365, num_records),
        'total_purchase_count': np.random.randint(1, 50, num_records),
        'total_spend': np.random.exponential(5000, num_records).round(2),
        'coupon_usage_rate': np.random.beta(2, 5, num_records).round(3),
        'avg_order_value': np.random.exponential(200, num_records).round(2),
        'days_since_register': np.random.randint(90, 1000, num_records)
    }

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"已生成 {num_records} 条测试数据到: {output_file}")
    return df


# --- 模块0: 敏感词检测 ---
SENSITIVE_WORDS = {
    'forbidden': [
        {'word': '最高', 'replacement': '高品质'},
        {'word': '国家级', 'replacement': ''},
        {'word': '最佳', 'replacement': '优质'},
        {'word': '第一', 'replacement': '领先'},
        {'word': '顶级', 'replacement': '高端'},
        {'word': '顶尖', 'replacement': '卓越'},
        {'word': '绝对', 'replacement': '非常'},
        {'word': '100%', 'replacement': '高品质'}
    ],
    'extreme': [
        {'word': '唯一', 'replacement': '仅有'},
        {'word': '首选', 'replacement': '推荐'},
        {'word': '首家', 'replacement': '较早推出'},
        {'word': '最先进', 'replacement': '先进'}
    ],
    'inducing': [
        {'word': '立即抢购', 'warning': True},
        {'word': '过期不候', 'warning': True},
        {'word': '马上领取', 'warning': True},
        {'word': '不容错过', 'warning': True},
        {'word': '最后机会', 'warning': True},
        {'word': '限时优惠', 'warning': True}
    ],
    'personal_info': [
        {'word': '身份证', 'warning': True},
        {'word': '银行卡', 'warning': True},
        {'word': '密码', 'warning': True},
        {'word': '验证码', 'warning': True}
    ],
    'false_claim': [
        {'word': '保证收益', 'warning': True},
        {'word': '无风险', 'warning': True},
        {'word': '100%有效', 'warning': True},
        {'word': '根治', 'warning': True},
        {'word': '彻底治愈', 'warning': True}
    ]
}


def check_sensitive_words(copy_library: dict) -> tuple:
    """
    检测文案库中的敏感词
    返回: (processed_library, warnings)
    """
    warnings = []

    def process_text(text):
        """处理单个文案，替换敏感词"""
        processed_text = text
        local_warnings = []

        for category, words in SENSITIVE_WORDS.items():
            for item in words:
                word = item['word']
                if word in processed_text:
                    if 'replacement' in item and item['replacement']:
                        # 替换违禁词
                        processed_text = processed_text.replace(word, item['replacement'])
                    local_warnings.append({
                        'category': category,
                        'word': word,
                        'suggestion': item.get('replacement', '请修改')
                    })

        return processed_text, local_warnings

    processed_library = {}

    for motivation, copies in copy_library.items():
        processed_library[motivation] = {}
        if isinstance(copies, dict):
            for copy_id, text in copies.items():
                processed_text, local_warnings = process_text(text)
                processed_library[motivation][copy_id] = processed_text
                warnings.extend(local_warnings)
        else:
            # 处理非字典格式的文案
            processed_library[motivation] = copies

    return processed_library, warnings


def get_sensitive_words_warning(copy_library: dict) -> list:
    """
    获取敏感词警告列表（不修改文案）
    """
    warnings = []

    for motivation, copies in copy_library.items():
        if isinstance(copies, dict):
            for copy_id, text in copies.items():
                for category, words in SENSITIVE_WORDS.items():
                    for item in words:
                        word = item['word']
                        if word in text:
                            warnings.append({
                                'category': category,
                                'word': word,
                                'copy_id': copy_id,
                                'suggestion': item.get('replacement', '请修改')
                            })

    return warnings


# --- 模块0.5: 品牌调性确认 ---
def confirm_brand_tone() -> dict:
    """
    步骤1.5: 确认品牌调性
    """
    print("【步骤1.5/5: 品牌调性确认】请提供以下信息：\n")

    # 品牌名称
    brand_name = input("1. 品牌名称：").strip()

    # 品牌调性选择
    print("\n2. 品牌调性（单选或多选）：")
    print("   A. 高端奢华 - 强调品质、尊贵、专属服务 (示例：LV、香奈儿、劳力士)")
    print("   B. 亲民实惠 - 强调性价比、优惠活动 (示例：小米、优衣库、蜜雪冰城)")
    print("   C. 情感温暖 - 强调陪伴、回忆、情感连接 (示例：可口可乐、旺旺、999感冒灵)")
    print("   D. 简约时尚 - 强调设计感、潮流 (示例：无印良品、苹果、优衣库)")

    brand_tone_choice = input("\n请输入调性字母（可多选，如AB）: ").strip().upper()
    tone_mapping = {
        'A': '高端奢华',
        'B': '亲民实惠',
        'C': '情感温暖',
        'D': '简约时尚'
    }
    brand_tones = [tone_mapping.get(c, c) for c in brand_tone_choice]

    # 品牌其他特点
    brand_features = input("\n3. 品牌其他特点（可选描述）: ").strip()

    brand_info = {
        'name': brand_name,
        'tones': brand_tones,
        'features': brand_features
    }

    print("\n确认的品牌信息：")
    print(f"  品牌名称: {brand_info['name']}")
    print(f"  品牌调性: {', '.join(brand_info['tones'])}")
    if brand_info['features']:
        print(f"  品牌特点: {brand_info['features']}")

    return brand_info


# --- 模块1: 交互式动机定义 ---
def propose_and_confirm_motivations(df: pd.DataFrame, api_key: str) -> dict:
    """
    步骤1: 由LLM基于真实数据摘要，生成动机初稿，等待用户确认。
    """
    print("ACTION: Generating motivation proposals based on data summary...")
    sample_summary = df.sample(min(100, len(df))).describe(include='all').to_string()

    prompt = f"""
# 角色
你是一位顶级的CRM数据策略师。

# 任务
基于以下的用户数据摘要，为"会员沉睡/流失"这个现象，归纳出4个最核心、最有代表性的原因。你的归纳需要具有普遍性，并为每个原因附上一个简短但精准的描述。

# 数据摘要
{sample_summary}

# 输出格式
请严格按照以下JSON格式输出，不要包含任何额外的解释：
{{
  "A": "描述...",
  "B": "描述...",
  "C": "描述...",
  "D": "描述..."
}}
"""

    if USE_ANTHROPIC:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        proposed_motivations = json.loads(response.content[0].text)
    else:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        proposed_motivations = json.loads(response.choices[0].message['content'])

    # 关键的交互点
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤1/5: 动机洞察】AI已生成初步的动机分类，请审核、修改或直接确认：")
    print(json.dumps(proposed_motivations, indent=2, ensure_ascii=False))

    confirmed_motivations_str = input("请输入您最终确认的JSON（直接回车确认上述内容）: ").strip()
    if confirmed_motivations_str:
        return json.loads(confirmed_motivations_str)
    return proposed_motivations


# --- 模块2: 交互式文案生成与审核 ---
def propose_and_confirm_copy(motivations: dict, brand_info: dict, api_key: str) -> dict:
    """
    步骤2: 为已确认的动机，生成文案初稿，等待用户审核确认。
    """
    print("ACTION: Generating copy drafts for confirmed motivations...")

    # 构建品牌调性提示
    brand_tones = brand_info.get('tones', ['高端奢华'])
    brand_tone_prompt = "、".join(brand_tones)

    proposed_library = {}
    for key, desc in motivations.items():
        prompt = f"""
# 角色
你是一位资深的品牌营销文案专家。

# 任务
请针对以下用户类型，创作3版不同风格的短信召回文案。

# 用户类型描述
{key}: {desc}

# 品牌调性要求
品牌调性：{brand_tone_prompt}

# 重要约束
1. 禁止使用具体天数（如"100+天"）或具体购买次数（如"8次购买"）等动态数据
2. 使用通用表述如"沉睡多时"、"期待您的归来"等
3. 文案应适配品牌调性

# 输出格式
请严格按照JSON格式输出，key为建议的文案ID，value为文案内容:
{{
  "{key}-StyleA": "文案内容...",
  "{key}-StyleB": "文案内容...",
  "{key}-StyleC": "文案内容..."
}}
"""

        if USE_ANTHROPIC:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            proposed_library[key] = json.loads(response.content[0].text)
        else:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            proposed_library[key] = json.loads(response.choices[0].message['content'])

    # 关键的交互点
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤2/5: 文案创生】AI已生成文案初稿。请挑选、修改并提供您最终要使用的JSON版本。")
    print("您可以删除不想要的文案，或修改文案内容。")
    print(json.dumps(proposed_library, indent=2, ensure_ascii=False))

    approved_copy_str = input("请输入您最终确认的JSON文案库（直接回车确认上述内容）: ").strip()
    if approved_copy_str:
        return json.loads(approved_copy_str)
    return proposed_library


# --- 模块3: 启发式规则匹配 (冷启动策略) ---
def heuristic_matching_cold_start(df: pd.DataFrame, approved_copy: dict) -> pd.DataFrame:
    """
    步骤3: 生产级的冷启动匹配策略，完全基于规则。
    """
    print("ACTION: Applying heuristic rules for cold-start matching...")

    # 定义文案风格（基于ID中的Style标签）
    def get_style_from_id(copy_id):
        if "StyleA" in copy_id: return "Premium"
        if "StyleB" in copy_id: return "Benefit"
        if "StyleC" in copy_id: return "Emotional"
        return "Standard"

    # 定义用户分层
    high_value_threshold = df['total_spend'].quantile(0.90)
    price_sensitive_threshold = df['coupon_usage_rate'].quantile(0.75)
    df = df.copy()
    df['user_segment'] = 'Standard'
    df.loc[df['total_spend'] >= high_value_threshold, 'user_segment'] = 'HighValue'
    df.loc[df['coupon_usage_rate'] >= price_sensitive_threshold, 'user_segment'] = 'PriceSensitive'

    # 启发式匹配逻辑
    def match_copy(row):
        motivation = row.get('llm_motivation_label', 'A')
        segment = row['user_segment']

        # 获取该动机下所有已批准的文案
        available_copies = approved_copy.get(motivation, {})
        if not available_copies:
            # 尝试获取任意动机的文案作为后备
            for m, c in approved_copy.items():
                if c:
                    available_copies = c
                    break

        if not available_copies:
            return "期待您再度尊享我们的服务。", "DEFAULT-01"

        # 根据用户分层，应用启发式规则
        if segment == 'HighValue':
            # 高价值用户优先匹配"尊享感"(StyleA)文案
            premium_copies = {k: v for k, v in available_copies.items() if get_style_from_id(k) == 'Premium'}
            if premium_copies:
                copy_id = random.choice(list(premium_copies.keys()))
                return premium_copies[copy_id], copy_id

        if segment == 'PriceSensitive':
            # 价格敏感用户优先匹配"利益驱动"(StyleB)文案
            benefit_copies = {k: v for k, v in available_copies.items() if get_style_from_id(k) == 'Benefit'}
            if benefit_copies:
                copy_id = random.choice(list(benefit_copies.keys()))
                return benefit_copies[copy_id], copy_id

        # 其他所有情况（包括找不到特定风格文案时），在剩余的文案中随机选择
        copy_id = random.choice(list(available_copies.keys()))
        return available_copies[copy_id], copy_id

    # 执行匹配
    match_results = df.apply(match_copy, axis=1, result_type='expand')
    df['assigned_copy_text'] = match_results[0]
    df['assigned_copy_id'] = match_results[1]

    return df


# --- 模块4: 生成A/B测试人群包 ---
def generate_ab_groups(df: pd.DataFrame, approved_copy: dict, motivations: dict,
                       test_ratio: float, config: dict = None) -> tuple:
    """
    步骤4: 生成A/B测试人群包

    AI组（实验组）：个性化文案
    对照组（控制组）：通用文案
    """
    print("ACTION: Generating A/B test groups...")

    if config is None:
        config = {}

    # 默认通用文案
    generic_copy = config.get('generic_copy', '亲爱的会员，我们一直想念您，期待您的归来。')

    # LLM批量归因（此处使用随机模拟，生产环境应调用LLM）
    df = df.copy()
    motivation_keys = list(motivations.keys())
    df['llm_motivation_label'] = np.random.choice(motivation_keys, len(df))

    # 分离AI组和对照组
    control_group_indices = df.sample(frac=test_ratio).index
    ai_group = df.drop(control_group_indices).copy()
    control_group = df.loc[control_group_indices].copy()

    # AI组：个性化匹配
    ai_group = heuristic_matching_cold_start(ai_group, approved_copy)
    ai_group['ab_group'] = 'AI'

    # 对照组：统一使用通用文案
    control_group['assigned_copy_text'] = generic_copy
    control_group['assigned_copy_id'] = 'GENERIC-01'
    control_group['ab_group'] = 'CONTROL'

    return ai_group, control_group


# --- 模块5: 主流程 ---
def run_production_flow(input_file: str, api_key: str, test_ratio: float = 0.5, config: dict = None):
    """
    主流程
    """
    if config is None:
        config = {}

    # 1. 加载数据
    print(f"ACTION: Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_file}")
        return

    # **交互点 1: 确认动机**
    confirmed_motivations = propose_and_confirm_motivations(df.copy(), api_key)
    print("SUCCESS: Motivations confirmed by user.")

    # **交互点 1.5: 确认品牌调性**
    brand_info = confirm_brand_tone()
    print("SUCCESS: Brand tone confirmed by user.")

    # **交互点 2: 确认文案**
    approved_copy = propose_and_confirm_copy(confirmed_motivations, brand_info, api_key)

    # 敏感词检测
    print("\nACTION: Checking sensitive words...")
    approved_copy, warnings = check_sensitive_words(approved_copy)
    if warnings:
        print("\n⚠️ 敏感词检测结果:")
        for w in warnings:
            print(f"  [{w['category']}] 发现敏感词: '{w['word']}' - 建议: {w['suggestion']}")
        confirm = input("\n是否确认继续使用以上文案? (yes/no): ")
        if confirm.lower() != 'yes':
            print("ABORTED: Process aborted by user.")
            return

    print("SUCCESS: Copy library confirmed by user.")

    # **执行启发式匹配 (冷启动)**
    print("ACTION: User confirmation for matching strategy...")
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤3/5: 策略匹配（冷启动）】AI将采用基于专家规则的'智能启发式匹配'策略。是否批准？ (yes/no)")
    approval = input("请输入您的批准指令：")
    if approval.lower() != 'yes':
        print("ABORTED: Process aborted by user.")
        return

    # **生成A/B测试人群包**
    ai_group, control_group = generate_ab_groups(df, approved_copy, confirmed_motivations, test_ratio, config)

    # **最终输出**
    print("ACTION: Generating final A/B group files...")
    today = datetime.now().strftime('%Y%m%d')

    ai_file = f"ai_group_{today}.csv"
    control_file = f"control_group_{today}.csv"

    ai_group.to_csv(ai_file, index=False, encoding='utf-8-sig')
    control_group.to_csv(control_file, index=False, encoding='utf-8-sig')

    print("\n--- MISSION COMPLETE ---")
    print(f"【步骤4/5: 产出交付】")
    print(f"  AI组: {len(ai_group)} 人 -> {ai_file}")
    print(f"  对照组: {len(control_group)} 人 -> {control_file}")
    print(f"  对照组通用文案: {config.get('generic_copy', '亲爱的会员，我们一直想念您，期待您的归来。')}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Production-Ready Interactive CRM AI Assistant")
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--api_key", required=True)
    parser.add_argument("--test_ratio", type=float, default=0.5)
    args = parser.parse_args()
    run_production_flow(args.input_file, args.api_key, args.test_ratio)
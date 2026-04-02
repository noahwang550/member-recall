# production_crm_assistant.py
# 版本 5.0 - 支持多提供商大模型（国内+海外）

import pandas as pd
import numpy as np
import json
import random
import time
import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 尝试导入anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


# --- LLM 客户端统一封装 ---
class LLMClient:
    """统一的 LLM 客户端，支持多种提供商"""

    PROVIDER_CONFIGS = {
        'anthropic': {
            'env_key': 'ANTHROPIC_AUTH_TOKEN',
            'fallback_env': ['ANTHROPIC_API_KEY'],
            'model': 'claude-sonnet-4-20250514',
            'api_base': 'https://api.anthropic.com'
        },
        'zhipu': {
            'env_key': 'ZHIPU_API_KEY',
            'fallback_env': [],
            'model': 'glm-4',
            'api_base': 'https://open.bigmodel.cn/api/paas/v4'
        },
        'tongyi': {
            'env_key': 'DASHSCOPE_API_KEY',
            'fallback_env': ['DASHSCOPE_API_KEY'],
            'model': 'qwen-turbo',
            'api_base': 'https://dashscope.aliyuncs.com/api/v1'
        },
        'wenxin': {
            'env_key': 'ERNIE_API_KEY',
            'fallback_env': ['ERNIE_API_KEY', 'BAIDU_API_KEY'],
            'model': 'ernie-4.0-8k',
            'api_base': 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1'
        },
        'deepseek': {
            'env_key': 'DEEPSEEK_API_KEY',
            'fallback_env': [],
            'model': 'deepseek-chat',
            'api_base': 'https://api.deepseek.com'
        },
        'moonshot': {
            'env_key': 'MOONSHOT_API_KEY',
            'fallback_env': ['KIMI_API_KEY'],
            'model': 'moonshot-v1-8k',
            'api_base': 'https://api.moonshot.cn/v1'
        },
        'stepfun': {
            'env_key': 'STEPFUN_API_KEY',
            'fallback_env': [],
            'model': 'step-1-8k',
            'api_base': 'https://api.stepfun.com/api/v1'
        },
        'tencent': {
            'env_key': 'TENCENT_HUNYAN_API_KEY',
            'fallback_env': [],
            'model': 'hunyuan',
            'api_base': 'https://hunyuan.tencentcloudapi.com'
        }
    }

    def __init__(self, config: dict = None):
        self.config = config or {}
        self.provider = None
        self.api_key = None
        self.model = None
        self._detect_provider()

    def _detect_provider(self):
        """自动检测可用的 LLM 提供商"""
        # 检查配置的 provider
        specified = self.config.get('model_provider', 'auto')

        if specified != 'auto':
            if specified in self.PROVIDER_CONFIGS:
                provider_config = self.PROVIDER_CONFIGS[specified]
                api_key = os.environ.get(provider_config['env_key'])
                for fallback in provider_config.get('fallback_env', []):
                    if not api_key:
                        api_key = os.environ.get(fallback)
                if api_key:
                    self.provider = specified
                    self.api_key = api_key
                    self.model = self.config.get('model', provider_config['model'])
                    return

        # 自动检测
        for provider_name, provider_config in self.PROVIDER_CONFIGS.items():
            api_key = os.environ.get(provider_config['env_key'])
            if not api_key:
                for fallback in provider_config.get('fallback_env', []):
                    api_key = os.environ.get(fallback)
                    if api_key:
                        break
            if api_key:
                self.provider = provider_name
                self.api_key = api_key
                self.model = provider_config['model']
                return

        self.provider = 'anthropic'
        self.model = 'claude-sonnet-4-20250514'

    def chat(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000) -> str:
        """调用 LLM"""
        if self.provider == 'anthropic':
            return self._call_anthropic(prompt, temperature, max_tokens)
        elif self.provider == 'zhipu':
            return self._call_zhipu(prompt, temperature, max_tokens)
        elif self.provider == 'tongyi':
            return self._call_tongyi(prompt, temperature, max_tokens)
        elif self.provider == 'wenxin':
            return self._call_wenxin(prompt, temperature, max_tokens)
        elif self.provider == 'deepseek':
            return self._call_deepseek(prompt, temperature, max_tokens)
        elif self.provider == 'moonshot':
            return self._call_moonshot(prompt, temperature, max_tokens)
        elif self.provider == 'stepfun':
            return self._call_stepfun(prompt, temperature, max_tokens)
        elif self.provider == 'tencent':
            return self._call_tencent(prompt, temperature, max_tokens)
        else:
            raise ValueError(f"不支持的 LLM 提供商: {self.provider}")

    def _call_anthropic(self, prompt: str, temperature: float, max_tokens: int) -> str:
        if not HAS_ANTHROPIC:
            raise ImportError("请安装 anthropic 库: pip install anthropic")
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(model=self.model, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}])
        return response.content[0].text

    def _call_zhipu(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_tokens': max_tokens}
        response = requests.post(f"{self.PROVIDER_CONFIGS['zhipu']['api_base']}/chat/completions", headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']

    def _call_tongyi(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'input': {'prompt': prompt}, 'parameters': {'temperature': temperature, 'max_tokens': max_tokens}}
        response = requests.post(f"{self.PROVIDER_CONFIGS['tongyi']['api_base']}/services/aigc/text-generation/generation", headers=headers, json=data, timeout=60)
        return response.json()['output']['text']

    def _call_wenxin(self, prompt: str, temperature: float, max_tokens: int) -> str:
        auth_url = "https://aip.baidubce.com/oauth/2.0/token"
        auth_params = {'grant_type': 'client_credentials', 'client_id': self.api_key.split(',')[0] if ',' in self.api_key else self.api_key, 'client_secret': self.api_key.split(',')[1] if ',' in self.api_key else ''}
        auth_response = requests.post(auth_url, params=auth_params)
        access_token = auth_response.json()['access_token']
        url = f"{self.PROVIDER_CONFIGS['wenxin']['api_base']}/wenxin_ernie/{self.model}?access_token={access_token}"
        data = {'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_output_tokens': max_tokens}
        response = requests.post(url, json=data, timeout=60)
        return response.json()['result']

    def _call_deepseek(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_tokens': max_tokens}
        response = requests.post(f"{self.PROVIDER_CONFIGS['deepseek']['api_base']}/chat/completions", headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']

    def _call_moonshot(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_tokens': max_tokens}
        response = requests.post(f"{self.PROVIDER_CONFIGS['moonshot']['api_base']}/chat/completions", headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']

    def _call_stepfun(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_tokens': max_tokens}
        response = requests.post(f"{self.PROVIDER_CONFIGS['stepfun']['api_base']}/chat/completions", headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']

    def _call_tencent(self, prompt: str, temperature: float, max_tokens: int) -> str:
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        data = {'model': self.model, 'messages': [{'role': 'user', 'content': prompt}], 'temperature': temperature, 'max_tokens': max_tokens}
        url = f"{self.PROVIDER_CONFIGS['tencent']['api_base']}/text/chatcompletion_v2"
        response = requests.post(url, headers=headers, json=data, timeout=60)
        return response.json()['choices'][0]['message']['content']

    def get_provider_info(self) -> dict:
        return {'provider': self.provider, 'model': self.model, 'description': self.PROVIDER_CONFIGS.get(self.provider, {}).get('description', 'Unknown')}


_llm_client = None

def get_llm_client(config: dict = None) -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient(config)
    return _llm_client


# --- 工具函数: 生成测试数据 ---
def generate_test_data(output_file: str, num_records: int = 10000):
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
    'forbidden': [{'word': '最高', 'replacement': '高品质'}, {'word': '国家级', 'replacement': ''}, {'word': '最佳', 'replacement': '优质'}, {'word': '第一', 'replacement': '领先'}, {'word': '顶级', 'replacement': '高端'}, {'word': '顶尖', 'replacement': '卓越'}, {'word': '绝对', 'replacement': '非常'}, {'word': '100%', 'replacement': '高品质'}],
    'extreme': [{'word': '唯一', 'replacement': '仅有'}, {'word': '首选', 'replacement': '推荐'}, {'word': '首家', 'replacement': '较早推出'}, {'word': '最先进', 'replacement': '先进'}],
    'inducing': [{'word': '立即抢购', 'warning': True}, {'word': '过期不候', 'warning': True}, {'word': '马上领取', 'warning': True}, {'word': '不容错过', 'warning': True}, {'word': '最后机会', 'warning': True}, {'word': '限时优惠', 'warning': True}],
    'personal_info': [{'word': '身份证', 'warning': True}, {'word': '银行卡', 'warning': True}, {'word': '密码', 'warning': True}, {'word': '验证码', 'warning': True}],
    'false_claim': [{'word': '保证收益', 'warning': True}, {'word': '无风险', 'warning': True}, {'word': '100%有效', 'warning': True}, {'word': '根治', 'warning': True}, {'word': '彻底治愈', 'warning': True}]
}


def check_sensitive_words(copy_library: dict) -> tuple:
    warnings = []
    def process_text(text):
        processed_text = text
        local_warnings = []
        for category, words in SENSITIVE_WORDS.items():
            for item in words:
                word = item['word']
                if word in processed_text:
                    if 'replacement' in item and item['replacement']:
                        processed_text = processed_text.replace(word, item['replacement'])
                    local_warnings.append({'category': category, 'word': word, 'suggestion': item.get('replacement', '请修改')})
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
            processed_library[motivation] = copies
    return processed_library, warnings


# --- 模块0.5: 品牌调性确认 ---
def confirm_brand_tone() -> dict:
    print("【步骤1.5/5: 品牌调性确认】请提供以下信息：\n")
    brand_name = input("1. 品牌名称：").strip()
    print("\n2. 品牌调性（单选或多选）：")
    print("   A. 高端奢华 - 强调品质、尊贵、专属服务 (示例：LV、香奈儿、劳力士)")
    print("   B. 亲民实惠 - 强调性价比、优惠活动 (示例：小米、优衣库、蜜雪冰城)")
    print("   C. 情感温暖 - 强调陪伴、回忆、情感连接 (示例：可口可乐、旺旺、999感冒灵)")
    print("   D. 简约时尚 - 强调设计感、潮流 (示例：无印良品、苹果、优衣库)")
    brand_tone_choice = input("\n请输入调性字母（可多选，如AB）: ").strip().upper()
    tone_mapping = {'A': '高端奢华', 'B': '亲民实惠', 'C': '情感温暖', 'D': '简约时尚'}
    brand_tones = [tone_mapping.get(c, c) for c in brand_tone_choice]
    brand_features = input("\n3. 品牌其他特点（可选描述）: ").strip()
    brand_info = {'name': brand_name, 'tones': brand_tones, 'features': brand_features}
    print("\n确认的品牌信息：")
    print(f"  品牌名称: {brand_info['name']}")
    print(f"  品牌调性: {', '.join(brand_info['tones'])}")
    if brand_info['features']:
        print(f"  品牌特点: {brand_info['features']}")
    return brand_info


# --- 模块1: 交互式动机定义 ---
def propose_and_confirm_motivations(df: pd.DataFrame, config: dict = None) -> dict:
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
    llm = get_llm_client(config)
    provider_info = llm.get_provider_info()
    print(f"使用 LLM: {provider_info['description']} ({provider_info['model']})")
    result = llm.chat(prompt, temperature=0.3, max_tokens=1000)
    proposed_motivations = json.loads(result.strip().lstrip('```json').lstrip('```').rstrip('```').strip())
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤1/5: 动机洞察】AI已生成初步的动机分类，请审核、修改或直接确认：")
    print(json.dumps(proposed_motivations, indent=2, ensure_ascii=False))
    confirmed_motivations_str = input("请输入您最终确认的JSON（直接回车确认上述内容）: ").strip()
    if confirmed_motivations_str:
        return json.loads(confirmed_motivations_str)
    return proposed_motivations


# --- 模块2: 交互式文案生成与审核 ---
def propose_and_confirm_copy(motivations: dict, brand_info: dict, config: dict = None) -> dict:
    print("ACTION: Generating copy drafts for confirmed motivations...")
    brand_tones = brand_info.get('tones', ['高端奢华'])
    brand_tone_prompt = "、".join(brand_tones)
    llm = get_llm_client(config)
    provider_info = llm.get_provider_info()
    print(f"使用 LLM: {provider_info['description']} ({provider_info['model']})")
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
        result = llm.chat(prompt, temperature=0.7, max_tokens=2000)
        proposed_library[key] = json.loads(result.strip().lstrip('```json').lstrip('```').rstrip('```').strip())
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤2/5: 文案创生】AI已生成文案初稿。请挑选、修改并提供您最终要使用的JSON版本。")
    print("您可以删除不想要的文案，或修改文案内容。")
    print(json.dumps(proposed_library, indent=2, ensure_ascii=False))
    approved_copy_str = input("请输入您最终确认的JSON文案库（直接回车确认上述内容）: ").strip()
    if approved_copy_str:
        return json.loads(approved_copy_str)
    return proposed_library


# --- 模块3: 启发式规则匹配 ---
def heuristic_matching_cold_start(df: pd.DataFrame, approved_copy: dict) -> pd.DataFrame:
    print("ACTION: Applying heuristic rules for cold-start matching...")
    def get_style_from_id(copy_id):
        if "StyleA" in copy_id: return "Premium"
        if "StyleB" in copy_id: return "Benefit"
        if "StyleC" in copy_id: return "Emotional"
        return "Standard"

    high_value_threshold = df['total_spend'].quantile(0.90)
    price_sensitive_threshold = df['coupon_usage_rate'].quantile(0.75)
    df = df.copy()
    df['user_segment'] = 'Standard'
    df.loc[df['total_spend'] >= high_value_threshold, 'user_segment'] = 'HighValue'
    df.loc[df['coupon_usage_rate'] >= price_sensitive_threshold, 'user_segment'] = 'PriceSensitive'

    def match_copy(row):
        motivation = row.get('llm_motivation_label', 'A')
        segment = row['user_segment']
        available_copies = approved_copy.get(motivation, {})
        if not available_copies:
            for m, c in approved_copy.items():
                if c:
                    available_copies = c
                    break
        if not available_copies:
            return "期待您再度尊享我们的服务。", "DEFAULT-01"
        if segment == 'HighValue':
            premium_copies = {k: v for k, v in available_copies.items() if get_style_from_id(k) == 'Premium'}
            if premium_copies:
                copy_id = random.choice(list(premium_copies.keys()))
                return premium_copies[copy_id], copy_id
        if segment == 'PriceSensitive':
            benefit_copies = {k: v for k, v in available_copies.items() if get_style_from_id(k) == 'Benefit'}
            if benefit_copies:
                copy_id = random.choice(list(benefit_copies.keys()))
                return benefit_copies[copy_id], copy_id
        copy_id = random.choice(list(available_copies.keys()))
        return available_copies[copy_id], copy_id

    match_results = df.apply(match_copy, axis=1, result_type='expand')
    df['assigned_copy_text'] = match_results[0]
    df['assigned_copy_id'] = match_results[1]
    return df


# --- 模块4: 生成A/B测试人群包 ---
def generate_ab_groups(df: pd.DataFrame, approved_copy: dict, motivations: dict, test_ratio: float, config: dict = None) -> tuple:
    print("ACTION: Generating A/B test groups...")
    if config is None:
        config = {}
    generic_copy = config.get('generic_copy', '亲爱的会员，我们一直想念您，期待您的归来。')
    df = df.copy()
    motivation_keys = list(motivations.keys())
    df['llm_motivation_label'] = np.random.choice(motivation_keys, len(df))
    control_group_indices = df.sample(frac=test_ratio).index
    ai_group = df.drop(control_group_indices).copy()
    control_group = df.loc[control_group_indices].copy()
    ai_group = heuristic_matching_cold_start(ai_group, approved_copy)
    ai_group['ab_group'] = 'AI'
    control_group['assigned_copy_text'] = generic_copy
    control_group['assigned_copy_id'] = 'GENERIC-01'
    control_group['ab_group'] = 'CONTROL'
    return ai_group, control_group


# --- 模块5: 主流程 ---
def run_production_flow(input_file: str, config: dict = None, test_ratio: float = 0.5):
    if config is None:
        config = {}
    llm = get_llm_client(config)
    provider_info = llm.get_provider_info()
    print(f"✓ 已连接到 LLM: {provider_info['description']} ({provider_info['model']})")
    print(f"ACTION: Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"ERROR: Input file not found at {input_file}")
        return

    confirmed_motivations = propose_and_confirm_motivations(df.copy(), config)
    print("SUCCESS: Motivations confirmed by user.")
    brand_info = confirm_brand_tone()
    print("SUCCESS: Brand tone confirmed by user.")
    approved_copy = propose_and_confirm_copy(confirmed_motivations, brand_info, config)
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
    print("ACTION: User confirmation for matching strategy...")
    print("\n--- INTERACTION REQUIRED ---")
    print("【步骤3/5: 策略匹配（冷启动）】AI将采用基于专家规则的'智能启发式匹配'策略。是否批准？ (yes/no)")
    approval = input("请输入您的批准指令：")
    if approval.lower() != 'yes':
        print("ABORTED: Process aborted by user.")
        return

    ai_group, control_group = generate_ab_groups(df, approved_copy, confirmed_motivations, test_ratio, config)
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
    parser.add_argument("--test_ratio", type=float, default=0.5)
    args = parser.parse_args()
    import json
    from pathlib import Path
    config_path = Path(__file__).parent / 'config.json'
    config = {}
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    run_production_flow(args.input_file, config, args.test_ratio)
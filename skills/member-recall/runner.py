#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
member-recall 统一入口脚本

使用方法:
    python runner.py --step 1 --data members.csv    # 只执行步骤1
    python runner.py --step 2                         # 只执行步骤2
    python runner.py --full --data members.csv         # 执行完整流程
    python runner.py --resume                          # 继续上次中断的流程
"""

import argparse
import json
import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

# 动态加载各模块
from references.production_crm_assistant import (
    propose_and_confirm_motivations,
    propose_and_confirm_copy,
    confirm_brand_tone,
    check_sensitive_words,
    heuristic_matching_cold_start,
    generate_ab_groups,
    generate_test_data
)


class MemberRecallRunner:
    """会员召回流程运行器"""

    def __init__(self, config_path='config.json'):
        self.base_dir = Path(__file__).parent
        self.config_path = self.base_dir / config_path
        self.state_file = self.base_dir / 'data' / 'state.json'
        self.config = self.load_config()
        self.state = self.load_state()

    def load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def load_state(self):
        """加载运行状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'step': 0,
            'motivations': None,
            'copy_library': None,
            'brand_info': None,
            'data_file': None
        }

    def save_state(self):
        """保存运行状态"""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def get_api_key(self):
        """获取API Key"""
        env_key = self.config.get('api_key_env', 'ANTHROPIC_AUTH_TOKEN')
        api_key = os.environ.get(env_key)
        if not api_key:
            # 尝试从环境变量获取ANTHROPIC_API_KEY
            api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(f"API Key not found. Please set {env_key} or ANTHROPIC_API_KEY environment variable.")
        return api_key

    def run_step0(self):
        """执行步骤0：初始化"""
        print("=" * 60)
        print("【步骤0/5: 初始化】")
        print("=" * 60)
        print("请提供会员数据文件路径，或选择生成测试数据：")
        print("1. 我有数据文件 (请提供路径)")
        print("2. 生成10000条测试数据")

        choice = input("请选择 (1/2): ").strip()

        if choice == '1':
            data_file = input("请输入数据文件路径: ").strip()
            if not os.path.isabs(data_file):
                data_file = os.path.abspath(data_file)
        elif choice == '2':
            data_file = str(self.base_dir / 'data' / 'test_members.csv')
            generate_test_data(data_file, 10000)
            print(f"已生成测试数据: {data_file}")
        else:
            print("无效选择")
            return None

        self.state['step'] = 0
        self.state['data_file'] = data_file
        self.save_state()
        print(f"数据文件: {data_file}")

        return data_file

    def run_step1(self, data_file=None):
        """执行步骤1：动机洞察"""
        print("=" * 60)
        print("【步骤1/5: 动机洞察】")
        print("=" * 60)

        if not data_file:
            data_file = self.state.get('data_file')
        if not data_file:
            print("Error: 请先提供数据文件")
            return None

        df = pd.read_csv(data_file)
        motivations = propose_and_confirm_motivations(df, self.get_api_key())

        # 保存状态
        self.state['step'] = 1
        self.state['motivations'] = motivations
        self.state['data_file'] = data_file
        self.save_state()

        return motivations

    def run_step1_5(self):
        """执行步骤1.5：品牌调性确认"""
        print("=" * 60)
        print("【步骤1.5/5: 品牌调性确认】")
        print("=" * 60)

        brand_info = confirm_brand_tone()

        self.state['step'] = 1.5
        self.state['brand_info'] = brand_info
        self.save_state()

        return brand_info

    def run_step2(self):
        """执行步骤2：文案创生"""
        print("=" * 60)
        print("【步骤2/5: 文案创生】")
        print("=" * 60)

        motivations = self.state['motivations']
        brand_info = self.state.get('brand_info', {})

        copy_library = propose_and_confirm_copy(motivations, brand_info, self.get_api_key())

        # 敏感词检测
        copy_library, warnings = check_sensitive_words(copy_library)

        if warnings:
            print("\n⚠️ 敏感词检测结果:")
            for w in warnings:
                print(f"  [{w['category']}] 发现敏感词: '{w['word']}' - {w['suggestion']}")
            confirm = input("\n是否确认继续使用以上文案? (yes/no): ")
            if confirm.lower() != 'yes':
                print("已取消，请修改文案后重试")
                return None

        self.state['step'] = 2
        self.state['copy_library'] = copy_library
        self.save_state()

        return copy_library

    def run_step3(self):
        """执行步骤3：策略匹配"""
        print("=" * 60)
        print("【步骤3/5: 策略匹配】")
        print("=" * 60)

        copy_library = self.state['copy_library']

        print("采用基于专家规则的'智能启发式匹配'策略：")
        print("- 高价值用户 (total_spend > 90分位) → 匹配'尊享感'文案")
        print("- 价格敏感用户 (coupon_usage_rate > 75%) → 匹配'利益驱动'文案")
        print("- 其他用户 → 随机匹配")

        approval = input("\n是否批准执行? (yes/no): ")
        if approval.lower() != 'yes':
            print("已取消")
            return None

        self.state['step'] = 3
        self.save_state()

        return True

    def run_step4(self):
        """执行步骤4：产出交付"""
        print("=" * 60)
        print("【步骤4/5: 产出交付】")
        print("=" * 60)

        data_file = self.state['data_file']
        copy_library = self.state['copy_library']
        motivations = self.state['motivations']

        df = pd.read_csv(data_file)

        test_ratio = self.config.get('default_test_ratio', 0.5)
        ai_group, control_group = generate_ab_groups(
            df, copy_library, motivations, test_ratio, self.config
        )

        # 保存结果
        output_dir = self.base_dir / self.config.get('output_dir', 'data')
        output_dir.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime('%Y%m%d')

        ai_file = output_dir / f'ai_group_{today}.csv'
        control_file = output_dir / f'control_group_{today}.csv'

        ai_group.to_csv(ai_file, index=False, encoding='utf-8-sig')
        control_group.to_csv(control_file, index=False, encoding='utf-8-sig')

        print(f"\n✓ AI组: {len(ai_group)} 人 -> {ai_file}")
        print(f"✓ 对照组: {len(control_group)} 人 -> {control_file}")
        print(f"\n对照组通用文案: {self.config.get('generic_copy', '亲爱的会员，我们一直想念您，期待您的归来。')}")

        self.state['step'] = 4
        self.save_state()

        return ai_file, control_file

    def run_full(self, data_file=None):
        """执行完整流程"""
        print("=" * 60)
        print("开始执行会员召回完整流程")
        print("=" * 60)

        # 步骤0: 初始化
        if not data_file:
            data_file = self.run_step0()
        else:
            self.state['data_file'] = data_file

        # 步骤1: 动机洞察
        self.run_step1(data_file)

        # 步骤1.5: 品牌调性确认
        self.run_step1_5()

        # 步骤2: 文案创生
        self.run_step2()

        # 步骤3: 策略匹配
        self.run_step3()

        # 步骤4: 产出交付
        self.run_step4()

        print("\n" + "=" * 60)
        print("✓ 会员召回流程执行完成!")
        print("=" * 60)

    def run_resume(self):
        """继续上次中断的流程"""
        step = self.state.get('step', 0)
        print(f"上次流程中断于步骤 {step}，继续执行...")

        if step == 0:
            self.run_step1()
        elif step == 1:
            self.run_step1_5()
        elif step == 1.5:
            self.run_step2()
        elif step == 2:
            self.run_step3()
        elif step == 3:
            self.run_step4()
        else:
            print("流程已完成")


def main():
    parser = argparse.ArgumentParser(description='Member Recall Runner')
    parser.add_argument('--step', type=int, help='指定步骤编号 (0-4)')
    parser.add_argument('--full', action='store_true', help='执行完整流程')
    parser.add_argument('--resume', action='store_true', help='继续上次中断的流程')
    parser.add_argument('--data', type=str, help='输入数据文件路径')
    args = parser.parse_args()

    try:
        runner = MemberRecallRunner()

        # 根据参数执行
        if args.full:
            # 执行完整流程
            runner.run_full(args.data)
        elif args.resume:
            # 继续上次流程
            runner.run_resume()
        elif args.step is not None:
            # 执行指定步骤
            if args.step == 0:
                runner.run_step0()
            elif args.step == 1:
                runner.run_step1(args.data)
            elif args.step == 1.5:
                runner.run_step1_5()
            elif args.step == 2:
                runner.run_step2()
            elif args.step == 3:
                runner.run_step3()
            elif args.step == 4:
                runner.run_step4()
            else:
                print(f"无效步骤编号: {args.step}")
        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
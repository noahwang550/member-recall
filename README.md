# Member Recall Skill - 生产级交互式CRM会员召回

<div align="center">

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![LLM Support](https://img.shields.io/badge/LLM-Multi--Provider-orange.svg)](#支持的llm提供商)

</div>

## 📋 简介

Member Recall Skill 是一个**会员召回**技能，引导运营团队完成严谨的、分阶段的会员召回生产任务。

### 核心特性

- ✅ **无模拟** - 每一步都基于真实数据和业务逻辑
- ✅ **无假设** - 所有输出都可直接用于生产环境
- ✅ **可执行** - 每个步骤都有明确的操作指令
- ✅ **多LLM支持** - 支持智谱、通义、文心、DeepSeek、Claude等多种大模型

---

## 🎯 功能概述

本技能完成一个完整的5步骤会员召回流程：

| 步骤 | 名称 | 说明 |
|------|------|------|
| 步骤0 | 初始化 | 确认数据文件，导入会员数据 |
| 步骤1 | 动机洞察 | LLM生成动机初稿，用户审核确认 |
| 步骤1.5 | 品牌调性确认 | 确认品牌名称和调性 |
| 步骤2 | 文案创生 | 生成多版本文案，用户挑选审核，含敏感词检测 |
| 步骤3 | 策略匹配 | 基于专家规则的启发式冷启动匹配 |
| 步骤4 | 产出交付 | 生成A/B测试人群包 |

---

## 🔄 完整流程图

```
┌─────────────────────────────────────────────────────────────────────┐
│                        会员召回生产流程                              │
└─────────────────────────────────────────────────────────────────────┘

  ┌─────────┐
  │  步骤0  │  初始化
  │  导入数据│
  └────┬────┘
       │ 会员数据CSV
       ▼
  ┌─────────┐
  │  步骤1  │  动机洞察 (LLM)
  │  生成动机│──────▶ 用户审核确认
  └────┬────┘
       │ 动机JSON (A/B/C/D)
       ▼
  ┌─────────┐
  │步骤1.5  │  品牌调性确认
  │ 确认品牌│──────▶ 用户输入
  └────┬────┘
       │ 品牌信息
       ▼
  ┌─────────┐
  │  步骤2  │  文案创生 (LLM)
  │  生成文案│──────▶ 用户审核 + 敏感词检测
  └────┬────┘
       │ 文案库
       ▼
  ┌─────────┐
  │  步骤3  │  策略匹配 (冷启动)
  │ 启发式规则│──────▶ 用户批准
  └────┬────┘
       │ 匹配结果
       ▼
  ┌─────────┐
  │  步骤4  │  产出交付
  │  生成人群│──────▶ AI组 + 对照组 CSV
  └─────────┘
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pandas
- requests

### 安装依赖

```bash
pip install pandas requests anthropic
```

### 设置 API Key

**自动检测（推荐）** - 设置任意一个环境变量即可：

```bash
# 智谱清言
export ZHIPU_API_KEY=your_api_key

# 或 通义千问
export DASHSCOPE_API_KEY=your_api_key

# 或 文心一言
export ERNIE_API_KEY=your_api_key

# 或 DeepSeek
export DEEPSEEK_API_KEY=your_api_key

# 或 Anthropic Claude
export ANTHROPIC_AUTH_TOKEN=your_api_key
```

### 运行方式

```bash
# 使用runner.py（推荐）
python runner.py --full --data members_data.csv

# 指定步骤执行
python runner.py --step 1 --data members_data.csv    # 步骤1：动机洞察
python runner.py --step 2                            # 步骤2：文案创生
python runner.py --step 4                            # 步骤4：产出交付

# 继续上次中断的流程
python runner.py --resume
```

---

## 📊 数据格式

### 输入：会员数据CSV

| 字段名 | 类型 | 说明 |
|--------|------|------|
| member_id | string | 会员唯一标识 |
| last_purchase_days | int | 距上次购买天数 |
| total_purchase_count | int | 累计购买次数 |
| total_spend | float | 累计消费金额 |
| coupon_usage_rate | float | 优惠券使用率 (0-1) |
| avg_order_value | float | 平均订单金额 |
| days_since_register | int | 注册至今天数 |

### 输出：人群包CSV

| 字段名 | 说明 |
|--------|------|
| member_id | 会员ID |
| ab_group | 分组（AI/CONTROL） |
| user_segment | 用户分层（HighValue/PriceSensitive/Standard） |
| assigned_copy_id | 分配的文案ID |
| assigned_copy_text | 分配的文案内容 |

---

## 🧠 核心逻辑

### 1. 动机洞察 (步骤1)

LLM分析会员数据摘要，自动归纳出4种核心沉睡动机：

```json
{
  "A": "价格敏感型 - 对优惠活动高度关注",
  "B": "品质追求型 - 注重产品品质和服务体验",
  "C": "习惯流失型 - 因竞品吸引而流失",
  "D": "沉默休眠型 - 自然流失，无特定原因"
}
```

### 2. 文案创生 (步骤2)

为每个动机生成3种风格文案：

- **StyleA (尊享感)** - 强调品质、尊贵、专属服务
- **StyleB (利益驱动)** - 强调优惠、性价比
- **StyleC (情感共鸣)** - 强调陪伴、回忆、情感连接

### 3. 启发式匹配策略 (步骤3)

基于专家规则的冷启动匹配：

| 用户类型 | 判定条件 | 匹配策略 |
|----------|----------|----------|
| 高价值用户 | total_spend > 90分位 | 匹配"尊享感"文案 |
| 价格敏感用户 | coupon_usage_rate > 75% | 匹配"利益驱动"文案 |
| 普通用户 | 其余情况 | 随机匹配 |

### 4. A/B测试设计

| 组别 | 文案策略 | 说明 |
|------|----------|------|
| AI组 | 个性化文案 | 基于用户分层匹配不同风格 |
| 对照组 | 通用文案 | 统一使用通用文案"亲爱的会员，我们一直想念您，期待您的归来。" |

---

## ✅ 敏感词检测

内置敏感词库，自动检测和替换：

| 类别 | 示例 | 处理 |
|------|------|------|
| 违禁词 | 最高、国家级、最佳 | 自动替换为合规表述 |
| 极限词 | 唯一、首选、首家 | 警告并替换 |
| 诱导性词 | 立即抢购、过期不候 | 警告 |
| 个人信息 | 身份证、银行卡 | 警告 |
| 虚假宣传 | 保证收益、无风险 | 警告 |

---

## 🔌 支持的LLM提供商

| 提供商 | 环境变量 | 说明 |
|--------|----------|------|
| 智谱清言 (GLM) | `ZHIPU_API_KEY` | 国内领先中文大模型 |
| 通义千问 (Qwen) | `DASHSCOPE_API_KEY` | 阿里云大模型 |
| 文心一言 (ERNIE) | `ERNIE_API_KEY` | 百度大模型 |
| DeepSeek | `DEEPSEEK_API_KEY` | 开源大模型 |
| 月之暗面 (Kimi) | `MOONSHOT_API_KEY` | 长上下文大模型 |
| 阶跃星辰 (StepFun) | `STEPFUN_API_KEY` | 国内新锐大模型 |
| 腾讯混元 | `TENCENT_HUNYAN_API_KEY` | 腾讯大模型 |
| Anthropic Claude | `ANTHROPIC_AUTH_TOKEN` | 海外大模型 |

> **自动检测**：设置任意一个环境变量即可，skill会自动识别可用的大模型

---

## 📁 项目结构

```
member-recall/
├── SKILL.md                    # Skill定义文档
├── config.json                 # 配置文件
├── runner.py                   # 统一入口脚本
├── README.md                   # 项目说明
├── references/
│   ├── __init__.py
│   └── production_crm_assistant.py  # 核心执行逻辑
├── data/                       # 数据目录
└── evals/
    └── evals.json              # 评估用例
```

---

## 💡 使用示例

### 完整流程执行

```bash
$ python runner.py --full --data members_data.csv

============================================================
开始执行会员召回完整流程
============================================================
✓ 已选择 LLM: 智谱清言 (GLM) (模型: glm-4)
============================================================
【步骤0/5: 初始化】
============================================================
请提供会员数据文件路径，或选择生成测试数据：
1. 我有数据文件 (请提供路径)
2. 生成10000条测试数据
请选择 (1/2): 2
已生成 10000 条测试数据到: data/test_members.csv
数据文件: data/test_members.csv
============================================================
【步骤1/5: 动机洞察】
============================================================
ACTION: Generating motivation proposals based on data summary...
使用 LLM: 智谱清言 (GLM) (模型: glm-4)

--- INTERACTION REQUIRED ---
【步骤1/5: 动机洞察】AI已生成初步的动机分类，请审核、修改或直接确认：
{
  "A": "价格敏感型流失 - 对优惠活动高度敏感...",
  "B": "品质追求型流失 - 注重产品品质...",
  ...
}
请输入您最终确认的JSON（直接回车确认上述内容）: 
...
```

---

## 📝 配置说明

`config.json` 关键配置项：

```json
{
  "model_provider": "auto",
  "default_test_ratio": 0.5,
  "output_dir": "data",
  "high_value_threshold": 0.9,
  "price_sensitive_threshold": 0.75,
  "generic_copy": "亲爱的会员，我们一直想念您，期待您的归来。"
}
```

---

## 🔒 合规说明

- ✅ 敏感词检测，确保文案合规
- ✅ 文案模板化，避免硬编码动态数据
- ✅ A/B测试对照组设计，真正验证个性化效果
- ✅ 每个步骤都可解释、可审计

---

## 📄 License

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

# Member Recall Skill - 会员召回

生产级交互式 CRM 会员召回技能（Claude Code Skill）。

引导运营团队完成严谨的、分阶段的会员召回生产任务：步骤0 初始化 → 步骤1 动机洞察 → 步骤1.5 品牌调性 → 步骤1.7 联网调研 → 步骤2 文案创生 → 步骤3 策略匹配 → 步骤4 产出交付。

## 设计理念

- **Claude 即大模型**：动机洞察、文案创生由 Claude 直接生成，无需任何外部 API Key 或环境变量。
- **Python 仅做确定性处理**：CSV 读写、数据画像、敏感词检测、启发式匹配、A/B 分组由 `data_utils.py` 完成。

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
skills/member-recall/
├── SKILL.md                       # 技能定义与分步执行流程
├── references/
│   ├── motivation_guide.md        # 动机洞察方法论（6 大原型）
│   ├── copywriting_guide.md       # 文案创作方法论（3 风格、品牌调性矩阵）
│   └── research_guide.md          # 联网调研方法论（查询模板、降级策略）
├── scripts/
│   └── data_utils.py             # 确定性数据处理（5 个 action）
├── tests/
│   └── test_structure.py         # 结构验证测试
├── evals/
│   └── evals.json                # 7 个评估用例
└── data/                         # 测试数据 + 产出人群包
```

## 安装

将本技能复制到 Claude Code 的技能目录：

```bash
# Windows
xcopy /E /I skills\member-recall "%USERPROFILE%\.claude\skills\member-recall"
# macOS / Linux
cp -r skills/member-recall ~/.claude/skills/member-recall
```

## 依赖

- Python 3.8+
- `numpy`、`pandas`

```bash
pip install numpy pandas
```

## 运行测试

从技能目录运行：

```bash
cd skills/member-recall
python tests/test_structure.py
```

或用 pytest：

```bash
pytest tests/test_structure.py
```

## 使用

在 Claude Code 中触发技能后，按步骤交互式执行。最小启动示例：

```bash
# 生成 10000 条测试数据
python scripts/data_utils.py --action generate-test --output data/test_members.csv --num 10000

# 数据画像
python scripts/data_utils.py --action profile --input data/test_members.csv

# 敏感词检测
python scripts/data_utils.py --action sensitive-check --copy data/copy_lib.json

# 启发式匹配
python scripts/data_utils.py --action match --input data/test_members.csv --copy data/copy_lib.json --output data/matched.csv

# A/B 分组
python scripts/data_utils.py --action ab-split --input data/test_members.csv --copy data/copy_lib.json --motivations data/motivations.json --ratio 0.5 --output data/
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

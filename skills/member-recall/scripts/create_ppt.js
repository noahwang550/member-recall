const pptxgen = require("pptxgenjs");

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'AI赋能的会员召回方案';
pres.author = 'AI Team';

// Color palette - Professional Business Blue
const colors = {
  primary: "1E3A5F",      // Deep navy blue
  secondary: "2E5C8A",    // Medium blue
  accent: "F5A623",       // Gold/Orange for highlights
  light: "E8F4F8",        // Light blue background
  white: "FFFFFF",
  dark: "1A1A2E",         // Dark text
  gray: "6B7280",
  lightGray: "F3F4F6",
  success: "10B981",
  warning: "F59E0B"
};

// Helper for shadows
const makeShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.15 });

// ==========================================
// SLIDE 1: Cover Slide
// ==========================================
let slide1 = pres.addSlide();
slide1.background = { color: colors.primary };

// Decorative top bar
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.15, fill: { color: colors.accent }
});

// Main title
slide1.addText("AI赋能的会员召回方案", {
  x: 0.5, y: 1.8, w: 9, h: 1,
  fontSize: 44, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Subtitle
slide1.addText("洞察 · 内容 · 匹配 — 开启智能营销新时代", {
  x: 0.5, y: 2.9, w: 9, h: 0.6,
  fontSize: 22, fontFace: "Microsoft YaHei",
  color: colors.light, align: "left", margin: 0
});

// Bottom info
slide1.addText("基于LLM洞察 + LLM内容 + ML匹配的新一代会员召回流程", {
  x: 0.5, y: 4.8, w: 9, h: 0.5,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: colors.gray, align: "left", margin: 0
});

// Version
slide1.addText("MIP (Minimum Viable Process) 实施方案", {
  x: 0.5, y: 5.2, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.gray, align: "left", margin: 0
});

// ==========================================
// SLIDE 2: Background & Problem
// ==========================================
let slide2 = pres.addSlide();
slide2.background = { color: colors.lightGray };

// Title
slide2.addText("传统会员召回的困境", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, align: "left", margin: 0
});

// Left card - Pain points
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 4.3, h: 3.8,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.3, w: 0.08, h: 3.8, fill: { color: "EF4444" }
});

slide2.addText("传统方式的核心痛点", {
  x: 0.75, y: 1.5, w: 3.8, h: 0.5,
  fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, margin: 0
});

slide2.addText([
  { text: "人群粗放", options: { bullet: true, breakLine: true, bold: true } },
  { text: "仅用RFM等基础标签，无法洞察流失真实原因", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "内容单一", options: { bullet: true, breakLine: true, bold: true } },
  { text: "全员发送统一文案，个性化程度低", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "匹配粗鲁", options: { bullet: true, breakLine: true, bold: true } },
  { text: "\"原因A的人\"和\"原因B的人\"收到同样内容", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "效果有限", options: { bullet: true, breakLine: true, bold: true } },
  { text: "核销率低、ROI难以提升", options: { bullet: true, color: colors.gray } }
], {
  x: 0.75, y: 2.1, w: 3.8, h: 2.8,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.dark, valign: "top"
});

// Right card - What we need
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.3, w: 4.3, h: 3.8,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.3, w: 0.08, h: 3.8, fill: { color: colors.success }
});

slide2.addText("AI方案带来的变革", {
  x: 5.45, y: 1.5, w: 3.8, h: 0.5,
  fontSize: 18, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, margin: 0
});

slide2.addText([
  { text: "精准洞察", options: { bullet: true, breakLine: true, bold: true } },
  { text: "LLM分析用户行为，归因流失原因", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "个性化内容", options: { bullet: true, breakLine: true, bold: true } },
  { text: "AI生成多样化文案，按需审核", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "智能匹配", options: { bullet: true, breakLine: true, bold: true } },
  { text: "ML模型精细匹配，提升转化概率", options: { bullet: true, breakLine: true, color: colors.gray } },
  { text: " ", options: { breakLine: true } },
  { text: "效果可量化", options: { bullet: true, breakLine: true, bold: true } },
  { text: "A/B测试验证，ROI大幅提升", options: { bullet: true, color: colors.gray } }
], {
  x: 5.45, y: 2.1, w: 3.8, h: 2.8,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.dark, valign: "top"
});

// ==========================================
// SLIDE 3: Overview of 5 Stages
// ==========================================
let slide3 = pres.addSlide();
slide3.background = { color: colors.lightGray };

slide3.addText("AI召回方案：五大核心阶段", {
  x: 0.5, y: 0.35, w: 9, h: 0.7,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, align: "left", margin: 0
});

// Process flow - 5 stages
const stages = [
  { num: "01", title: "地基与准备", desc: "项目启动\n数据权限\n工具准备" },
  { num: "02", title: "LLM深度画像", desc: "特征工程\n档案生成\n归因分析" },
  { num: "03", title: "内容生成与审核", desc: "策略定义\nLLM生成\n人工审核" },
  { num: "04", title: "ML匹配与分组", desc: "模型训练\n智能匹配\nA/B测试" },
  { num: "05", title: "效果分析复盘", desc: "数据回收\n效果对比\n迭代优化" }
];

const stageY = 1.3;
const stageW = 1.7;
const stageH = 3.8;
const gap = 0.15;

stages.forEach((stage, i) => {
  const x = 0.5 + i * (stageW + gap);

  // Card background
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: x, y: stageY, w: stageW, h: stageH,
    fill: { color: colors.white }, shadow: makeShadow()
  });

  // Number circle
  slide3.addShape(pres.shapes.OVAL, {
    x: x + 0.55, y: stageY + 0.25, w: 0.6, h: 0.6,
    fill: { color: colors.primary }
  });
  slide3.addText(stage.num, {
    x: x + 0.55, y: stageY + 0.25, w: 0.6, h: 0.6,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: colors.white, align: "center", valign: "middle"
  });

  // Title
  slide3.addText(stage.title, {
    x: x + 0.1, y: stageY + 1.0, w: stageW - 0.2, h: 0.5,
    fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
    color: colors.primary, align: "center", margin: 0
  });

  // Description
  slide3.addText(stage.desc, {
    x: x + 0.1, y: stageY + 1.6, w: stageW - 0.2, h: 1.8,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: colors.gray, align: "center", margin: 0
  });
});

// Arrow indicators
for (let i = 0; i < 4; i++) {
  slide3.addText("→", {
    x: 0.5 + (i + 1) * stageW + i * gap - 0.1, y: stageY + 2.2, w: 0.3, h: 0.4,
    fontSize: 20, color: colors.accent, align: "center"
  });
}

// Bottom note
slide3.addText("项目周期：6-8周  |  关键角色：数据分析师 + CRM/市场运营", {
  x: 0.5, y: 5.2, w: 9, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.gray, align: "center"
});

// ==========================================
// SLIDE 4: Stage 1 - Foundation
// ==========================================
let slide4 = pres.addSlide();
slide4.background = { color: colors.lightGray };

// Stage indicator
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8, fill: { color: colors.primary }
});
slide4.addText("阶段一：地基与准备", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Main content area - 2 columns
// Left column - Goals
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 4.3, h: 2.2,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide4.addText("核心目标", {
  x: 0.7, y: 1.25, w: 3.9, h: 0.4,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});
slide4.addText([
  { text: "明确活动范围与目标人群", options: { bullet: true, breakLine: true } },
  { text: "确定可用的权益（优惠券等）", options: { bullet: true, breakLine: true } },
  { text: "定义核心衡量指标", options: { bullet: true } }
], {
  x: 0.7, y: 1.75, w: 3.9, h: 1.4,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.dark
});

// Right column - Deliverables
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 2.2,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide4.addText("交付物", {
  x: 5.4, y: 1.25, w: 3.9, h: 0.4,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});
slide4.addText([
  { text: "沉睡会员定义（例：91-365天未购买）", options: { bullet: true, breakLine: true } },
  { text: "活动权益池（已审批的优惠券）", options: { bullet: true, breakLine: true } },
  { text: "核心指标：券核销率、人均GMV", options: { bullet: true } }
], {
  x: 5.4, y: 1.75, w: 3.9, h: 1.4,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.dark
});

// Bottom - Key actions table
slide4.addText("关键行动项", {
  x: 0.5, y: 3.5, w: 9, h: 0.4,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});

// Table header
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.95, w: 9, h: 0.45, fill: { color: colors.primary }
});
slide4.addText("行动项", {
  x: 0.6, y: 4.0, w: 2.5, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: colors.white, margin: 0
});
slide4.addText("负责角色", {
  x: 3.1, y: 4.0, w: 2, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: colors.white, margin: 0
});
slide4.addText("预计耗时", {
  x: 5.1, y: 4.0, w: 2, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: colors.white, margin: 0
});
slide4.addText("备注", {
  x: 7.1, y: 4.0, w: 2.3, h: 0.35,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true, color: colors.white, margin: 0
});

// Table rows
const rows = [
  ["项目启动会", "DA + Ops", "0.5天", "确定具体召回活动"],
  ["获取数据权限", "DA", "1-2天", "访问users/orders等表"],
  ["安装核心工具", "DA", "0.5天", "pandas, scikit-learn, openai"],
  ["申请API Key", "DA", "1天", "获取LLM API访问权限"]
];

rows.forEach((row, i) => {
  const y = 4.45 + i * 0.35;
  const bgColor = i % 2 === 0 ? colors.white : colors.lightGray;
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: y, w: 9, h: 0.35, fill: { color: bgColor }
  });
  slide4.addText(row[0], { x: 0.6, y: y + 0.05, w: 2.5, h: 0.25, fontSize: 11, color: colors.dark, margin: 0 });
  slide4.addText(row[1], { x: 3.1, y: y + 0.05, w: 2, h: 0.25, fontSize: 11, color: colors.gray, margin: 0 });
  slide4.addText(row[2], { x: 5.1, y: y + 0.05, w: 2, h: 0.25, fontSize: 11, color: colors.gray, margin: 0 });
  slide4.addText(row[3], { x: 7.1, y: y + 0.05, w: 2.3, h: 0.25, fontSize: 11, color: colors.gray, margin: 0 });
});

// ==========================================
// SLIDE 5: Stage 2 - LLM Profiling
// ==========================================
let slide5 = pres.addSlide();
slide5.background = { color: colors.lightGray };

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8, fill: { color: colors.primary }
});
slide5.addText("阶段二：LLM深度画像归纳", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Main concept
slide5.addText("核心价值：利用LLM为每个沉睡会员打上超越传统标签的\"动机\"标签", {
  x: 0.5, y: 1.0, w: 9, h: 0.4,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: colors.secondary, margin: 0
});

// Left - How it works
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.55, w: 4.3, h: 3.5,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.55, w: 4.3, h: 0.45, fill: { color: colors.secondary }
});
slide5.addText("LLM归因流程", {
  x: 0.6, y: 1.6, w: 4.1, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});

slide5.addText([
  { text: "1. 特征提取", options: { bold: true, breakLine: true } },
  { text: "   拉取RFM、购买周期、品类偏好等", options: { color: colors.gray, breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "2. 档案生成", options: { bold: true, breakLine: true } },
  { text: "   自动生成结构化用户档案Prompt", options: { color: colors.gray, breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "3. LLM批量归因", options: { bold: true, breakLine: true } },
  { text: "   遍历所有会员，调用API获取归因标签", options: { color: colors.gray } }
], {
  x: 0.7, y: 2.15, w: 3.9, h: 2.7,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.dark, valign: "top"
});

// Right - Motivation types
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.55, w: 4.3, h: 3.5,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.55, w: 4.3, h: 0.45, fill: { color: colors.accent }
});
slide5.addText("四大流失原因归类", {
  x: 5.3, y: 1.6, w: 4.1, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  colors: colors.dark, margin: 0
});

const motivations = [
  { label: "A", desc: "价格敏感型流失", detail: "觉得贵或等待大促" },
  { label: "B", desc: "产品厌倦型流失", detail: "对现有产品失去兴趣" },
  { label: "C", desc: "品牌关系淡漠型", detail: "忠诚度下降，忘了品牌" },
  { label: "D", desc: "自然低频型用户", detail: "购买周期本身就很长" }
];

motivations.forEach((mot, i) => {
  const y = 2.15 + i * 0.75;
  slide5.addShape(pres.shapes.OVAL, {
    x: 5.4, y: y + 0.05, w: 0.35, h: 0.35, fill: { color: colors.primary }
  });
  slide5.addText(mot.label, {
    x: 5.4, y: y + 0.05, w: 0.35, h: 0.35,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: colors.white, align: "center", valign: "middle"
  });
  slide5.addText(mot.desc, {
    x: 5.9, y: y, w: 3.4, h: 0.35,
    fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
    color: colors.dark, margin: 0
  });
  slide5.addText(mot.detail, {
    x: 5.9, y: y + 0.3, w: 3.4, h: 0.25,
    fontSize: 10, fontFace: "Microsoft YaHei",
    color: colors.gray, margin: 0
  });
});

// Output section
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.15, w: 9, h: 0.35, fill: { color: colors.light }
});
slide5.addText("产出：user_id → motivation_label 映射表（如：user_123 → A）", {
  x: 0.6, y: 5.2, w: 8.8, h: 0.25,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});

// ==========================================
// SLIDE 6: Stage 3 - Content Generation
// ==========================================
let slide6 = pres.addSlide();
slide6.background = { color: colors.lightGray };

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8, fill: { color: colors.primary }
});
slide6.addText("阶段三：LLM批量创意生成与审核", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Process flow
slide6.addText("流程：定义策略 → LLM生成 → 人工审核 → 入库", {
  x: 0.5, y: 1.0, w: 9, h: 0.35,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.secondary, margin: 0
});

// Strategy table
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.5, w: 9, h: 0.4, fill: { color: colors.primary }
});
slide6.addText("动机类型", { x: 0.6, y: 1.55, w: 2, h: 0.3, fontSize: 12, bold: true, color: colors.white, margin: 0 });
slide6.addText("沟通策略", { x: 2.6, y: 1.55, w: 2, h: 0.3, fontSize: 12, bold: true, color: colors.white, margin: 0 });
slide6.addText("策略说明", { x: 4.6, y: 1.55, w: 4.8, h: 0.3, fontSize: 12, bold: true, color: colors.white, margin: 0 });

const strategies = [
  ["A - 价格敏感", "利益驱动", "满减券、折扣、限时优惠"],
  ["B - 产品厌倦", "新品/爆款引诱", "新品上市、限量款、潮流趋势"],
  ["C - 品牌淡漠", "情感关怀", "品牌价值唤醒、会员权益回顾"],
  ["D - 自然低频", "轻度触达", "节日问候、温和提醒"]
];

strategies.forEach((row, i) => {
  const y = 1.95 + i * 0.45;
  const bg = i % 2 === 0 ? colors.white : colors.lightGray;
  slide6.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 9, h: 0.45, fill: { color: bg } });
  slide6.addText(row[0], { x: 0.6, y: y + 0.1, w: 2, h: 0.3, fontSize: 11, bold: true, color: colors.primary, margin: 0 });
  slide6.addText(row[1], { x: 2.6, y: y + 0.1, w: 2, h: 0.3, fontSize: 11, bold: true, color: colors.dark, margin: 0 });
  slide6.addText(row[2], { x: 4.6, y: y + 0.1, w: 4.8, h: 0.3, fontSize: 11, color: colors.gray, margin: 0 });
});

// Example of generated content
slide6.addText("生成示例（LLM产出 → 人工审核）", {
  x: 0.5, y: 3.85, w: 9, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});

// LLM Output
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.3, w: 4.3, h: 1.15,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide6.addText("LLM生成（示例）", {
  x: 0.6, y: 4.4, w: 4.1, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.secondary, margin: 0
});
slide6.addText("\"久未谋面，一份来自未来的惊喜已悄然开启...您关注的XX系列迎来年度革新...潮流总在变，但引领者不变。\"", {
  x: 0.6, y: 4.75, w: 4.1, h: 0.6,
  fontSize: 10, fontFace: "Microsoft YaHei", italic: true,
  color: colors.gray, margin: 0
});

// Approved Output
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 4.3, w: 4.3, h: 1.15,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide6.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 4.3, w: 0.06, h: 1.15, fill: { color: colors.success }
});
slide6.addText("审核通过（带ID）", {
  x: 5.4, y: 4.4, w: 4.1, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.success, margin: 0
});
slide6.addText("ID: NEW-01\n\"潮流总在变，但引领者不变。您关注的XX系列迎来年度革新，点击查看→\"", {
  x: 5.4, y: 4.7, w: 4.0, h: 0.7,
  fontSize: 11, fontFace: "Microsoft YaHei",
  color: colors.dark, margin: 0
});

// ==========================================
// SLIDE 7: Stage 4 - ML Matching
// ==========================================
let slide7 = pres.addSlide();
slide7.background = { color: colors.lightGray };

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8, fill: { color: colors.primary }
});
slide7.addText("阶段四：ML模型匹配与A/B测试", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Key concept
slide7.addText("核心价值：将\"对的人\"和\"对的话\"精准匹配，实现转化率最大化", {
  x: 0.5, y: 1.0, w: 9, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei",
  color: colors.secondary, margin: 0
});

// Two approaches comparison
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.5, w: 4.3, h: 2.6,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.5, w: 0.08, h: 2.6, fill: { color: colors.warning }
});
slide7.addText("硬规则匹配（冷启动）", {
  x: 0.75, y: 1.65, w: 3.8, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, margin: 0
});
slide7.addText("原因A → 策略A → 文案A组\n原因B → 策略B → 文案B组\n\n同一策略下随机选择文案", {
  x: 0.75, y: 2.1, w: 3.8, h: 1.8,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.gray, margin: 0
});
slide7.addText("适合：快速验证、零历史数据", {
  x: 0.75, y: 3.85, w: 3.8, h: 0.2,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: colors.warning, margin: 0
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.5, w: 4.3, h: 2.6,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.5, w: 0.08, h: 2.6, fill: { color: colors.success }
});
slide7.addText("ML模型匹配（进阶）", {
  x: 5.45, y: 1.65, w: 3.8, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, margin: 0
});
slide7.addText("输入：用户特征 + 动机标签\n输出：最优文案ID\n\n考虑：客单价、品类偏好、\n优惠券使用习惯、沟通风格偏好", {
  x: 5.45, y: 2.1, w: 3.8, h: 1.8,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.gray, margin: 0
});
slide7.addText("适合：追求效果最大化", {
  x: 5.45, y: 3.85, w: 3.8, h: 0.2,
  fontSize: 10, fontFace: "Microsoft YaHei", bold: true,
  color: colors.success, margin: 0
});

// Experiment design
slide7.addText("A/B测试实验设计", {
  x: 0.5, y: 4.25, w: 9, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});

// Experiment cards
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.7, w: 4.3, h: 0.8,
  fill: { color: colors.primary }
});
slide7.addText("实验组 (AI组) - 50%", {
  x: 0.6, y: 4.8, w: 4.1, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});
slide7.addText("ML模型匹配 + 个性化文案", {
  x: 0.6, y: 5.15, w: 4.1, h: 0.3,
  fontSize: 11,
  color: colors.light, margin: 0
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 4.7, w: 4.3, h: 0.8,
  fill: { color: colors.gray }
});
slide7.addText("对照组 (传统组) - 50%", {
  x: 5.3, y: 4.8, w: 4.1, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});
slide7.addText("统一文案 + 统一权益", {
  x: 5.3, y: 5.15, w: 4.1, h: 0.3,
  fontSize: 11,
  color: colors.lightGray, margin: 0
});

// ==========================================
// SLIDE 8: Stage 5 - Analysis
// ==========================================
let slide8 = pres.addSlide();
slide8.background = { color: colors.lightGray };

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.8, fill: { color: colors.primary }
});
slide8.addText("阶段五：结果分析与复盘", {
  x: 0.5, y: 0.15, w: 9, h: 0.5,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Timeline
slide8.addText("执行活动后14天，进行效果回收与分析", {
  x: 0.5, y: 1.0, w: 9, h: 0.3,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.secondary, margin: 0
});

// Analysis dimensions
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.45, w: 2.9, h: 2.4,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.45, w: 2.9, h: 0.4, fill: { color: colors.primary }
});
slide8.addText("1. 核心指标对比", {
  x: 0.6, y: 1.5, w: 2.7, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});
slide8.addText([
  { text: "券核销率", options: { bold: true, breakLine: true } },
  { text: "人均GMV", options: { bold: true, breakLine: true } },
  { text: "活动ROI", options: { bold: true } }
], {
  x: 0.65, y: 2.0, w: 2.6, h: 1.7,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.dark
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 3.55, y: 1.45, w: 2.9, h: 2.4,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 3.55, y: 1.45, w: 2.9, h: 0.4, fill: { color: colors.secondary }
});
slide8.addText("2. 细分维度下探", {
  x: 3.65, y: 1.5, w: 2.7, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});
slide8.addText([
  { text: "NEW- vs PROFIT- vs EMOTION-", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "各类文案效果对比", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "LLM归因准确性验证", options: {} }
], {
  x: 3.7, y: 2.0, w: 2.6, h: 1.7,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.dark
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 6.6, y: 1.45, w: 2.9, h: 2.4,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 6.6, y: 1.45, w: 2.9, h: 0.4, fill: { color: colors.accent }
});
slide8.addText("3. 决策输出", {
  x: 6.7, y: 1.5, w: 2.7, h: 0.3,
  fontSize: 12, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});
slide8.addText([
  { text: "效果提升验证", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "流程固化建议", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "扩展场景规划", options: {} }
], {
  x: 6.75, y: 2.0, w: 2.6, h: 1.7,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.dark
});

// Key output format
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.0, w: 9, h: 1.5,
  fill: { color: colors.white }, shadow: makeShadow()
});
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.0, w: 0.08, h: 1.5, fill: { color: colors.success }
});
slide8.addText("MIP复盘报告核心结论格式", {
  x: 0.75, y: 4.15, w: 8.5, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, margin: 0
});
slide8.addText("\"本次MIP验证，'LLM洞察+内容+ML匹配'的新流程，相较传统方法：\"\n\n• 券核销率提升了 XX%\n• ROI提升了 YY%\n\n\"下一步建议：将此流程固化，扩展到新客激活、复购提升等场景\"", {
  x: 0.75, y: 4.55, w: 8.5, h: 0.9,
  fontSize: 12, fontFace: "Microsoft YaHei",
  color: colors.dark, margin: 0
});

// ==========================================
// SLIDE 9: Traditional vs AI - THE KEY SLIDE
// ==========================================
let slide9 = pres.addSlide();
slide9.background = { color: colors.primary };

// Title
slide9.addText("传统方式 vs AI方式：核心差异对比", {
  x: 0.5, y: 0.35, w: 9, h: 0.7,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "left", margin: 0
});

// Comparison table header
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.2, w: 9, h: 0.5,
  fill: { color: "2A4A6E" }
});
slide9.addText("维度", { x: 0.6, y: 1.3, w: 2, h: 0.3, fontSize: 13, bold: true, color: colors.white, margin: 0 });
slide9.addText("传统方式", { x: 2.6, y: 1.3, w: 3, h: 0.3, fontSize: 13, bold: true, color: colors.light, margin: 0 });
slide9.addText("AI方式", { x: 5.6, y: 1.3, w: 3.8, h: 0.3, fontSize: 13, bold: true, color: colors.accent, margin: 0 });

// Comparison rows
const comparisons = [
  ["人群洞察", "RFM基础标签\n无法洞察真实流失原因", "LLM深度分析\n归因四大流失类型"],
  ["内容生产", "人工撰写\n效率低、难规模化", "AI批量生成\n多样化、可持续迭代"],
  ["人-内容匹配", "统一文案\n\"千人一面\"", "ML智能匹配\n\"千人千面\""],
  ["效果上限", "核销率低\nROI提升困难", "显著提升\n可量化、可优化"]
];

comparisons.forEach((row, i) => {
  const y = 1.75 + i * 0.85;
  const bg = i % 2 === 0 ? "2A4A6E" : "335878";
  slide9.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 9, h: 0.85, fill: { color: bg } });
  slide9.addText(row[0], { x: 0.6, y: y + 0.2, w: 2, h: 0.45, fontSize: 13, bold: true, color: colors.white, margin: 0 });
  slide9.addText(row[1], { x: 2.6, y: y + 0.15, w: 3, h: 0.55, fontSize: 11, color: colors.lightGray, margin: 0 });
  slide9.addText(row[2], { x: 5.6, y: y + 0.15, w: 3.8, h: 0.55, fontSize: 11, bold: true, color: colors.white, margin: 0 });
});

// Bottom highlight
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 5.1, w: 9, h: 0.4, fill: { color: colors.accent }
});
slide9.addText("结论：AI方式在各个环节实现降维打击，效果提升可达到数个百分点", {
  x: 0.7, y: 5.15, w: 8.6, h: 0.3,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, align: "center", margin: 0
});

// ==========================================
// SLIDE 10: Value Summary
// ==========================================
let slide10 = pres.addSlide();
slide10.background = { color: colors.lightGray };

slide10.addText("AI召回方案：核心价值主张", {
  x: 0.5, y: 0.4, w: 9, h: 0.7,
  fontSize: 32, fontFace: "Microsoft YaHei", bold: true,
  color: colors.primary, align: "left", margin: 0
});

// Three value pillars
const values = [
  { title: "精准洞察", desc: "LLM将用户行为转化为可操作的动机标签，洞察深度远超传统RFM", icon: "🎯" },
  { title: "高效内容", desc: "AI批量生成多样化文案，人工审核保驾护航，质量和效率兼得", icon: "⚡" },
  { title: "智能匹配", desc: "ML模型实现\"原因→策略→文案→风格\"的精细匹配，最大化转化", icon: "🎨" }
];

values.forEach((val, i) => {
  const x = 0.5 + i * 3.1;
  slide10.addShape(pres.shapes.RECTANGLE, {
    x: x, y: 1.3, w: 2.9, h: 2.4,
    fill: { color: colors.white }, shadow: makeShadow()
  });
  slide10.addText(val.icon, {
    x: x, y: 1.45, w: 2.9, h: 0.5,
    fontSize: 28, align: "center", margin: 0
  });
  slide10.addText(val.title, {
    x: x + 0.1, y: 2.05, w: 2.7, h: 0.4,
    fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
    color: colors.primary, align: "center", margin: 0
  });
  slide10.addText(val.desc, {
    x: x + 0.15, y: 2.55, w: 2.6, h: 1.0,
    fontSize: 11, fontFace: "Microsoft YaHei",
    color: colors.gray, align: "center", margin: 0
  });
});

// ROI highlight
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.95, w: 9, h: 1.5,
  fill: { color: colors.primary }
});
slide10.addText("预期效果", {
  x: 0.7, y: 4.1, w: 2, h: 0.35,
  fontSize: 14, fontFace: "Microsoft YaHei", bold: true,
  color: colors.accent, margin: 0
});

// Stats
slide10.addText("券核销率", {
  x: 0.7, y: 4.55, w: 2.5, h: 0.25,
  fontSize: 11, color: colors.light, margin: 0
});
slide10.addText("↑ XX%", {
  x: 0.7, y: 4.75, w: 2.5, h: 0.4,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});

slide10.addText("人均GMV", {
  x: 3.5, y: 4.55, w: 2.5, h: 0.25,
  fontSize: 11, color: colors.light, margin: 0
});
slide10.addText("↑ YY%", {
  x: 3.5, y: 4.75, w: 2.5, h: 0.4,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});

slide10.addText("营销ROI", {
  x: 6.3, y: 4.55, w: 2.5, h: 0.25,
  fontSize: 11, color: colors.light, margin: 0
});
slide10.addText("↑ ZZ%", {
  x: 6.3, y: 4.75, w: 2.5, h: 0.4,
  fontSize: 24, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, margin: 0
});

// ==========================================
// SLIDE 11: Summary
// ==========================================
let slide11 = pres.addSlide();
slide11.background = { color: colors.primary };

// Decorative element
slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.1, fill: { color: colors.accent }
});

slide11.addText("总结与下一步", {
  x: 0.5, y: 1.2, w: 9, h: 0.7,
  fontSize: 36, fontFace: "Microsoft YaHei", bold: true,
  color: colors.white, align: "center", margin: 0
});

slide11.addText("LLM归因 → 解决\"说什么\"（What）\nML匹配 → 解决\"怎么说\"（How）\n\n双引擎驱动，实现会员召回效果飞跃", {
  x: 0.5, y: 2.1, w: 9, h: 1.2,
  fontSize: 16, fontFace: "Microsoft YaHei",
  color: colors.light, align: "center", margin: 0
});

slide11.addShape(pres.shapes.RECTANGLE, {
  x: 2, y: 3.6, w: 6, h: 0.5, fill: { color: colors.accent }
});
slide11.addText("立即启动MIP试点，6-8周验证效果", {
  x: 2, y: 3.65, w: 6, h: 0.4,
  fontSize: 16, fontFace: "Microsoft YaHei", bold: true,
  color: colors.dark, align: "center", margin: 0
});

slide11.addText("建议扩展场景：新客激活 | 复购提升 | 流失预警", {
  x: 0.5, y: 4.8, w: 9, h: 0.4,
  fontSize: 13, fontFace: "Microsoft YaHei",
  color: colors.gray, align: "center", margin: 0
});

// Save
pres.writeFile({ fileName: "AI会员召回方案.pptx" })
  .then(() => console.log("PPT created successfully!"))
  .catch(err => console.error(err));
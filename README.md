# member-recall Skill

AI 驱动的会员召回方案 Claude Code Skill

## 安装方法

### 方法 1：复制到本地 skills 目录

将 `skills/member-recall` 目录复制到你的 Claude Code skills 目录：

```
C:\Users\<你的用户名>\.claude\skills\member-recall\
```

### 方法 2：从 GitHub 克隆

```bash
git clone https://github.com/noahwang550/member-recall.git
```

然后将内容复制到 skills 目录。

## 使用方法

### 生成演示文稿

```bash
cd skills/member-recall/scripts
npm install
node create_ppt.js
```

这将生成 `AI会员召回方案.pptx` 文件。

### 在 Claude Code 中使用

当你想创建会员召回方案或执行召回流程时，直接调用此 skill：

```
/member-recall
```

或者描述你的需求，如：
- "帮我创建一个会员召回方案"
- "如何执行 AI 驱动的会员召回"
- "会员召回的五个阶段是什么"

## 技能内容

- **SKILL.md**: 完整的五阶段召回流程文档
- **scripts/create_ppt.js**: PPT 生成脚本
- **scripts/package.json**: 依赖配置

## GitHub 仓库

https://github.com/noahwang550/member-recall
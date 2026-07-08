# DeepGarden 投资研究 Skill 系列

一套面向 A股/港股投资的 **WorkBuddy / CodeBuddy Skill** 方法论合集，覆盖「申购前研究 → 上市后业绩跟踪 → 研报独立复核」的完整研究闭环。

> 本仓库为系列聚合仓。三个 skill **各自独立、可单独安装使用**，彼此无代码或安装依赖；仅 `deepgarden-report-deep-read` 在文档中引用 `deepgarden-earnings-tracking` 的仓库目录做「双向印证」，且该引用降级优雅（缺定期报告系列时自动标注「待补充印证」）。

## 包含的 Skill

| Skill | 说明 | 适用场景 |
|---|---|---|
| `deepgarden-ipo-research` | 新股/公司深度研究五维度评估框架（市场前景 / 竞争格局 / 经营特征 / 财务特征 / 企业素质） | 新股评估、打新分析、IPO 研究 |
| `deepgarden-earnings-tracking` | 按提示词框架批量阅读上市公司定期报告（年报/半年报/季报），生成 Obsidian 友好 Markdown | 定期财报跟踪、业绩梳理 |
| `deepgarden-report-deep-read` | 公司研报四步结构化精读 + 研报跟踪对比 Hub + 与定期报告双向印证，输出带页码引用的笔记 | 研报精读、研报对比、研报印证定期报告 |

## 目录结构

```
deepgarden-skills/
├── deepgarden-ipo-research/        # 新股研究
│   ├── SKILL.md
│   └── references/sample-output-*.md
├── deepgarden-earnings-tracking/   # 定期财报跟踪
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
└── deepgarden-report-deep-read/    # 研报精读
    ├── SKILL.md
    ├── scripts/extract_report.py
    └── references/                 # Hub 范例 / 精读范例 / 使用指南 / 跟踪 Hub 模板
```

## 安装方式

**方式 A：手动安装（推荐）**
1. 克隆或下载本仓库；
2. 将需要的 skill 目录整体复制到 WorkBuddy 的 skill 目录：
   - 用户级：`~/.workbuddy/skills/`
   - 项目级：`<你的仓库>/.workbuddy/skills/`
3. 重启/刷新 WorkBuddy，即可通过自然语言触发（如「用 DeepGarden 研报精读 框架精读某 PDF」）。

**方式 B：Git 子模块**
```bash
git submodule add <本仓库地址> .workbuddy/skills/deepgarden-skills
```

## 运行依赖
- 各 skill 的 PDF 抽取脚本依赖 Python `pdfplumber`（首次使用时会尝试自动安装，或手动 `pip install pdfplumber`）。
- 其余为纯提示词 + Markdown 模板，无额外运行时依赖。

## 关于 DeepGarden 出品
DeepGarden 是面向个人投资者的研究方法论品牌，强调「结构化、带引用、跨期印证、独立复核」。所有输出均附「仅供参考研究，不构成买卖建议」声明。

## 免责声明
本仓库所有内容仅用于研究与学习，**不构成任何投资建议**。据此操作风险自担。

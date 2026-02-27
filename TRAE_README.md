# cursor-agent-team — TRAE_CN 适配说明

TRAE_CN（字节跳动）平台适配版本。将 cursor-agent-team 的单人多角色 AI 协作方法论从 Cursor IDE 迁移到 TRAE_CN。

## 前提条件

- TRAE_CN v3.3.21+（或 v1.3.0+）
- Python 3.8+
- Git
- 使用 main 分支，TRAE 适配已包含在内

## 安装

### 1. 在已有项目中添加子模块

与 Cursor 版相同：在已有项目根目录将 cursor-agent-team 作为子模块加入。若项目是 clone 且已带 `--recurse-submodules`，则已有 `cursor-agent-team` 目录，可跳过本步。

```bash
git submodule add -f https://github.com/thiswind/cursor-agent-team.git cursor-agent-team
```

### 2. 运行安装脚本

```bash
bash cursor-agent-team/install_trae.sh
```

脚本会：
- 在项目根目录创建 `.trae/rules/` 与 `.trae/skills/`
- 将 `project_rules.md` 复制到 `.trae/rules/`
- 将全部 6 个 Skills 复制到 `.trae/skills/`

### 3. 在 TRAE 中手动创建智能体

在 TRAE → 设置 → 智能体中创建三个智能体（讨论搭档、执行组员、提示工程师）。每个智能体请使用**按智能体分的安装指南**，按步骤填写所有表单项（名称、提示词、英文标识名、何时调用、工具）。

- 索引与链接：见 [_trae/agent_prompts/README.md](_trae/agent_prompts/README.md)
- 带预填值的分步说明：见 `_trae/agent_prompts/<name>_INSTALL_GUIDE.md`（讨论搭档、执行组员、提示工程师各有一份）

说明：英文标识名、何时调用在 TRAE 中为必填项。

### 4. 更新（可选）

拉取 cursor-agent-team 更新后重新运行安装脚本，与主 README 一致：

```bash
git submodule update --remote cursor-agent-team && bash cursor-agent-team/install_trae.sh
```

## 使用方式

典型用法是多角色协作：讨论与执行分离、方案驱动。下面按三条常见流程举例。

### 流程一：讨论 → 出方案 → 执行

先和**讨论搭档**分析需求、定步骤并生成执行方案（如 `ai_workspace/plans/PLAN-XX-001.md`），再让**执行组员**按该方案逐步执行。让执行组员执行时，可说「执行」或「/crew PLAN-XX」（如 PLAN-AC-001），或在指令里写一段简短的方案要点。

```
@讨论搭档 我想做 XXX 功能/重构，先一起分析一下可行性和步骤，然后生成一份可执行的方案
（方案生成后）
@执行组员 执行 ai_workspace/plans/PLAN-XX-001.md
```

### 流程二：讨论 → 定需求/方案 → 提示工程师建新角色

先和**讨论搭档**确定新角色的职责、边界与流程，产出 AGENT-REQUIREMENT 或方案；再让**提示工程师**根据该文档生成 Agent 提示词与 INSTALL_GUIDE。

```
@讨论搭档 我需要一个用于 YYY 场景的新智能体，我们先把职责、边界和流程定下来，出一份 AGENT-REQUIREMENT
（需求/文档确定后）
@提示工程师 根据刚才和讨论搭档确定的 AGENT-REQUIREMENT（或 ai_workspace/agent_requirements/ 里的文件），生成新智能体的提示词和 INSTALL_GUIDE
```

### 流程三：小改现有提示词

先和**讨论搭档**确认要改什么、改到什么程度；再让**提示工程师**按结论修改对应 `_trae/agent_prompts/` 下的文件。

```
@讨论搭档 我想在讨论搭档的提示词里增加对 Z 场景的说明，你帮我看下该怎么表述、改哪一段
（结论明确后）
@提示工程师 按刚才讨论的结论，在 discussion_partner.md 里增加对 Z 场景的说明
```

三个智能体也可单独用于简单询问或小改，但完整任务建议按上述流程多角色协作。

## 目录结构

```
cursor-agent-team/
├── _trae/                          # TRAE 专用配置
│   ├── agent_prompts/              # Agent 提示词模板（复制到 TRAE GUI）
│   │   ├── README.md
│   │   ├── discussion_partner.md
│   │   ├── discussion_partner_INSTALL_GUIDE.md
│   │   ├── crew_member.md
│   │   ├── crew_member_INSTALL_GUIDE.md
│   │   ├── trae_prompt_engineer.md
│   │   └── trae_prompt_engineer_INSTALL_GUIDE.md
│   ├── rules/                      # 项目规则
│   │   └── project_rules.md
│   └── skills/                     # 跨智能体 Skills
│       ├── skill-gleaning/SKILL.md
│       ├── skill-wandering/SKILL.md
│       ├── skill-persona/SKILL.md
│       ├── skill-history-handler/SKILL.md
│       ├── skill-tts/SKILL.md
│       └── skill-social-media/SKILL.md
├── _cursor/                        # Cursor 专用（TRAE 不使用）
├── _scripts/                       # 共用脚本（两平台通用）
├── ai_workspace/                   # 共用工作区（两平台通用）
├── install_trae.sh                 # TRAE 安装脚本
└── TRAE_README.md                  # 本文件
```

## 与 Cursor 版本的区别

| 维度 | Cursor | TRAE_CN |
|------|--------|---------|
| 角色唤起 | `/discuss`、`/crew`、`/prompt_engineer` 命令 | `@讨论搭档`、`@执行组员`、`@提示工程师` 智能体 |
| 规则注入 | Cursor 自动注入 `.mdc` 文件 | 项目规则在 `.trae/rules/`，Skills 在 `.trae/skills/` |
| 横切能力 | 始终生效的 `.mdc` 规则 | TRAE 按需加载 Skills |
| 智能体创建 | 在 `.cursor/commands/` 中定义 | 在 GUI 中手动创建并粘贴提示词 |
| 脚本 | 相同 | 相同 |
| AI 工作区 | 相同 | 相同 |

## 更新智能体提示词

当 `_trae/agent_prompts/` 中的提示词有更新时：
1. 拉取最新：`cd cursor-agent-team && git pull`
2. 打开 TRAE → 设置 → 智能体
3. 找到要更新的智能体
4. 用更新后文件中的提示词内容替换原提示词
5. 保存

## 更新 Skills 与 Rules

```bash
bash cursor-agent-team/install_trae.sh
```

会重新将 rules 与 skills 复制到 `.trae/`。

---

**版本**：v0.11.1（更新于 2026-02-27）。TRAE 已合并至 main，安装请按各智能体的 INSTALL_GUIDE 操作。

# cursor-agent-team — TRAE_CN 适配说明

TRAE_CN（字节跳动）平台适配版本。将 cursor-agent-team 的单人多角色 AI 协作方法论从 Cursor IDE 迁移到 TRAE_CN。

## 前提条件

- TRAE_CN v3.3.21+（或 v1.3.0+）
- Python 3.8+
- Git

## 安装

### 1. 克隆并带子模块

使用默认分支（main），TRAE 适配已包含在内。

```bash
git clone --recurse-submodules <your-project-repo>
cd <your-project>
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

- 索引与链接：见 `_trae/agent_prompts/README.md`
- 带预填值的分步说明：见 `_trae/agent_prompts/<name>_INSTALL_GUIDE.md`（讨论搭档、执行组员、提示工程师各有一份）

说明：英文标识名、何时调用在 TRAE 中为必填项。

## 使用方式

### 讨论搭档（Discussion Partner）

用于讨论、分析、头脑风暴与生成方案，不执行具体操作。

```
@讨论搭档 我们来讨论一下项目架构
@讨论搭档 分析一下这个方案的优劣
@讨论搭档 生成执行方案
```

### 执行组员（Crew Member）

用于按讨论搭档生成的方案严格执行。

```
@执行组员 PLAN-AC-001
@执行组员 执行最新的方案
```

### 提示工程师（TRAE Prompt Engineer）

用于创建与维护 Agent 提示词、Skills 与项目规则。

```
@提示工程师 创建一个新的写作助手 Agent
@提示工程师 更新讨论搭档的提示词
```

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

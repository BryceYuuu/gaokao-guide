# gaokao-guide 高考志愿指南

`gaokao-guide` 是一个面向中国高考家庭的通用 LLM 指令包，同时适配 Codex Skill。它可用于高考填志愿、高考报志愿、高考志愿填报、选大学、选专业、冲稳保排序、院校专业组风险审计、专业调剂审计、志愿表审计、学校体检、专业核实、看板输出和一页式信息图生成。

它不只限于 Codex。你也可以把它放进 ChatGPT 自定义 GPT、Claude Project、Gemini Gems、OpenAI API system prompt、本地大模型或其他支持长提示词/知识库的 LLM 工具里使用。

![gaokao-guide 高考志愿指南](docs/assets/gaokao-guide-hero.png)

## 适合什么场景

- 不知道“这个分数/位次能上什么大学”。
- 想做高考志愿填报方案，但不想从空白开始描述偏好。
- 需要按位次做冲、稳、保、观察、剔除分层。
- 需要检查院校专业组、服从调剂、专业组下限风险。
- 需要把第三方志愿卡、Excel、CSV、截图候选表做风险审计。
- 想比较学校、城市、专业、就业路径、家庭约束和学生承受力。
- 不想看大段文字，希望输出看板、短表、风险灯。
- 想生成一张设计过的高考志愿汇总信息图。

![功能卡片](docs/assets/gaokao-readme-feature-cards.png)

## 核心能力

- 首次咨询先给可复制填写的问诊表，让家长不用从零组织信息。
- 坚持位次优先：位次优先于裸分，分数只能粗筛。
- 建立证据账本：一分一段、招生计划、录取位次、院校专业组、招生章程、待核验项。
- 生成候选池：冲、稳、保、观察、剔除。
- 审计专业组下限和服从调剂风险。
- 深挖学校真实体验：校风、安全、宿舍、校区、体检限制、转专业、保研、绩点、挂科、费用和隐形成本。
- 核实专业在具体学校里的成色：硕博点、认证、课程新旧、行业出口、升学去向和专业组下限。
- 做轻量位次模拟：用近年位次区间做冲稳保压力测试，明确模型边界，不伪装成官方录取概率。
- 扫描低估机会和热门方向过热风险。
- 引入人生杠杆复核：评估平台、城市、行业、家庭资源、失败成本和入学后兑现动作。
- 输出看板式摘要，减少大段文字。
- 支持从结构化 JSON 生成一页式 SVG 汇总图。

## 目录结构

```text
gaokao-guide/
├── README.md
├── UNIVERSAL_PROMPT.md             # 通用 LLM 复制版提示词
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── intake-form.md              # 问诊表
│   ├── intake-and-routing.md       # 问诊和任务路由
│   ├── evidence-ledger.md          # 证据账本
│   ├── strategy-and-portfolio.md   # 候选池和策略组合
│   ├── major-career-map.md         # 专业和职业路径
│   ├── school-major-audit.md       # 学校体检和专业核实
│   ├── deep-school-audit.md        # 校风、安全、绩点、暗规则深挖
│   ├── rank-model-and-simulation.md # 位次模型和模拟说明
│   ├── leverage-review-methodology.md # 人生杠杆和策略复核
│   ├── dashboard-templates.md      # 看板模板
│   ├── infographic-output.md       # 信息图输出说明
│   └── ...
└── scripts/
    ├── audit_candidates.py         # 候选表审计脚本
    ├── rank_simulator.py           # 轻量位次模拟脚本
    └── render_summary_svg.py       # SVG 信息图生成脚本
```

## 在不同 LLM 中使用

### Codex

直接使用 `gaokao-guide/SKILL.md` 作为 Skill 入口，`references/` 作为按需加载资料，`scripts/` 作为可执行工具。

安装到当前用户的 Codex skills 目录：

```bash
python3 install.py
```

默认安装位置是：

```text
${CODEX_HOME:-~/.codex}/skills/gaokao-guide
```

也可以显式指定：

```bash
python3 install.py --platform codex
```

### Claude 本地 Skill

Claude 的平台内置目录 `/mnt/skills/` 通常是只读挂载，只能读取官方或平台预置 Skill，不能作为自定义 Skill 的安装位置。自定义 Skill 应放在本地可写目录。

全局安装，所有 Claude 会话可用：

```bash
python3 install.py --platform claude
```

默认安装位置是：

```text
${CLAUDE_HOME:-~/.claude}/skills/gaokao-guide
```

项目局部安装，仅当前项目目录生效：

```bash
python3 install.py --platform claude --scope project
```

对应位置是：

```text
./.claude/skills/gaokao-guide
```

手动安装也可以：

```bash
mkdir -p ~/.claude/skills
cp -R gaokao-guide ~/.claude/skills/gaokao-guide
```

安装后完全退出 Claude 并重新打开，执行 `/skills` 检查是否加载。如果能正常加载，说明 `SKILL.md` 内容没有问题；如果仍然报 `/mnt/skills` 只读，通常是外部安装器、MCP 配置或环境变量仍指向系统只读目录。

如果你的运行环境提示 `/mnt/skills` 是系统只读挂载，这是正常的。不要把 `/mnt/skills` 当作永久安装目录；使用上面的 `install.py` 会自动安装到用户可写目录。也可以手动指定：

```bash
python3 install.py --target ~/.codex/skills
python3 install.py --platform claude --target ~/.claude/skills
```

### 关于 `/mnt/skills` 只读

`/mnt/skills` 通常是平台运行时挂载进来的系统级只读目录，控制权在平台侧，不在用户、Claude、Codex 或本仓库这边。即使容器里有 root 权限，写操作也会被操作系统的挂载层拒绝。

所以这个问题不能通过开源仓库里的 installer 绕过。当前可行方案是：

- Codex 安装到用户可写目录：`${CODEX_HOME:-~/.codex}/skills/gaokao-guide`
- Claude 全局安装到用户可写目录：`${CLAUDE_HOME:-~/.claude}/skills/gaokao-guide`
- Claude 项目局部安装到：`./.claude/skills/gaokao-guide`
- 或者不安装为系统级 skill，直接使用 `UNIVERSAL_PROMPT.md` + `references/` 作为通用 LLM 指令包
- 或者 fork 本仓库，在你自己的运行环境里把 `gaokao-guide/` 目录挂载到目标 LLM 可读取的位置

本项目保持完全开源，解决的是“内容、方法、脚本、提示词可自由使用和迁移”，不是“强行写入平台只读挂载目录”。

如果你使用本地 Skill MCP，请确认配置读取的是本地可写目录，而不是 `/mnt/skills`。示例：

```json
{
  "mcpServers": {
    "local-skills": {
      "command": "local-skills-mcp",
      "env": {
        "SKILLS_DIR": "~/.claude/skills"
      }
    }
  }
}
```

不同 MCP 工具的环境变量名可能不同，`SKILLS_DIR` 需要以你实际使用的 MCP 文档为准。

### ChatGPT 自定义 GPT / Claude Project / Gemini Gems

把 [UNIVERSAL_PROMPT.md](UNIVERSAL_PROMPT.md) 复制到系统提示词或项目说明里，再把 `references/` 目录中的资料作为知识库上传。推荐至少上传：

- `references/intake-form.md`
- `references/evidence-ledger.md`
- `references/strategy-and-portfolio.md`
- `references/major-career-map.md`
- `references/school-major-audit.md`
- `references/deep-school-audit.md`
- `references/rank-model-and-simulation.md`
- `references/leverage-review-methodology.md`
- `references/dashboard-templates.md`
- `references/infographic-output.md`

### OpenAI API / 本地 LLM

把 `UNIVERSAL_PROMPT.md` 放进 system prompt。若上下文长度有限，优先放入问诊、证据账本、策略组合和输出模板；需要执行表格审计或信息图生成时，再调用 `scripts/` 中的 Python 脚本。

### 能不能“一键安装到任何 LLM”

不同 LLM 平台没有统一的 Skill 安装标准，所以不能保证像 Codex 一样自动识别 `SKILL.md`。但这个仓库的核心能力是可迁移的：把通用提示词作为系统指令，把 references 作为知识库，把 scripts 作为外部工具即可。

## 示例提问

```text
请使用 $gaokao-guide 帮我做一版高考志愿填报方案。

省份：江苏
年份：2026
科类/选科：物理类，物化生
分数：608
位次：约34500
批次：本科批
预算：公办普通学费优先
专业偏好：计算机、电子信息、电气、自动化
排斥专业：土木、化工、材料、环境、生物
风险偏好：均衡偏稳，不能滑档

请先输出看板，不要大段文字。
```

## 默认问诊表

Skill 首次启动时会先让用户填写中等长度问诊表，例如：

```text
【基础信息】
省份：
年份：
批次：本科批 / 专科批 / 提前批 / 专项计划 / 艺术体育 / 其他：
科类/选科：物理类 / 历史类 / 理科 / 文科 / 3+3综合；选科：
分数：
位次：有 / 没有 / 估算位次：
目前阶段：出分前估分 / 已出分 / 志愿填报期 / 已有候选表

【家庭约束】
预算：只考虑公办普通学费 / 可接受民办 / 可接受中外合作，最高每年：__ 万
地域：本省优先 / 周边省份可接受 / 全国都可看 / 明确不去：

【专业和城市偏好】
想优先看的方向：计算机软件AI / 电子信息通信 / 电气电网 / 自动化智能制造 / 医学医技药学 / 师范教育 / 法学考公 / 财会金融 / 机械车辆 / 交通土建 / 文史外语传媒 / 还没想好 / 其他：
明确排斥的专业：土木 / 化工 / 材料 / 环境 / 生物 / 护理 / 医学长学制 / 师范 / 农学 / 机械 / 金融 / 法学 / 管理 / 不排斥 / 其他：
优先城市/地区：本省 / 一线城市 / 新一线 / 省会 / 长三角 / 珠三角 / 京津冀 / 成渝 / 其他：
排斥城市/地区：东北 / 西北 / 西南 / 华北 / 县城或远郊校区 / 气候太冷 / 气候太热 / 无
```

## 候选表审计

当你有志愿卡导出、Excel CSV、手工整理候选表时，可以运行：

```bash
python3 gaokao-guide/scripts/audit_candidates.py candidates.csv --student-rank 34500
```

脚本会检查这些机械风险：

- 关键列缺失
- 重复候选
- 信源状态薄弱
- 保底层太薄
- 风险字段为空
- 待核验项为空
- 小计划数或计划数缺失

脚本只做机械审计，不替代官方数据核验和最终志愿判断。

## 轻量位次模拟

当候选表里有近年录取位次区间时，可以运行：

```bash
python3 gaokao-guide/scripts/rank_simulator.py examples/sample_candidates.csv --student-rank 34500 --runs 5000 --output examples/sample_candidates.simulation.json
```

它会输出：

- 每个候选的模拟分层：冲、稳、保、观察。
- 按志愿顺序模拟的首个录取分布。
- 无录取压力测试结果。
- 信源、计划数和专业组下限等风险提示。

这个脚本不是完整数据库录取概率引擎，也不是官方录取预测。它解决的是“候选表有没有明显排序风险、保底是否够厚、冲稳保是否失衡”。

## 生成一页式信息图

可以把结构化结果渲染成一张 SVG 信息图：

```bash
python3 gaokao-guide/scripts/render_summary_svg.py input.json --output gaokao-summary.svg
```

SVG 生成是确定性的，适合承载位次、风险等级、待核验项等关键文字，避免纯 AI 生图把数字或学校名画错。

![数据接入路线图](docs/assets/gaokao-data-roadmap.png)

## 样例与测试

仓库内置了可直接查看和复现的演示材料：

- [江苏案例](examples/jiangsu-case.md)：物理类中上分段，热门城市 + 工科主线。
- [山东案例](examples/shandong-case.md)：3+3 综合，专业 + 院校模式。
- [河南案例](examples/henan-case.md)：高竞争省份，保本科与就业路径并重。
- [候选表示例 CSV](examples/sample_candidates.csv)：用于测试候选表审计。
- [候选表审计输出](examples/sample_candidates.audit.json)：由 `audit_candidates.py` 生成。
- [候选表位次模拟输出](examples/sample_candidates.simulation.json)：由 `rank_simulator.py` 生成。
- [SVG 输入 JSON](examples/svg-summary-input.json)：用于生成一页式信息图。
- [SVG 样例图](examples/gaokao-summary.svg)：由 `render_summary_svg.py` 生成。
- [SVG 与数据接入路线图设计稿](docs/svg-and-roadmap-design.md)：给设计图使用的文字和结构。

运行脚本测试：

```bash
python3 tests/test_scripts.py
```

重新生成样例审计输出：

```bash
python3 gaokao-guide/scripts/audit_candidates.py examples/sample_candidates.csv --student-rank 34500 --output examples/sample_candidates.audit.json
```

重新生成样例 SVG：

```bash
python3 gaokao-guide/scripts/render_summary_svg.py examples/svg-summary-input.json --output examples/gaokao-summary.svg
```

## 关键词

高考填志愿、高考报志愿、高考志愿填报、填报志愿、报考大学、选大学、选专业、专业选择、分数能上什么大学、位次能上什么学校、冲稳保、平行志愿、院校专业组、专业调剂、服从调剂、一分一段、招生计划、录取位次、志愿卡、志愿表、学校体检、专业核实、高考志愿看板、高考志愿信息图。

## 开源协议

本项目使用 MIT License 开源。你可以自由使用、复制、修改、分发、二次开发和集成到其他 LLM 工作流中；保留原始版权和许可声明即可。

## 免责声明

本 Skill 只做高考志愿决策支持，不构成录取承诺、就业承诺、保研承诺、转专业承诺或薪资承诺。正式填报前，应以省级考试院、高校招生网、招生章程、当年招生计划和官方志愿系统为准，并结合学校老师或可信专业人士复核。

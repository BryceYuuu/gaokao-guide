# Dashboard Templates

Use this file when the user asks for 看板、仪表盘、摘要、短表、不要大段文字, or when a parent-facing answer should be scannable.

## Dashboard Rules

- Use compact Markdown tables and short status cards.
- Avoid paragraphs longer than 2 lines.
- Start with the dashboard, then offer to expand evidence only if needed.
- Use text status labels instead of color-only signals: `绿灯`, `黄灯`, `红灯`, `灰灯`.
- Every card must include the practical implication, not just a label.
- Do not hide uncertainty; put it in `待核验`.

## Top Summary Cards

```markdown
| 模块 | 状态 | 一句话判断 |
| --- | --- | --- |
| 录取安全 | 黄灯 | 有可做方案，但保底必须看专业组下限。 |
| 专业匹配 | 绿灯 | 数理基础适合电子信息/电气/自动化。 |
| 城市偏好 | 黄灯 | 只盯热门城市会压缩选择空间。 |
| 预算风险 | 绿灯 | 公办普通学费可控，高价中外合作剔除。 |
| 最大风险 | 红灯 | 服从调剂滑入排斥专业。 |
```

## Candidate Pool Board

```markdown
| 层级 | 候选方向 | 用途 | 进入条件 | 风险灯 |
| --- | --- | --- | --- | --- |
| 冲 | 热门城市强专业 | 少量上行机会 | 专业组下限可接受 | 红/黄 |
| 稳 | 公办工科主线 | 主力志愿 | 位次有缓冲、计划稳定 | 黄/绿 |
| 保 | 真可接受保底 | 防滑档 | 全组专业能接受 | 绿 |
| 观察 | 低估机会 | 备选扩展 | 证据补齐后再定 | 灰/黄 |
| 剔除 | 不可接受组 | 避坑 | 含排斥专业或费用超限 | 红 |
```

## Risk Heatmap

```markdown
| 风险项 | 等级 | 影响 | 处理 |
| --- | --- | --- | --- |
| 专业组下限 | 高 | 可能录到不想读的专业 | 逐组核验，不合格不服从 |
| 招生计划变化 | 中 | 冲稳保会变 | 查当年计划和计划变更 |
| 热门专业溢价 | 中 | 分数买不到对应回报 | 给同层次替代 |
| 高价项目 | 高 | 超预算 | 直接剔除或单列 |
```

## Strategy Board

```markdown
| 方案 | 适合什么目标 | 主线 | 代价 | 当前结论 |
| --- | --- | --- | --- | --- |
| 主方案 | 稳中求好 | 本省/周边公办 + 可接受专业组 | 热门城市可能降级 | 先做 |
| 对冲方案 | 防止偏好过窄 | 省外/非核心城市工科强校 | 离家远、城市体验弱 | 必做 |
| 机会方案 | 找低估项 | 地理折价/行业特色/低热强专业 | 需要证据补齐 | 观察 |
```

## Major Path Board

```markdown
| 专业方向 | 匹配度 | 出路主线 | 主要坑点 | 建议 |
| --- | --- | --- | --- | --- |
| 计算机/AI | 中-高 | 大厂/软件/考研 | 热度高、学校差异大 | 可冲，不做唯一主线 |
| 电子信息 | 高 | 通信/硬件/考研/制造 | 本科就业质量看学校 | 主线 |
| 电气 | 高 | 电网/能源/制造 | 电网通道看学校和地区 | 主线 |
| 自动化 | 中-高 | 制造/控制/机器人 | 口径宽，需看课程 | 主线备选 |
```

## Verification Board

```markdown
| 待核验 | 优先级 | 为什么 |
| --- | --- | --- |
| 当年一分一段 | 高 | 确认位次锚点 |
| 当年招生计划 | 高 | 决定计划数和专业组 |
| 专业组内全部专业 | 高 | 决定能否服从调剂 |
| 招生章程/学费/校区 | 中 | 过滤费用和校区风险 |
| 近三年投档位次 | 中 | 判断大小年和稳定性 |
```

## One-Screen Output Order

Use this order for concise dashboard output:

1. `Top Summary Cards`
2. `Candidate Pool Board`
3. `Risk Heatmap`
4. `Strategy Board`
5. `Verification Board`
6. `Next Action`: one line only.

If the user wants a shareable image, convert these same sections into the JSON schema in `infographic-output.md` and render with `scripts/render_summary_svg.py`.

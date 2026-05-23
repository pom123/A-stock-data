# a-stock-data

A 股全栈数据工具包 — 10 层架构 · 29 个端点 · 11 个数据源实测

一个自包含的 Skill 文件，把分散在 11 个数据源里的 A 股原始数据整合成 AI 编程助手直接能用的工具集。你不用再背 mootdx 的 K 线参数、东财的 PDF Referer 头、iwencai 的 X-Claw 鉴权、百度 PAE 的 Header 拼接——全部封装好了。

> 兼容 [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://github.com/openai/codex) · [OpenClaw](https://github.com/anthropics/openclaw)
>
> Skill 文件本质是结构化 Markdown + 内嵌 Python，任何支持上下文注入的 AI 编程助手都能用。

---

## Donate

如果这个工具帮到了你的投研工作流，欢迎请作者喝杯咖啡 ☕

<p align="center">
  <img src="./assets/wechat-sponsor.jpg" width="240" alt="微信赞赏码">
</p>
<p align="center">
  <a href="https://ifdian.net/a/simonlin">爱发电</a> ·
  <a href="https://buymeacoffee.com/simonlin1212">Buy Me a Coffee</a>
</p>

> 想要什么数据端点？欢迎开 [Issue](https://github.com/simonlin1212/a-stock-data/issues) 提需求，赞助者的 Issue 优先处理。

---

## 架构

```
A 股全栈数据 · 十层架构
│
├── 行情层      mootdx + 腾讯财经        K线 + 五档盘口 + PE/PB/市值/换手率/涨跌停
├── 研报层      东财 + akshare + iwencai  研报列表 / PDF下载 / 一致预期 / NL搜索
├── 信号层      同花顺 + 百度股市通       强势股 + 题材归因 + 北向资金 + 概念板块
│              + akshare + 东财DC       + 资金流向 + 龙虎榜 + 全市场龙虎榜 + 解禁 + 行业对比
├── 新闻层      akshare × 3              个股新闻 / 财联社快讯 / 全球资讯
├── 基础数据    mootdx finance / F10     37字段季报 + 9类公司资料
├── 财务趋势层  同花顺 + 东财             近3年营收/净利/增速/ROE/毛利率 + 80+字段深度分析 (V2.2)
├── 技术面层    mootdx K线 + stockstats  MA5/10/20/60/120 + MACD/RSI/BOLL + 趋势信号 (V2.2)
├── 筹码分布层  mootdx K线 + 指数衰减     获利盘/套牢盘/平均成本/90%集中区/抛压支撑 + 资金流向 (V2.3)
├── 行业估值层  同花顺行业 + 腾讯批量      同行PE/PB均值/中位数/个股排名 (V2.2)
└── 公告层      巨潮 cninfo + mootdx     沪深北全量公告
```

---

## 快速开始

**3 步，2 分钟。**

```bash
# 1. 创建 skill 目录
mkdir -p ~/.claude/skills/a-stock-data

# 2. 把 SKILL.md 放进去
curl -o ~/.claude/skills/a-stock-data/SKILL.md \
  https://raw.githubusercontent.com/simonlin1212/a-stock-data/main/SKILL.md

# 3. 安装依赖
pip install mootdx akshare requests pandas stockstats

# 4. (可选) 验证环境
python check_env.py
```

启动 Claude Code，说一句「帮我看看 688017 的估值」，自动激活。

> **Codex / OpenClaw 用户：** 把 SKILL.md 的内容贴入你的系统 prompt 或项目上下文文件即可，内嵌的 Python 代码可直接执行。

---

## 29 个端点能力清单

### 行情层（实时，不封 IP）

| 端点 | 数据 |
|------|------|
| mootdx 行情 | K线(多周期) + 五档盘口 + 逐笔成交 + 实时报价 46 字段 |
| 腾讯财经 | PE(TTM) / PB / 总市值 / 流通市值 / 换手率 / 涨跌停价 / 量比 |

### 研报层

| 端点 | 数据 |
|------|------|
| 东财 reportapi | 研报列表 + 评级 + 三年 EPS 预测 |
| 东财 PDF 下载 | 完整研报 PDF（已处理 Referer 鉴权） |
| akshare 一致预期 | 同花顺源机构一致预期 EPS |
| iwencai NL 搜索 | 自然语言跨主题研报检索 |

### 信号层（V2.1 大幅扩展）

| 端点 | 数据 |
|------|------|
| 同花顺热点 | 当日强势股 + 题材归因 reason tags（编辑部人工标注） |
| 同花顺北向（实时） | 沪股通 / 深股通分钟级流向（262 个时间点） |
| 同花顺北向（历史） | 本地自缓存日级历史（V2.1 改） |
| 百度概念板块 | 行业 / 概念 / 地域三维归属 + 当日涨跌幅（V2.1 新增） |
| 百度资金流向 | 主力 / 散户 / 超大单分钟级 + 20 日历史（V2.1 新增） |
| 龙虎榜席位 | 上榜记录 + 买卖席位 TOP5 + 机构动向（V2.1 新增） |
| 全市场龙虎榜 | 每日全市场上榜股票 + 净买额排名 + 上榜原因（V2.1 新增） |
| 限售解禁日历 | 历史解禁 + 未来 90 天待解禁预警（V2.1 新增） |
| 行业横向对比 | 同花顺 90 行业涨跌排名 + 领涨股（V2.1 新增） |

### 新闻层

| 端点 | 数据 |
|------|------|
| 个股新闻 | 东财个股新闻流 |
| 财联社快讯 | 分钟级电报 |
| 全球资讯 | 东财全球财经资讯 |

### 基础数据 + 公告

| 端点 | 数据 |
|------|------|
| 季报快照 | 37 字段（EPS / ROE / 净利润 / 主营收入...） |
| F10 公司资料 | 9 大类文本（V2.1 截断优化，-70% token） |
| 巨潮公告 | 沪深北交所全量公告 |

### 财务趋势层（V2.2 新增）

| 端点 | 数据 |
|------|------|
| 同花顺财务摘要 | 近3年营收/净利/增速/ROE/毛利率多期趋势 |
| 东财财务指标 | 80+字段深度分析（周转率/偿债/现金流/资产结构） |
| 东财业绩报表 | 单季EPS/营收/净利/同比/环比 |

### 技术面层（V2.2 新增）

| 端点 | 数据 |
|------|------|
| MA均线 | MA5/10/20/60/120 + 多头/空头排列判断 |
| MACD/RSI/BOLL | 金叉/死叉信号 + 超买超卖 + 布林带 |

### 筹码分布层（V2.3 新增）

| 端点 | 数据 |
|------|------|
| 筹码分布计算 | 获利盘/套牢盘/平均成本/90%集中区/上方抛压/下方支撑/筹码分布图 |
| 资金流向聚合 | 主力/超大单/大单 5/10/20日净流入趋势 |
| 筹码+资金联合 | 双维度综合研判信号 |

### 行业估值对比层（V2.2 新增）

| 端点 | 数据 |
|------|------|
| 同行业PE/PB对比 | 行业均值/中位数 + 个股排名 + 相对偏离度 |

### 鉴权要求

10 个数据源**完全免费无 Key**，仅 iwencai 语义搜索需要 API Key（[申请地址](https://www.iwencai.com/skillhub)）。

---

## 使用示例

跟你的 AI 助手说这些话就能激活：

| 场景 | 说什么 |
|------|--------|
| 个股估值 | 「帮我估一下 688017，给我 PE / PEG / 消化时间」 |
| 题材归因 | 「今天哪些股票走强，主要是什么题材」 |
| 研报检索 | 「人形机器人产业链最近的研报，特别是丝杠和减速器」 |
| 北向资金 | 「今天北向资金流入流出怎么样」 |
| 概念板块 | 「688017 属于哪些概念板块」 |
| 资金流向 | 「000858 今天主力资金流入还是流出」 |
| 龙虎榜 | 「002475 最近上过龙虎榜吗，哪些营业部在买」 |
| 全市场龙虎榜 | 「今天龙虎榜哪些票净买入最多」 |
| 解禁预警 | 「这只股票未来 3 个月有没有限售解禁」 |
| 行业轮动 | 「今天哪些行业涨幅最大，资金在流入哪些板块」 |
| 新闻公告 | 「拉一下 300476 最近的新闻和公告」 |
| 批量对比 | 「帮我对比这 5 只半导体股的估值」 |
| 财务趋势 | 「000537 近3年营收和净利润趋势怎么样」 |
| 技术面 | 「000537 现在技术面怎么样，MACD和均线如何」 |
| 行业估值 | 「000537 在电力行业里PE算贵还是便宜」 |
| 筹码分布 | 「002281 筹码分布怎么样，获利盘多少，上方抛压重不重」 |
| 筹码+资金 | 「帮我分析下002281的筹码和资金流向」 |

### 内置 4 套调研流程

| 流程 | 做什么 | 耗时 |
|------|--------|------|
| 单票估值 | 实时价 → 一致预期 EPS → 前向 PE / PEG / PE 消化年数 | 30 秒 |
| 批量对比 | 多只股票横向估值排列 | 1 分钟 |
| 主题研报 | iwencai 多关键词 NL 搜索 + 东财 PDF 交叉补充 | 2 分钟 |
| 新标的调研 | 机构覆盖 → 估值 → 财务趋势 → 技术面 → 筹码 → 行业对比 → 概念板块 → 资金流向 → 龙虎榜 → 解禁预警 | 1 分钟 |

---

## 版本演进

| 版本 | 新增能力 |
|------|---------|
| V2.3 | 筹码分布层（获利盘/套牢盘/平均成本/抛压支撑/筹码分布图 + 资金流向聚合） |
| V2.2 | 财务趋势层 + 技术面层 + 行业估值对比层 |
| V2.1 | 龙虎榜席位 + 全市场龙虎榜 + 限售解禁 + 行业横向 + 百度概念板块 + 百度资金流向 + 北向自缓存 + F10截断 |
| V1.0 | 行情层 + 研报层 + 信号层 + 新闻层 + 基础数据层 + 公告层 |

---

## 数据源优先级

| 优先级 | 数据源 | 协议 | 封 IP 风险 |
|--------|--------|------|-----------|
| 1 | mootdx | TCP (7709) | 极低 |
| 2 | 腾讯财经 | HTTP | 低 |
| 3 | akshare | Python | 中（东财源） |
| 4 | iwencai | OpenAPI | 低（需 Key） |
| 5 | 东财 PDF | HTTP | 低 |
| 6 | 同花顺热点 | HTTP | 极低（零鉴权） |
| 7 | 同花顺北向 | HTTP | 极低（零鉴权） |
| 8 | 百度股市通 | HTTP | 极低（零鉴权） |
| 9 | 同花顺 THS | HTTP | 极低 |
| 10 | stockstats | 本地计算 | 无 |
| 11 | 筹码分布算法 | 本地计算 | 无 |

---

## FAQ

**Q: mootdx 和腾讯有什么区别？**
互补。mootdx = 交易层（价格 + 盘口 + K 线），腾讯 = 估值层（PE / PB / 市值 / 换手率 / 涨跌停价）。两者都不封 IP。

**Q: 在海外服务器跑，mootdx 超时？**
mootdx 走 TCP 直连通达信行情服务器，需国内 IP 才稳定。海外环境建议走代理或切换到 yfinance。

**Q: 腾讯 API 字段 43 是 PB 吗？**
不是。43 = 振幅%，46 = PB。网上大量教程写错了，这里是实测校准结果。

**Q: akshare 报超时？**
东财源有反爬，加 `time.sleep(1~3)` 重试。行情请走 mootdx，不受影响。

**Q: iwencai 返回 401？**
检查：(1) API Key 有效性 (2) 是否携带了 X-Claw-* Headers。SkillHub 2.0 后强制要求。

**Q: 同花顺热点 reason 字段为空？**
盘后数据还没更新，15:30 之后再调。个别 ST 股没有人工标注，`dropna` 过滤即可。

**Q: 百度股市通 ResultCode 不稳定？**
已知坑——有时返回 int `0`，有时返回 string `"0"`。代码里用 `str()` 统一比较即可。

**Q: 北向资金历史只有几天？**
V2.1 改为本地自缓存。每次调用自动积累，越跑越丰富。首次运行只有当天数据。

**Q: 筹码分布准确吗？**
采用"指数衰减+日内均匀分布"近似算法（60日半衰期），与通达信结果在大方向一致（获利盘误差通常<5%），但具体价位占比可能有差异。半衰期可调：短线30天，长线90天。

**Q: 不用 Claude Code，能用吗？**
能。SKILL.md 本质是 Markdown + 内嵌 Python 代码。Codex、OpenClaw 或任何 AI 编程助手都能读取。你也可以直接把 Python 代码段复制出来在自己的脚本里跑。

---

## 更新日志

见 [CHANGELOG.md](./CHANGELOG.md)。

---

## Disclaimer

本项目仅提供数据获取工具，不构成任何投资建议。股市有风险，投资需谨慎。

---

## License

[Apache License 2.0](./LICENSE) — 自由使用，注明出处即可。

**作者：** Simon 林 · 抖音「Simon林」 · 公众号「硅基世纪」

---

<details>
<summary><b>🇬🇧 English</b></summary>

# a-stock-data

Full-stack data toolkit for China A-Share market — 10-layer architecture · 29 endpoints · 11 data sources, battle-tested

A self-contained Skill file that consolidates raw A-share data from 11 sources into a ready-to-use toolkit for AI coding assistants. No need to memorize mootdx candlestick parameters, Eastmoney PDF Referer headers, iwencai X-Claw authentication, or Baidu PAE header assembly — it's all handled.

> Compatible with [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://github.com/openai/codex) · [OpenClaw](https://github.com/anthropics/openclaw)
>
> The Skill file is structured Markdown + embedded Python. Any AI coding assistant with context injection can use it.

---

## Architecture

```
China A-Share Full-Stack Data · 10-Layer Architecture
│
├── Market Data        mootdx + Tencent Finance     Candlesticks + Order Book + PE/PB/Market Cap/Limits
├── Research           Eastmoney + akshare + iwencai Report list / PDF download / Consensus EPS / NL search
├── Signals            THS + Baidu + akshare + EM    Hot stocks + Attribution + Northbound + Concepts
│                                                  + Fund flow + Dragon Tiger + Lockup + Industry
├── News               akshare × 3                   Stock news / CLS flash / Global finance
├── Fundamentals       mootdx finance / F10          37-field quarterly + 9 categories company data
├── Financial Trend    THS + Eastmoney               3yr revenue/profit/ROE/margin trends + 80+ deep metrics (V2.2)
├── Technical          mootdx + stockstats            MA5/10/20/60/120 + MACD/RSI/BOLL + trend signals (V2.2)
├── Chip Distribution  mootdx + decay algorithm      Profit/loss % / avg cost / 90% range / pressure/support + fund flow (V2.3)
├── Industry Valuation THS industry + Tencent batch   Peer PE/PB mean/median + ranking + deviation (V2.2)
└── Filings            cninfo + mootdx               Full filings across SSE / SZSE / BSE
```

---

## Quick Start

**3 steps, 2 minutes.**

```bash
# 1. Create skill directory
mkdir -p ~/.claude/skills/a-stock-data

# 2. Download SKILL.md
curl -o ~/.claude/skills/a-stock-data/SKILL.md \
  https://raw.githubusercontent.com/simonlin1212/a-stock-data/main/SKILL.md

# 3. Install dependencies
pip install mootdx akshare requests pandas stockstats

# 4. (Optional) Verify environment
python check_env.py
```

Launch Claude Code and say "Check the valuation of 688017" — the skill activates automatically.

> **Codex / OpenClaw users:** Paste the contents of SKILL.md into your system prompt or project context file. The embedded Python code is ready to execute.

---

## Version History

| Version | New Capabilities |
|---------|-----------------|
| V2.3 | Chip distribution layer (profit/loss %, avg cost, pressure/support + fund flow aggregation) |
| V2.2 | Financial trend layer + Technical analysis layer + Industry valuation comparison |
| V2.1 | Dragon Tiger + Full market DT + Lockup + Industry comparison + Baidu concepts/funds + Northbound cache + F10 truncation |
| V1.0 | Market data + Research + Signals + News + Fundamentals + Filings |

---

## Disclaimer

This project provides data access tools only and does not constitute investment advice. Investing involves risk.

---

## License

[Apache License 2.0](./LICENSE)

**Author:** Simon Lin · TikTok [@simonlin121212](https://www.tiktok.com/@simonlin121212) · Douyin "Simon林" · WeChat Official Account "硅基世纪"

</details>

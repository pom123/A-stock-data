---
name: a-stock-data
description: A股全栈数据工具包 — 覆盖行情(mootdx+腾讯)、研报(东财+iwencai)、信号(同花顺热点+北向+百度PAE+龙虎榜+解禁+行业)、新闻(akshare)、基础数据(mootdx财务/F10)、财务趋势(同花顺多期)、技术面(MA/MACD/RSI/BOLL)、筹码分布(获利盘/套牢盘/平均成本/抛压支撑)、行业估值对比(同花顺行业+腾讯批量)、公告(巨潮)十层数据源，内嵌全部调用代码，自包含零依赖外部文件。适用于个股估值、研报检索、题材归因、龙虎榜跟踪、解禁预警、行业轮动、产业链调研、批量筛选、财务趋势分析、技术面判断、筹码分布分析等场景。
origin: custom
version: 2.3
---

> 📦 项目主页：https://github.com/simonlin1212/a-stock-data — 更新、反馈、支持作者
> 
> 作者：Simon 林 · 抖音「Simon林」· 公众号「硅基世纪」

# A股全栈数据工具包 V2.3

十层数据架构，29 个端点，全部实测可用（2026-05-13 验证，覆盖主板/中小板/科创板/ST）。

> **V2.3 新增**：筹码分布层（mootdx K线 + 指数衰减算法 → 获利盘/套牢盘/平均成本/90%集中区/上方抛压/下方支撑/筹码分布图 + akshare资金流向聚合）
>
> **V2.2 新增**：财务趋势层（近3年营收/净利/增速/ROE/毛利率趋势）+ 技术面层（MA均线/MACD/RSI/BOLL）+ 同行业PE/PB估值对比（同花顺行业成分 + 腾讯批量行情）
>
> **V2.1 新增**：龙虎榜席位 + 全市场龙虎榜 + 限售解禁日历 + 行业横向对比 + 百度股市通（概念板块 / 资金流向）+ 北向自缓存 + F10 截断优化

**使用方式：** 将本文件放入 `~/.claude/skills/a-stock-data/SKILL.md`，Claude Code 会自动识别并在 A 股相关对话中激活。

```
行情层（实时，不封IP）
├── mootdx        → K线 + 五档盘口 + 逐笔成交 (TCP 7709)
└── 腾讯财经 API   → PE/PB/市值/换手率/涨跌停 (HTTP)

研报层
├── 东财 reportapi → 研报列表 + PDF下载 + 评级 + 三年EPS
├── 同花顺 THS     → 一致预期EPS (akshare封装)
└── iwencai        → NL语义搜索研报 (唯一能力，需X-Claw)

信号层（V2 新增 + V2.1 大幅扩展）
├── 同花顺热点     → 当日强势股 + 题材归因 reason tags (零鉴权 73ms)
├── 同花顺北向     → hgt/sgt 分钟资金流向 + 本地自缓存历史 (V2.1 改)
├── 百度股市通     → 概念板块归属 + 个股资金流向 (V2.1 新增)
├── 龙虎榜席位     → 上榜记录 + 买卖席位 TOP5 + 机构动向 (V2.1 新增)
├── 全市场龙虎榜   → 每日全市场上榜股票 + 净买额排名 (V2.1 新增)
├── 限售解禁日历   → 历史解禁 + 未来90天待解禁 (V2.1 新增)
└── 行业横向对比   → 同花顺90行业涨跌排名 (V2.1 新增)

新闻层
├── akshare stock_news_em      → 个股新闻 (东财)
├── akshare stock_info_global_cls   → 财联社快讯
└── akshare stock_info_global_em    → 东财全球资讯

基础数据层
├── mootdx finance → 季报快照 (37字段, EPS/ROE/净利)
├── mootdx F10     → 公司资料 (9大类文本, V2.1 截断优化)
└── akshare        → 个股基本面 (stock_individual_info_em)

财务趋势层（V2.2 新增）
├── 同花顺财务摘要 → 近3年营收/净利/增速/ROE/毛利率多期趋势 (stock_financial_abstract_ths)
├── 东财财务指标   → 80+字段深度分析 (stock_financial_analysis_indicator)
└── 东财业绩报表   → 单季EPS/营收/净利/同比/环比 (stock_yjbb_em)

技术面层（V2.2 新增）
├── mootdx K线     → 120根日K原始数据 (TCP)
└── stockstats     → MA5/10/20/60/120 + MACD/RSI/BOLL 计算

筹码分布层（V2.3 新增）
├── mootdx K线     → 250根日K原始数据 (TCP)
├── 指数衰减算法   → 60日半-life衰减 + 日内均匀分布 → 筹码分布图
├── akshare        → 主力/超大单/大单资金流向 (stock_individual_fund_flow)
└── 聚合输出       → 获利盘% / 套牢盘% / 平均成本 / 90%集中区 / 上方抛压 / 下方支撑 / 筹码分布图 / 5-20日资金流向

行业估值对比层（V2.2 新增）
├── 同花顺行业列表 → 90行业名称+代码 (stock_board_industry_name_ths)
├── 同花顺行业信息 → 板块涨幅/资金净流入/涨跌家数 (stock_board_industry_info_ths)
└── 腾讯批量行情   → 同行业个股PE/PB → 算行业均值/中位数/排名

公告层
├── 巨潮 cninfo    → 公告全文 (akshare封装)
└── mootdx F10     → 最新公告摘要
```

## When to Activate

- 用户要查 A 股个股估值（一致预期 / PE / PEG / PE消化）
- 用户要拉实时行情（价格 / 五档盘口 / K线 / 涨跌停价）
- 用户要搜研报（按主题 / 按标的 / 按行业 / 下载PDF）
- 用户要看**当日强势股 / 题材归因 / 概念热点**
- 用户要看**北向资金动向**（沪股通/深股通分钟流向）
- 用户要看**概念板块归属**（行业/概念/地域）
- 用户要看**个股资金流向**（主力/散户/超大单/大单分钟级）
- 用户要看**龙虎榜席位**（营业部 + 机构买卖）
- 用户要看**全市场龙虎榜**（当日所有上榜股票 + 净买额排名）
- 用户要看**限售解禁日历**（历史解禁 + 未来待解禁）
- 用户要做**行业横向对比**（涨跌排名 / 资金流入 / 领涨股）
- 用户要看新闻资讯（个股新闻 / 财联社快讯 / 全球资讯）
- 用户要查公告（巨潮公告全文）
- 用户要做产业链调研 / 批量横向对比
- 用户要看**财务趋势**（近3年营收/净利/增速/ROE/毛利率）
- 用户要看**技术面**（均线MA/MACD/RSI/BOLL/买卖时机）
- 用户要做**同行业估值对比**（行业PE/PB均值/中位数/个股排名）
- 用户要看**筹码分布**（获利盘/套牢盘/平均成本/上方抛压/下方支撑/筹码分布图）
- 用户要看**筹码+资金联合分析**（筹码面+主力资金流向双维度评估）
- 关键词：估值、一致预期、机构预测、市盈率、PEG、市值、研报、产业链、行业研究、K线、盘口、公告、新闻、**强势股、题材、热点、概念归因、北向资金、沪股通、深股通、概念板块、资金流向、主力、龙虎榜、席位、营业部、全市场龙虎榜、净买入、解禁、限售、行业对比、行业轮动、财务趋势、营收、净利润、增速、ROE、毛利率、均线、MACD、RSI、BOLL、买卖时机、技术面、筹码、筹码分布、获利盘、套牢盘、平均成本、抛压、支撑位**

### 快捷使用场景

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

---

## Prerequisites

```bash
pip install mootdx akshare requests pandas stockstats
```

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| mootdx | >= 0.10 | TCP行情+财务+F10 |
| akshare | >= 1.10 | 研报/新闻/公告/一致预期/龙虎榜/解禁/行业 |
| requests | any | 腾讯API+东财PDF+百度PAE+同花顺 |
| pandas | any | 数据处理 |
| stockstats | any | 技术指标计算（RSI/MACD/BOLL等） |

### iwencai API Key（仅语义搜索需要）

```bash
# 环境变量方式
export IWENCAI_API_KEY="your_key_here"
export IWENCAI_BASE_URL="https://openapi.iwencai.com"

# 申请地址: https://www.iwencai.com/skillhub
# 注册后安装 SkillHub CLI，再安装 report-search 技能即可获得 Key
```

其他数据源（mootdx / 腾讯 / akshare / 巨潮 / 同花顺 / 百度股市通）全部免费，无需 key。

### 市场前缀规则（全局通用）

```python
def get_prefix(code: str) -> str:
    """6位代码 → 市场前缀"""
    if code.startswith(("6", "9")):
        return "sh"
    elif code.startswith("8"):
        return "bj"
    else:
        return "sz"
```

### Ticker 格式归一化

所有接口统一支持多种输入格式，内部归一化为纯 6 位数字：

| 输入 | 归一化结果 |
|------|-----------|
| `688017` | `688017` |
| `SH688017` / `sh688017` | `688017` |
| `688017.SH` / `688017.sh` | `688017` |
| `SZ000001` | `000001` |
| `BJ832000` | `832000` |

---

## Layer 1: 行情层（实时，不封IP）

### 1.1 mootdx — K线 + 五档盘口 + 逐笔成交

TCP 二进制协议，连通达信服务器(7709)，无需注册，不封IP。

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')

# === K线数据 ===
# market: 0=深圳, 1=上海
# category: 4=日线, 5=周线, 6=月线, 7=1分钟, 8=5分钟, 9=15分钟, 10=30分钟, 11=60分钟
klines = client.bars(symbol='688017', category=4, offset=10)
# 返回: open, close, high, low, vol, amount, datetime

# === 实时报价 ===
quotes = client.quotes(symbol=['688017', '300476'])
# 返回 46 个字段:
#   price(现价), open, high, low, last_close(昨收)
#   bid1~bid5, ask1~ask5, bid_vol1~bid_vol5, ask_vol1~ask_vol5
#   vol(成交量), amount(成交额), servertime

# === 逐笔成交（非交易时间返回空）===
trades = client.transaction(symbol='688017', date='20260502')
# 返回: time, price, vol, num, buyorsell(0买/1卖/2中性)
```

**mootdx 不提供 PE / PB / 市值 / 换手率 / 涨跌停价** — 这些走腾讯财经。

### 1.2 腾讯财经 API — PE/PB/市值/换手率/涨跌停

HTTP GET，GBK 编码，`~` 分隔 88 个字段，不封IP。

```python
import urllib.request

def tencent_quote(codes: list[str]) -> dict[str, dict]:
    """
    批量拉取腾讯财经实时行情。
    codes: ["688017", "300476", "002463"]
    返回: {code: {name, price, pe_ttm, pb, mcap, ...}}
    """
    prefixed = []
    for c in codes:
        if c.startswith(("6", "9")):
            prefixed.append(f"sh{c}")
        elif c.startswith("8"):
            prefixed.append(f"bj{c}")
        else:
            prefixed.append(f"sz{c}")

    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode("gbk")

    result = {}
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 53:
            continue
        code = key[2:]
        result[code] = {
            "name":         vals[1],
            "price":        float(vals[3]) if vals[3] else 0,
            "last_close":   float(vals[4]) if vals[4] else 0,
            "open":         float(vals[5]) if vals[5] else 0,
            "change_amt":   float(vals[31]) if vals[31] else 0,
            "change_pct":   float(vals[32]) if vals[32] else 0,
            "high":         float(vals[33]) if vals[33] else 0,
            "low":          float(vals[34]) if vals[34] else 0,
            "amount_wan":   float(vals[37]) if vals[37] else 0,
            "turnover_pct": float(vals[38]) if vals[38] else 0,
            "pe_ttm":       float(vals[39]) if vals[39] else 0,
            "amplitude_pct":float(vals[43]) if vals[43] else 0,
            "mcap_yi":      float(vals[44]) if vals[44] else 0,
            "float_mcap_yi":float(vals[45]) if vals[45] else 0,
            "pb":           float(vals[46]) if vals[46] else 0,
            "limit_up":     float(vals[47]) if vals[47] else 0,
            "limit_down":   float(vals[48]) if vals[48] else 0,
            "vol_ratio":    float(vals[49]) if vals[49] else 0,
            "pe_static":    float(vals[52]) if vals[52] else 0,
        }
    return result

# 用法
quotes = tencent_quote(["688017", "300476", "002463"])
for code, q in quotes.items():
    print(f"{q['name']}({code}): {q['price']}元 PE={q['pe_ttm']} PB={q['pb']} 市值={q['mcap_yi']}亿")
```

#### 腾讯财经字段索引速查（实测校准 2026-05-03）

| 索引 | 含义 | 示例 |
|------|------|------|
| 1 | 名称 | 绿的谐波 |
| 3 | 当前价 | 224.12 |
| 4 | 昨收 | 215.01 |
| 5 | 今开 | 214.10 |
| 9-18 | 买一~买五(价+量) | |
| 19-28 | 卖一~卖五(价+量) | |
| 31 | 涨跌额 | 9.11 |
| 32 | 涨跌幅% | 4.24 |
| 33 | 最高 | 229.62 |
| 34 | 最低 | 214.10 |
| 37 | 成交额(万) | 187040 |
| 38 | 换手率% | 4.55 |
| **39** | **PE(TTM)** | 300.45 |
| **43** | **振幅%（不是PB！）** | 7.22 |
| **44** | **总市值(亿)** | 410.88 |
| **45** | **流通市值(亿)** | 410.88 |
| **46** | **PB(市净率)** | 11.51 |
| **47** | **涨停价** | 258.01 |
| **48** | **跌停价** | 172.01 |
| 49 | 量比 | 1.20 |
| **52** | **PE(静)** | 314.76 |

> **踩坑提醒：** 网上很多教程把索引 43 写成 PB，实测是振幅%。PB 在索引 46。

---

## Layer 2: 研报层

### 2.1 东财研报 API — 研报列表 + PDF下载（主力）

A级接口（公开JSON API），reportapi.eastmoney.com，免费无key。

```python
import requests
import re
import time
from pathlib import Path

REPORT_API = "https://reportapi.eastmoney.com/report/list"
PDF_TPL = "https://pdf.dfcfw.com/pdf/H3_{info_code}_1.pdf"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def eastmoney_reports(code: str, max_pages: int = 5) -> list[dict]:
    """拉取指定股票的研报列表"""
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Referer": "https://data.eastmoney.com/"})
    all_records = []
    for page in range(1, max_pages + 1):
        params = {
            "industryCode": "*", "pageSize": "100", "industry": "*",
            "rating": "*", "ratingChange": "*",
            "beginTime": "2000-01-01", "endTime": "2030-01-01",
            "pageNo": str(page), "fields": "", "qType": "0",
            "orgCode": "", "code": code, "rcode": "",
            "p": str(page), "pageNum": str(page), "pageNumber": str(page),
        }
        r = session.get(REPORT_API, params=params, timeout=30)
        d = r.json()
        rows = d.get("data") or []
        if not rows:
            break
        all_records.extend(rows)
        if page >= (d.get("TotalPage", 1) or 1):
            break
        time.sleep(0.3)
    return all_records

def download_pdf(record: dict, target_dir: str = "./reports") -> str | None:
    """下载单份研报PDF，返回保存路径或None"""
    info_code = record.get("infoCode", "")
    if not info_code:
        return None
    date = (record.get("publishDate") or "")[:10]
    org = record.get("orgSName") or "未知"
    title = re.sub(r'[\\/:*?"<>|]', "_", record.get("title", ""))[:80]
    fname = f"{date}_{org}_{title}.pdf"
    target = Path(target_dir) / fname
    if target.exists():
        return str(target)
    url = PDF_TPL.format(info_code=info_code)
    r = requests.get(url, headers={"User-Agent": UA, "Referer": "https://data.eastmoney.com/"}, timeout=60)
    if r.status_code == 200 and len(r.content) >= 1024:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(r.content)
        return str(target)
    return None

# 用法
reports = eastmoney_reports("688017")
print(f"共 {len(reports)} 篇研报")
for r in reports[:5]:
    print(f"  {r.get('publishDate','')[:10]} | {r.get('orgSName')} | {r.get('title','')[:60]}")
```

#### 研报 record 关键字段

| 字段 | 含义 |
|------|------|
| title | 研报标题 |
| publishDate | 发布日期 |
| orgSName | 机构简称 |
| infoCode | 用于拼 PDF URL |
| predictThisYearEps | 今年EPS预测 |
| predictNextYearEps | 明年EPS预测 |
| predictNextTwoYearEps | 后年EPS预测 |
| emRatingName | 评级(买入/增持/...) |
| indvInduName | 行业分类 |

### 2.2 akshare — 机构一致预期EPS

```python
import akshare as ak

df = ak.stock_profit_forecast_ths(
    symbol="688017",
    indicator="预测年报每股收益"
)
# 返回列: 年度, 预测机构数, 最小值, 均值, 最大值, 行业平均数
# "均值" = 机构一致预期EPS
# "预测机构数" < 3 的要谨慎

# indicator 选项:
# "预测年报每股收益" → EPS共识（最稳定）
# "预测年报净利润"   → 净利润预测
# "预测详细指标"     → 综合维度（有时返回空）
# "业绩预测详表-机构" → 按机构展示
```

### 2.3 iwencai — NL语义搜索研报（唯一能力）

需要 API Key + X-Claw Headers（SkillHub 2.0 强制要求）。

```python
import os
import json
import secrets
import requests

IWENCAI_BASE = os.environ.get("IWENCAI_BASE_URL", "https://openapi.iwencai.com")
IWENCAI_KEY = os.environ.get("IWENCAI_API_KEY", "")

def _claw_headers(call_type: str = "normal") -> dict:
    """SkillHub 2.0 必须的 X-Claw 鉴权头"""
    return {
        "X-Claw-Call-Type": call_type,
        "X-Claw-Skill-Id": "report-search",
        "X-Claw-Skill-Version": "2.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": secrets.token_hex(32),
    }

def iwencai_search(query: str, channel: str = "report", size: int = 50) -> list[dict]:
    """
    iwencai 语义搜索。
    channel: "report"(研报) / "announcement"(公告) / "news"(新闻)
    size: 默认10, 实测可调到50（隐藏参数）
    """
    headers = {
        "Authorization": f"Bearer {IWENCAI_KEY}",
        "Content-Type": "application/json",
        **_claw_headers(),
    }
    payload = {
        "channels": [channel],
        "app_id": "AIME_SKILL",
        "query": query,
        "size": size,
    }
    r = requests.post(
        f"{IWENCAI_BASE}/v1/comprehensive/search",
        json=payload, headers=headers, timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"iwencai HTTP {r.status_code}: {r.text[:200]}")
    data = r.json()
    if data.get("status_code", 0) != 0:
        raise RuntimeError(f"iwencai error: {data.get('status_msg', '')}")
    return data.get("data") or []

def iwencai_query(query: str, page: int = 1, limit: int = 50) -> list[dict]:
    """
    iwencai NL数据查询（结构化字段）。
    例: "贵州茅台 ROE" → DataFrame-like rows
    """
    headers = {
        "Authorization": f"Bearer {IWENCAI_KEY}",
        "Content-Type": "application/json",
        **_claw_headers(),
    }
    payload = {
        "query": query,
        "page": str(page),
        "limit": str(limit),
        "is_cache": "1",
        "expand_index": "true",
    }
    r = requests.post(
        f"{IWENCAI_BASE}/v1/query2data",
        json=payload, headers=headers, timeout=30,
    )
    if r.status_code != 200:
        raise RuntimeError(f"iwencai HTTP {r.status_code}: {r.text[:200]}")
    data = r.json()
    if data.get("status_code", 0) != 0:
        raise RuntimeError(f"iwencai error: {data.get('status_msg', '')}")
    return data.get("datas") or []

def dedup_articles(articles: list[dict]) -> list[dict]:
    """同一uid仅保留score最高的段落"""
    best = {}
    for a in articles:
        uid = a.get("uid", "") or f"{a.get('title','')}|{a.get('publish_date','')}"
        score = float(a.get("score", 0))
        if uid not in best or score > float(best[uid].get("score", 0)):
            best[uid] = a
    return sorted(best.values(), key=lambda x: x.get("publish_date", ""), reverse=True)

# 用法: NL语义搜索研报
articles = iwencai_search("人形机器人 行星滚柱丝杠 2026", channel="report", size=50)
articles = dedup_articles(articles)
for a in articles[:5]:
    extra = a.get("extra") or {}
    if isinstance(extra, str):
        extra = json.loads(extra)
    print(f"{a.get('publish_date','')[:10]} | {extra.get('organization','')} | {a.get('title','')[:60]}")
```

**iwencai 的唯一价值：** NL 主题搜索。"人形机器人 行星滚柱丝杠" 这种跨主题检索只有 iwencai 能做。按标的搜研报走东财 reportapi 更稳定。

---

## Layer 3: 新闻层

### 3.1 个股新闻（akshare → 东财）

```python
import akshare as ak

df = ak.stock_news_em(symbol="688017")
# 返回: 新闻标题, 新闻内容, 发布时间, 文章来源, 新闻链接
# 注意: symbol 传 6 位代码，默认返回最近新闻
```

### 3.2 财联社快讯（akshare）

```python
import akshare as ak

df = ak.stock_info_global_cls()
# 返回: 标题, 内容, 发布时间
# 财联社电报，更新频率极高（分钟级）
```

### 3.3 东财全球资讯（akshare）

```python
import akshare as ak

df = ak.stock_info_global_em()
# 返回: 标题, 摘要, 发布时间, 链接
# 东方财富全球财经资讯
```

---

## Layer 4: 基础数据层

### 4.1 mootdx 财务快照（37字段季报数据）

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')

# market: 0=深圳, 1=上海
fin = client.finance(symbol='688017')
# 返回 37 个字段的季报快照:
#   liutongguben(流通股本), zongguben(总股本)
#   eps(每股收益), bvps(每股净资产), roe(净资产收益率%)
#   profit(净利润), income(主营收入)
#   meigujingzichan(每股净资产), meigugongjijin(每股公积金)
#   meiguweifeipeili(每股未分配利润)
#   等37个季报财务字段
```

### 4.2 mootdx F10（公司文本资料，V2.1 截断优化）

```python
from mootdx.quotes import Quotes

client = Quotes.factory(market='std')

# 9 大类文本数据:
categories = [
    "最新提示", "公司概况", "财务分析",
    "股东研究", "股本结构", "资本运作",
    "业内点评", "行业分析", "公司大事",
]
for cat in categories:
    text = client.F10(symbol='688017', name=cat)
    print(f"=== {cat} ===")
    print(text[:200] if text else "(空)")
```

> **V2.1 优化：** "股东研究" 中的【4.股东变化】章节原始 F10 全文含大量历史十大股东列表（000858 实测 16121 chars，占全文 80%），现只保留最新一期（~2000 chars），优化效果：19969→5906 chars（**-70% token**）。

### 4.3 akshare 个股基本面

```python
import akshare as ak

df = ak.stock_individual_info_em(symbol="688017")
# 返回: 股票代码, 股票简称, 总股本, 流通股, 总市值(元), 流通市值(元), 行业, 上市时间
# 注意: 市值单位是"元"不是亿元
# 返回格式是 2 列 DataFrame (item / value)
```

---

## Layer 5: 财务趋势层（V2.2 新增）

> **核心价值：** mootdx finance 只返回最近一季快照，无法看趋势。这层补上多期财务数据，判断增长质量。

### 5.1 同花顺财务摘要 — 近3年营收/净利/增速/ROE/毛利率

```python
import akshare as ak

def financial_trend(code: str, years: int = 3) -> list[dict]:
    """
    近 N 年年报财务趋势（营收/净利/增速/ROE/毛利率）。
    数据源: 同花顺 financial_abstract_ths
    """
    df = ak.stock_financial_abstract_ths(symbol=code)
    if df.empty:
        return []

    # 筛选年报（12-31），取最近 N 年
    df_annual = df[df['报告期'].str.contains('12-31')].head(years)

    result = []
    for _, row in df_annual.iterrows():
        result.append({
            "date": row['报告期'],
            "revenue": row['营业总收入'],           # 如 "36.91亿"
            "revenue_yoy": row['营业总收入同比增长率'], # 如 "7.60%"
            "net_profit": row['净利润'],
            "net_profit_yoy": row['净利润同比增长率'],
            "deducted_net_profit": row['扣非净利润'],
            "deducted_yoy": row['扣非净利润同比增长率'],
            "eps": row['基本每股收益'],
            "bvps": row['每股净资产'],
            "ocf_per_share": row['每股经营现金流'],
            "net_margin": row['销售净利率'],
            "gross_margin": row['销售毛利率'],
            "roe": row['净资产收益率'],
            "roe_diluted": row['净资产收益率-摊薄'],
            "debt_ratio": row['资产负债率'],
        })
    return result

# 用法
trend = financial_trend("000537", 3)
for t in trend:
    print(f"{t['date']}: 营收={t['revenue']} (+{t['revenue_yoy']}) | "
          f"净利={t['net_profit']} (+{t['net_profit_yoy']}) | "
          f"ROE={t['roe']} 毛利率={t['gross_margin']}")
```

#### 财务趋势字段速查

| 字段 | 含义 | 示例 |
|------|------|------|
| 营业总收入 | 含税营收 | 36.91亿 |
| 营业总收入同比增长率 | 营收增速 | 7.60% |
| 净利润 | 归母净利润 | 9.20亿 |
| 净利润同比增长率 | 净利增速 | 45.14% |
| 扣非净利润 | 扣非后净利 | 8.50亿 |
| 基本每股收益 | EPS | 0.48 |
| 销售净利率 | 净利率 | 24.9% |
| 销售毛利率 | 毛利率 | 53.54% |
| 净资产收益率 | ROE | 5.48% |
| 每股经营现金流 | 经营质量 | 0.90 |
| 资产负债率 | 杠杆率 | 68.02% |

> **数据覆盖：** 1993年至今所有年报 + 半年报，共 ~114 行。早期数据部分字段为 `False`（未披露）。

### 5.2 东财财务指标 — 80+字段深度分析

```python
import akshare as ak

def financial_indicators(code: str, start_year: str = "2023") -> list[dict]:
    """
    东财财务分析指标，80+字段深度分析。
    含: 周转率/偿债能力/现金流/资产结构 等
    """
    df = ak.stock_financial_analysis_indicator(symbol=code, start_year=start_year)
    if df.empty:
        return []
    # 关键字段（列名示例，实际80+列）
    key_cols = ['日期', '摊薄每股收益(元)', '加权每股收益(元)',
                '每股经营性现金流(元)', '净资产收益率(%)',
                '销售毛利率(%)', '销售净利率(%)',
                '应收账款周转率(次)', '存货周转率(次)',
                '流动比率', '速动比率', '资产负债率(%)']
    available = [c for c in key_cols if c in df.columns]
    return df[available].to_dict('records')

# 用法
indicators = financial_indicators("000537", "2023")
for ind in indicators:
    print(f"{ind.get('日期','')}: ROE={ind.get('净资产收益率(%)','')} "
          f"毛利率={ind.get('销售毛利率(%)','')}")
```

> **注意：** 此接口较慢（~3秒），字段名含中文和单位，需按实际返回列名取值。

### 5.3 东财业绩报表 — 单季EPS/营收/净利/同比/环比

```python
import akshare as ak

def quarterly_report(code: str, date: str = "20250331") -> dict:
    """
    东财单季业绩报表。
    date: 报告期 YYYYMMDD
    """
    df = ak.stock_yjbb_em(date=date)
    if df.empty:
        return {}
    row = df[df['股票代码'] == code]
    if row.empty:
        return {}
    r = row.iloc[0]
    return {
        "code": r['股票代码'],
        "name": r['股票简称'],
        "eps": r['每股收益'],
        "revenue": r['营业总收入-营业总收入'],
        "revenue_yoy": r['营业总收入-同比增长'],
        "revenue_qoq": r['营业总收入-季度环比增长'],
        "net_profit": r['净利润-净利润'],
        "net_profit_yoy": r['净利润-同比增长'],
        "net_profit_qoq": r['净利润-季度环比增长'],
        "bvps": r['每股净资产'],
        "roe": r['净资产收益率'],
        "ocf_ps": r['每股经营现金流量'],
        "gross_margin": r['销售毛利率'],
        "industry": r['所处行业'],
    }

# 用法
report = quarterly_report("000537", "20250331")
if report:
    print(f"{report['name']}: EPS={report['eps']} "
          f"营收同比={report['revenue_yoy']}% 净利同比={report['net_profit_yoy']}%")
```

> **批量拉多个季度：** 循环调不同 date 即可，如 `["20241231", "20240930", "20240630", "20240331"]`。

---

## Layer 6: 技术面层（V2.2 新增）

> **核心价值：** 用 mootdx K线 + stockstats 计算技术指标，判断买卖时机。

### 6.1 MA均线 + MACD + RSI + BOLL

```python
from mootdx.quotes import Quotes
from stockstats import StockDataFrame
import pandas as pd

def technical_analysis(code: str, offset: int = 120) -> dict:
    """
    技术面分析：MA均线 + MACD + RSI + BOLL。
    offset: K线根数，120≈半年
    """
    client = Quotes.factory(market='std')
    klines = client.bars(symbol=code, category=4, offset=offset)
    if klines is None or klines.empty:
        return {}

    df = pd.DataFrame(klines)
    sdf = StockDataFrame.retype(df)

    # MACD
    macd_val = sdf['macd'].iloc[-1]
    signal_val = sdf['macds'].iloc[-1]
    hist_val = sdf['macdh'].iloc[-1]

    # RSI
    rsi_val = sdf['rsi_14'].iloc[-1]

    # BOLL
    boll_ub = sdf['boll_ub'].iloc[-1] if 'boll_ub' in sdf.columns else None
    boll_lb = sdf['boll_lb'].iloc[-1] if 'boll_lb' in sdf.columns else None

    # MA均线
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    df['ma120'] = df['close'].rolling(120).mean()

    price = df['close'].iloc[-1]

    # 均线多头/空头排列判断
    ma_list = [df['ma5'].iloc[-1], df['ma10'].iloc[-1], df['ma20'].iloc[-1], df['ma60'].iloc[-1]]
    is_bullish_alignment = all(ma_list[i] > ma_list[i+1] for i in range(len(ma_list)-1) if pd.notna(ma_list[i]) and pd.notna(ma_list[i+1]))
    is_bearish_alignment = all(ma_list[i] < ma_list[i+1] for i in range(len(ma_list)-1) if pd.notna(ma_list[i]) and pd.notna(ma_list[i+1]))

    # MACD金叉/死叉
    hist_prev = sdf['macdh'].iloc[-2] if len(sdf) > 1 else 0
    is_golden_cross = hist_prev < 0 and hist_val > 0
    is_death_cross = hist_prev > 0 and hist_val < 0

    return {
        "price": round(price, 2),
        "ma5": round(df['ma5'].iloc[-1], 2) if pd.notna(df['ma5'].iloc[-1]) else None,
        "ma10": round(df['ma10'].iloc[-1], 2) if pd.notna(df['ma10'].iloc[-1]) else None,
        "ma20": round(df['ma20'].iloc[-1], 2) if pd.notna(df['ma20'].iloc[-1]) else None,
        "ma60": round(df['ma60'].iloc[-1], 2) if pd.notna(df['ma60'].iloc[-1]) else None,
        "ma120": round(df['ma120'].iloc[-1], 2) if pd.notna(df['ma120'].iloc[-1]) else None,
        "macd": round(macd_val, 4),
        "macd_signal": round(signal_val, 4),
        "macd_hist": round(hist_val, 4),
        "rsi14": round(rsi_val, 2),
        "boll_ub": round(boll_ub, 2) if boll_ub and pd.notna(boll_ub) else None,
        "boll_lb": round(boll_lb, 2) if boll_lb and pd.notna(boll_lb) else None,
        "is_bullish_alignment": is_bullish_alignment,
        "is_bearish_alignment": is_bearish_alignment,
        "is_golden_cross": is_golden_cross,
        "is_death_cross": is_death_cross,
        "trend_signal": _trend_signal(price, df, is_bullish_alignment, is_bearish_alignment,
                                       is_golden_cross, is_death_cross, rsi_val),
    }

def _trend_signal(price, df, is_bull, is_bear, golden, death, rsi) -> str:
    """综合趋势信号"""
    signals = []
    if is_bull:
        signals.append("均线多头排列(看多)")
    if is_bear:
        signals.append("均线空头排列(看空)")
    if golden:
        signals.append("MACD金叉(买入信号)")
    if death:
        signals.append("MACD死叉(卖出信号)")
    if rsi > 70:
        signals.append(f"RSI={rsi:.0f}超买(注意回调)")
    elif rsi < 30:
        signals.append(f"RSI={rsi:.0f}超卖(关注反弹)")
    if price > df['ma20'].iloc[-1]:
        signals.append("站上20日线")
    else:
        signals.append("跌破20日线")
    return " | ".join(signals) if signals else "中性"

# 用法
tech = technical_analysis("000537")
print(f"现价={tech['price']} MA20={tech['ma20']} MA60={tech['ma60']}")
print(f"MACD={tech['macd']} Signal={tech['macd_signal']} Hist={tech['macd_hist']}")
print(f"RSI14={tech['rsi14']} BOLL={tech['boll_ub']}/{tech['boll_lb']}")
print(f"信号: {tech['trend_signal']}")
```

#### 技术面信号解读

| 信号 | 含义 | 操作建议 |
|------|------|----------|
| 均线多头排列 | MA5>MA10>MA20>MA60 | 趋势向上，持股 |
| 均线空头排列 | MA5<MA10<MA20<MA60 | 趋势向下，观望 |
| MACD金叉 | DIF上穿DEA | 买入信号 |
| MACD死叉 | DIF下穿DEA | 卖出信号 |
| RSI>70 | 超买 | 注意回调风险 |
| RSI<30 | 超卖 | 关注反弹机会 |
| 站上/跌破20日线 | 短期趋势分水岭 | 多空分界线 |

> **筹码分布：** 见下方 Layer 6.5 筹码分布层，已实现本地计算（mootdx K线 + 指数衰减算法）。

---

## Layer 6.5: 筹码分布层（V2.3 新增）

> **核心价值：** 通达信/同花顺的筹码分布是客户端本地计算，无公开API。本层用 mootdx K线数据 + 指数衰减算法在本地复现筹码分布，可输出获利盘/套牢盘比例、平均成本、90%筹码集中区、上方抛压位、下方支撑位、筹码分布图。同时聚合 akshare 资金流向数据，一次调用完成"筹码+资金"双维度分析。

### 6.5.1 筹码分布计算（指数衰减算法）

**算法原理：**
1. 取最近250个交易日K线（mootdx TCP）
2. 每根K线的成交量均匀分布在当日最高价~最低价区间
3. 时间衰减：距今天数越远的K线权重越低，半衰期60天（即60天前的成交量权重减半）
4. 衰减公式：`decay = exp(-ln(2) * days_ago / 60)`
5. 累加所有价位的衰减后成交量，得到筹码分布

```python
from mootdx.quotes import Quotes
import numpy as np

def chip_distribution(code: str, offset: int = 250, half_life: int = 60) -> dict:
    """
    筹码分布分析（指数衰减算法）。
    
    code: 6位股票代码
    offset: K线根数，250≈一年
    half_life: 衰减半衰期（天），默认60
    
    返回: {
        price, avg_cost, deviation_pct, profit_pct, loss_pct,
        pct90_low, pct90_high, pressure_price, pressure_ratio, above_total,
        support_price, support_ratio, below_total,
        chip_chart: [{price, pct}],  # 筹码分布图数据
        avg_5d, avg_20d, avg_60d, dev_5d, dev_20d, dev_60d,
    }
    """
    client = Quotes.factory(market='std')
    k = client.bars(symbol=code, category=4, offset=offset)
    if k is None or k.empty:
        return {}
    
    cp = float(k['close'].iloc[-1])
    chip = {}
    td = len(k)
    
    for idx in range(td):
        row = k.iloc[idx]
        da = td - idx - 1  # 距今天数
        decay = float(np.exp(-np.log(2) * da / half_life))
        lo = int(row['low'])
        hi = int(row['high'])
        vol = float(row['vol'])
        nb = max(hi - lo, 1)  # 价格区间内价位数
        vpb = vol * decay / nb  # 每个价位的衰减成交量
        for p in range(lo, hi + 1):
            chip[p] = chip.get(p, 0) + vpb
    
    tc = sum(chip.values())  # 总筹码量
    wa = sum(p * v for p, v in chip.items()) / tc  # 加权平均成本
    
    # 获利盘/套牢盘
    profit_vol = sum(v for p, v in chip.items() if p < cp)
    profit_pct = profit_vol / tc * 100
    loss_pct = 100 - profit_pct
    
    # 90%筹码集中区
    cum = 0
    p5 = p95 = None
    for p in sorted(chip.keys()):
        cum += chip[p]
        if p5 is None and cum / tc >= 0.05:
            p5 = p
        if cum / tc >= 0.95:
            p95 = p
            break
    
    # 上方抛压位（当前价以上最大筹码峰）
    above = {p: v for p, v in chip.items() if p > int(cp)}
    below = {p: v for p, v in chip.items() if p < int(cp)}
    
    pressure_price = pressure_ratio = above_total = None
    if above:
        mp = max(above, key=above.get)
        above_total = sum(above.values()) / tc * 100
        pressure_price = mp
        pressure_ratio = above[mp] / tc * 100
    
    # 下方支撑位（当前价以下最大筹码峰）
    support_price = support_ratio = below_total = None
    if below:
        ms = max(below, key=below.get)
        below_total = sum(below.values()) / tc * 100
        support_price = ms
        support_ratio = below[ms] / tc * 100
    
    # 筹码分布图数据（价格 vs 占比%）
    max_vol = max(chip.values())
    chip_chart = []
    for bk in sorted(chip.keys()):
        vol2 = chip[bk]
        pct = vol2 / tc * 100
        bar_len = int(vol2 / max_vol * 30)
        is_current = abs(bk - round(cp)) < 1
        chip_chart.append({
            "price": bk,
            "pct": round(pct, 1),
            "bar_len": bar_len,
            "is_current_price": is_current,
        })
    
    # 均价偏离
    avg_data = {}
    for days, label in [(5, '5d'), (20, '20d'), (60, '60d')]:
        tail = k.tail(days)
        avg = (tail['close'] * tail['vol']).sum() / tail['vol'].sum()
        dev = (cp / avg - 1) * 100
        avg_data[f'avg_{label}'] = round(avg, 2)
        avg_data[f'dev_{label}'] = round(dev, 1)
    
    return {
        "price": round(cp, 2),
        "avg_cost": round(wa, 2),
        "deviation_pct": round((cp / wa - 1) * 100, 1),
        "profit_pct": round(profit_pct, 1),
        "loss_pct": round(loss_pct, 1),
        "pct90_low": p5,
        "pct90_high": p95,
        "pressure_price": pressure_price,
        "pressure_ratio": round(pressure_ratio, 1) if pressure_ratio else None,
        "above_total": round(above_total, 1) if above_total else None,
        "support_price": support_price,
        "support_ratio": round(support_ratio, 1) if support_ratio else None,
        "below_total": round(below_total, 1) if below_total else None,
        "chip_chart": chip_chart,
        **avg_data,
    }

# 用法
result = chip_distribution("002281")
print(f"当前价: {result['price']}")
print(f"平均成本: {result['avg_cost']} (偏离{result['deviation_pct']}%)")
print(f"获利盘: {result['profit_pct']}%  套牢盘: {result['loss_pct']}%")
print(f"90%筹码集中区: {result['pct90_low']}~{result['pct90_high']}")
print(f"上方抛压: {result['pressure_price']}元(占比{result['pressure_ratio']}%) 合计{result['above_total']}%")
print(f"下方支撑: {result['support_price']}元(占比{result['support_ratio']}%) 合计{result['below_total']}%")
print(f"5日均价={result['avg_5d']}(偏离{result['dev_5d']}%) 20日均价={result['avg_20d']}(偏离{result['dev_20d']}%)")
```

#### 打印筹码分布图

```python
def print_chip_chart(result: dict):
    """打印终端筹码分布图（价格 vs 筹码占比柱状图）"""
    if not result or not result.get("chip_chart"):
        print("无筹码数据")
        return
    
    cp = result['price']
    print(f"\n筹码分布图（当前价={cp}）：")
    print("-" * 60)
    for item in result['chip_chart']:
        bar = chr(9608) * item['bar_len']
        marker = " <=" if item['is_current_price'] else ""
        print("%5d | %5.1f%% | %s%s" % (item['price'], item['pct'], bar, marker))
    print("-" * 60)
    print(f"上方抛压位: {result['pressure_price']}元 (占比{result['pressure_ratio']}%) 上方合计{result['above_total']}%")
    print(f"下方支撑位: {result['support_price']}元 (占比{result['support_ratio']}%) 下方合计{result['below_total']}%")

# 用法
print_chip_chart(result)
```

### 6.5.2 资金流向聚合（akshare）

```python
import akshare as ak
import pandas as pd

def fund_flow_analysis(code: str, market: str = None, days: list = [5, 10, 20]) -> dict:
    """
    个股资金流向分析（主力/超大单/大单净流入趋势）。
    
    code: 6位股票代码
    market: 'sh'/'sz'/None，None则自动判断（6/9开头=sh，其余=sz）
    days: 统计周期列表
    
    返回: {
        summary: [{period, main_net, super_net, large_net, positive_days, total_days}],
        detail_5d: [{date, close, change_pct, main_net, super_net, large_net}],
        detail_20d: [...],
    }
    """
    if market is None:
        market = 'sh' if code.startswith(('6', '9')) else ('bj' if code.startswith('8') else 'sz')
    
    df = ak.stock_individual_fund_flow(stock=code, market=market)
    df['主力净流入-净额'] = pd.to_numeric(df['主力净流入-净额'], errors='coerce')
    df['超大单净流入-净额'] = pd.to_numeric(df['超大单净流入-净额'], errors='coerce')
    df['大单净流入-净额'] = pd.to_numeric(df['大单净流入-净额'], errors='coerce')
    df['收盘价'] = pd.to_numeric(df['收盘价'], errors='coerce')
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    
    # 各周期汇总
    summary = []
    for d in days:
        tail = df.tail(d)
        main_net = tail['主力净流入-净额'].sum() / 1e8
        super_net = tail['超大单净流入-净额'].sum() / 1e8
        large_net = tail['大单净流入-净额'].sum() / 1e8
        pos_days = (tail['主力净流入-净额'] > 0).sum()
        summary.append({
            "period": f"{d}日",
            "main_net_yi": round(main_net, 2),
            "super_net_yi": round(super_net, 2),
            "large_net_yi": round(large_net, 2),
            "positive_days": int(pos_days),
            "total_days": len(tail),
            "signal": "主力净流入" if main_net > 0 else "主力净流出",
        })
    
    # 近5日明细
    detail_5d = []
    for _, r in df.tail(5).iterrows():
        detail_5d.append({
            "date": str(r['日期']),
            "close": round(float(r['收盘价']), 2) if pd.notna(r['收盘价']) else None,
            "change_pct": round(float(r['涨跌幅']), 2) if pd.notna(r['涨跌幅']) else None,
            "main_net_yi": round(float(r['主力净流入-净额']) / 1e8, 2) if pd.notna(r['主力净流入-净额']) else None,
            "super_net_yi": round(float(r['超大单净流入-净额']) / 1e8, 2) if pd.notna(r['超大单净流入-净额']) else None,
            "large_net_yi": round(float(r['大单净流入-净额']) / 1e8, 2) if pd.notna(r['大单净流入-净额']) else None,
        })
    
    # 近20日明细
    detail_20d = []
    for _, r in df.tail(20).iterrows():
        detail_20d.append({
            "date": str(r['日期']),
            "close": round(float(r['收盘价']), 2) if pd.notna(r['收盘价']) else None,
            "change_pct": round(float(r['涨跌幅']), 2) if pd.notna(r['涨跌幅']) else None,
            "main_net_yi": round(float(r['主力净流入-净额']) / 1e8, 2) if pd.notna(r['主力净流入-净额']) else None,
            "super_net_yi": round(float(r['超大单净流入-净额']) / 1e8, 2) if pd.notna(r['超大单净流入-净额']) else None,
            "large_net_yi": round(float(r['大单净流入-净额']) / 1e8, 2) if pd.notna(r['大单净流入-净额']) else None,
        })
    
    return {
        "summary": summary,
        "detail_5d": detail_5d,
        "detail_20d": detail_20d,
    }

# 用法
flow = fund_flow_analysis("002281")
print("=== 资金流向汇总 ===")
for s in flow['summary']:
    print(f"  {s['period']}: 主力{s['main_net_yi']}亿 超大单{s['super_net_yi']}亿 大单{s['large_net_yi']}亿 "
          f"净流入天数={s['positive_days']}/{s['total_days']} → {s['signal']}")
print("\n=== 近5日资金流向明细 ===")
for d in flow['detail_5d']:
    print(f"  {d['date']} 收盘{d['close']} 涨{d['change_pct']}% 主力{d['main_net_yi']}亿 超大单{d['super_net_yi']}亿 大单{d['large_net_yi']}亿")
```

### 6.5.3 筹码+资金 联合分析（一站式调用）

```python
def chip_and_fund_analysis(code: str) -> dict:
    """
    筹码分布 + 资金流向 联合分析。
    一次调用完成"筹码面+资金面"双维度评估。
    
    返回: {
        chip: {...},   # chip_distribution 的完整返回
        fund: {...},   # fund_flow_analysis 的完整返回
        combined_signal: str,  # 综合研判信号
    }
    """
    chip = chip_distribution(code)
    fund = fund_flow_analysis(code)
    
    if not chip or not fund.get('summary'):
        return {"error": "数据获取失败"}
    
    # 综合信号判断
    signals = []
    
    # 筹码面信号
    if chip['profit_pct'] > 90:
        signals.append(f"获利盘{chip['profit_pct']:.0f}%偏高(回吐压力大)")
    elif chip['profit_pct'] < 30:
        signals.append(f"获利盘仅{chip['profit_pct']:.0f}%(套牢重)")
    
    if chip.get('above_total') and chip['above_total'] < 5:
        signals.append("上方抛压轻(利于上攻)")
    elif chip.get('above_total') and chip['above_total'] > 30:
        signals.append("上方抛压重(阻力大)")
    
    if chip.get('deviation_pct') and chip['deviation_pct'] > 30:
        signals.append(f"偏离成本{chip['deviation_pct']:.0f}%(严重超买)")
    
    # 资金面信号
    for s in fund['summary']:
        if s['period'] == '5日':
            if s['main_net_yi'] < -5:
                signals.append(f"5日主力净流出{s['main_net_yi']:.1f}亿(主力出逃)")
            elif s['main_net_yi'] > 5:
                signals.append(f"5日主力净流入{s['main_net_yi']:.1f}亿(主力建仓)")
    
    return {
        "chip": chip,
        "fund": fund,
        "combined_signal": " | ".join(signals) if signals else "筹码与资金面中性",
    }

# 用法
result = chip_and_fund_analysis("002281")
print(f"综合信号: {result['combined_signal']}")
print_chip_chart(result['chip'])
for s in result['fund']['summary']:
    print(f"  {s['period']}: 主力{s['main_net_yi']}亿 → {s['signal']}")
```

#### 筹码分布核心字段速查

| 字段 | 含义 | 示例 |
|------|------|------|
| price | 当前价 | 201.55 |
| avg_cost | 市场加权平均成本 | 70.23 |
| deviation_pct | 偏离平均成本% | +187.1% |
| profit_pct | 获利盘比例% | 99.1% |
| loss_pct | 套牢盘比例% | 0.9% |
| pct90_low | 90%筹码集中区下沿 | 40 |
| pct90_high | 90%筹码集中区上沿 | 200 |
| pressure_price | 上方最大筹码峰价位 | 202 |
| pressure_ratio | 上方峰值占比% | 0.1% |
| above_total | 上方合计占比% | 0.8% |
| support_price | 下方最大筹码峰价位 | 70 |
| support_ratio | 下方峰值占比% | 4.0% |
| below_total | 下方合计占比% | 99.1% |
| avg_5d/20d/60d | 5/20/60日成交量加权均价 | 187.27/140.55/105.73 |
| dev_5d/20d/60d | 偏离5/20/60日均价% | +7.4%/+43.0%/+90.2% |

#### 筹码分布信号解读

| 信号 | 含义 | 操作建议 |
|------|------|----------|
| 获利盘>90% | 大量持仓者浮盈 | 注意获利回吐，不宜追高 |
| 获利盘<30% | 大量持仓者被套 | 关注超跌反弹，但套牢盘解套有抛压 |
| 上方合计<5% | 上方抛压极轻 | 利于继续上攻 |
| 上方合计>30% | 上方抛压沉重 | 上行阻力大，需放量突破 |
| 偏离成本>50% | 严重偏离平均成本 | 超买风险，均线回归压力大 |
| 90%集中区窄 | 筹码集中，方向选择在即 | 关注突破方向 |
| 90%集中区宽 | 筹码分散，持仓成本差异大 | 震荡为主，难有趋势 |

> **算法说明：** 通达信的筹码分布算法未公开，本实现采用"指数衰减+日内均匀分布"近似。半衰期60天可根据需要调整——短线交易者可设30天（更关注近期筹码），长线投资者可设90天（更关注长期持仓成本）。与通达信结果在大方向上一致（获利盘比例误差通常<5%），但具体价位占比可能有差异。

---

## Layer 7: 行业估值对比层（V2.2 新增）

> **核心价值：** 判断个股PE/PB在同行中是贵还是便宜，需要行业均值作参照。

### 7.1 同花顺行业列表 + 行业信息

```python
import akshare as ak

def find_industry(code: str) -> str | None:
    """
    根据股票代码查找其所属的同花顺行业板块名称。
    先用百度概念板块找行业名，再匹配同花顺90行业。
    """
    # 方法1: 从百度概念板块的行业分类中获取
    blocks = baidu_concept_blocks(code)  # 复用 6.3 的函数
    if blocks["industry"]:
        return blocks["industry"][0]["name"]

    # 方法2: 遍历同花顺90行业查找（兜底，较慢）
    df = ak.stock_board_industry_name_ths()
    for _, row in df.iterrows():
        industry_name = row['name']
        try:
            info = ak.stock_board_industry_info_ths(symbol=industry_name)
            # 检查该行业是否包含目标股票（需另外接口）
        except:
            continue
    return None

def industry_info(industry_name: str) -> dict:
    """
    同花顺行业板块信息（涨幅/资金净流入/涨跌家数等）。
    """
    df = ak.stock_board_industry_info_ths(symbol=industry_name)
    if df.empty:
        return {}
    result = {}
    for _, row in df.iterrows():
        result[row['项目']] = row['值']
    return result

# 用法
info = industry_info("电力")
print(f"板块涨幅: {info.get('板块涨幅', 'N/A')}")
print(f"资金净流入: {info.get('资金净流入(亿)', 'N/A')}亿")
print(f"涨跌家数: {info.get('涨跌家数', 'N/A')}")
```

### 7.2 同行业PE/PB估值对比（核心功能）

```python
import urllib.request
import akshare as ak
import pandas as pd

def industry_pe_pb_comparison(code: str, industry_name: str = None, max_stocks: int = 30) -> dict:
    """
    同行业PE/PB估值对比。
    1. 找到同行业个股列表
    2. 腾讯批量行情拉PE/PB
    3. 算行业均值/中位数/个股排名

    industry_name: 同花顺行业名（如"电力"），None则自动检测
    """
    # 1. 确定行业名
    if industry_name is None:
        blocks = baidu_concept_blocks(code)
        if blocks["industry"]:
            industry_name = blocks["industry"][0]["name"]
        else:
            return {"error": "无法自动检测行业，请手动指定 industry_name"}

    # 2. 拿同行业个股代码（用同花顺行业成分或百度概念）
    #    同花顺行业成分暂无直接接口，改用百度概念板块中的行业成分
    #    或手动指定同行业代码列表
    #    这里用 akshare stock_board_industry_name_ths 获取行业代码
    #    然后用 stock_board_industry_index_ths 获取成分（该接口返回K线，非个股列表）
    #    实测最可靠方式: 手动维护常见行业 → 代码列表映射
    #    或用东财 stock_board_industry_cons_em（但走push2域名，可能被代理拦截）

    # 实用方案: 用百度概念板块的同行股票
    try:
        url = (
            f"https://finance.pae.baidu.com/api/getrelatedblock"
            f"?code={code}&market=ab&typeCode=all&finClientType=pc"
        )
        headers = {
            "Host": "finance.pae.baidu.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
            "Accept": "application/vnd.finance-web.v1+json",
            "Origin": "https://gushitong.baidu.com",
            "Referer": "https://gushitong.baidu.com/",
        }
        import requests
        r = requests.get(url, headers=headers, timeout=10)
        d = r.json()
        if str(d.get("ResultCode", -1)) != "0":
            return {"error": "百度PAE错误"}

        # 从行业分类中提取同行业个股
        peer_codes = []
        for block in d.get("Result", []):
            if "行业" in block.get("type", ""):
                for item in block.get("list", []):
                    c = item.get("code", "")
                    if c and c.isdigit() and len(c) == 6:
                        peer_codes.append(c)
    except:
        peer_codes = []

    if not peer_codes:
        return {"error": "无法获取同行业个股列表"}

    peer_codes = list(dict.fromkeys(peer_codes))[:max_stocks]  # 去重 + 限制数量

    # 3. 腾讯批量行情拉PE/PB
    prefixed = []
    for c in peer_codes:
        if c.startswith(("6", "9")):
            prefixed.append(f"sh{c}")
        elif c.startswith("8"):
            prefixed.append(f"bj{c}")
        else:
            prefixed.append(f"sz{c}")

    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode("gbk")

    peers = []
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 53:
            continue
        c = key[2:]
        pe = float(vals[39]) if vals[39] else 0
        pb = float(vals[46]) if vals[46] else 0
        name = vals[1]
        mcap = float(vals[44]) if vals[44] else 0
        price = float(vals[3]) if vals[3] else 0
        change_pct = float(vals[32]) if vals[32] else 0
        if pe > 0:
            peers.append({
                "code": c, "name": name, "price": price,
                "pe": pe, "pb": pb, "mcap": mcap,
                "change_pct": change_pct,
                "is_target": c == code,
            })

    if not peers:
        return {"error": "无有效PE数据"}

    df = pd.DataFrame(peers)

    # 4. 计算行业均值/中位数
    pe_mean = round(df['pe'].mean(), 1)
    pe_median = round(df['pe'].median(), 1)
    pb_mean = round(df['pb'].mean(), 2)
    pb_median = round(df['pb'].median(), 2)

    # 5. 目标股排名
    target = next((p for p in peers if p['is_target']), None)
    pe_rank = sorted(peers, key=lambda x: x['pe']).index(target) + 1 if target else None

    return {
        "industry": industry_name,
        "peer_count": len(peers),
        "pe_mean": pe_mean,
        "pe_median": pe_median,
        "pb_mean": pb_mean,
        "pb_median": pb_median,
        "target": target,
        "pe_rank": f"{pe_rank}/{len(peers)}" if pe_rank else None,
        "pe_vs_median": f"{((target['pe'] / pe_median - 1) * 100):+.1f}%" if target else None,
        "peers_sorted_by_pe": sorted(peers, key=lambda x: x['pe']),
    }

# 用法
comp = industry_pe_pb_comparison("000537", "电力")
if "error" not in comp:
    t = comp['target']
    print(f"\n{t['name']}({t['code']}): PE={t['pe']:.1f} PB={t['pb']:.2f}")
    print(f"行业PE均值={comp['pe_mean']} 中位数={comp['pe_median']} 排名={comp['pe_rank']}")
    print(f"相对行业PE中位数: {comp['pe_vs_median']}")
    print(f"\n同行业PE排名:")
    for p in comp['peers_sorted_by_pe']:
        marker = " ★" if p['is_target'] else ""
        print(f"  {p['code']} {p['name']}: PE={p['pe']:.1f} PB={p['pb']:.2f} 市值={p['mcap']:.0f}亿{marker}")
```

> **数据源选择：** 同行业个股列表优先走百度概念板块（零鉴权、稳定），东财 `stock_board_industry_cons_em` 走 push2 域名可能被代理拦截。同花顺行业成分暂无直接 API，`stock_board_industry_index_ths` 返回的是行业K线而非个股列表。

---

## Layer 8: 公告层

### 5.1 巨潮公告（akshare → cninfo）

```python
import akshare as ak

df = ak.stock_zh_a_disclosure_report_cninfo(
    symbol="688017",
    market="沪市"   # "沪市" / "深市" / "北交所"
)
# 返回: 公告标题, 公告类型, 公告日期, 公告链接
# 注意: 6开头用"沪市", 0/3开头用"深市", 8开头用"北交所"

# market 判断
def get_cninfo_market(code: str) -> str:
    if code.startswith("6"):
        return "沪市"
    elif code.startswith("8"):
        return "北交所"
    else:
        return "深市"
```

### 5.2 mootdx F10 公告摘要

```python
from mootdx.quotes import Quotes
client = Quotes.factory(market='std')
text = client.F10(symbol='688017', name='最新提示')
# 包含最近的公告/分红/股东大会决议等摘要
```

---

## Layer 9: 信号层（V2 新增 + V2.1 大幅扩展）

### 6.1 同花顺热点 — 当日强势股 + 题材归因 reason tags（独家）

**核心价值：** akshare 只告诉你"哪些走强"，这个接口告诉你**"为什么走强"** —— 同花顺编辑部人工运营的题材标签。

```python
import requests
import pandas as pd

def ths_hot_reason(date: str = None) -> pd.DataFrame:
    """
    同花顺当日强势股归因。
    date: 'YYYY-MM-DD' 格式，None=今天
    返回 DataFrame，含每只股票的题材标签 (reason)。

    实测: 73ms 拿到 ~125 只 + 完整字段
    """
    from datetime import date as _date
    if date is None:
        date = _date.today().strftime("%Y-%m-%d")

    url = (
        f"http://zx.10jqka.com.cn/event/api/getharden/"
        f"date/{date}/orderby/date/orderway/desc/charset/GBK/"
    )
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "Chrome/117.0.0.0 Safari/537.36"
        )
    }
    r = requests.get(url, headers=headers, timeout=10)
    data = r.json()
    if data.get("errocode", 0) != 0:
        raise RuntimeError(f"同花顺热点错误: {data.get('errormsg', '')}")

    rows = data.get("data") or []
    df = pd.DataFrame(rows)
    if df.empty:
        return df

    # 字段重命名（中文友好）
    rename_map = {
        "name": "名称", "code": "代码", "reason": "题材归因",
        "close": "收盘价", "zhangdie": "涨跌额", "zhangfu": "涨幅%",
        "huanshou": "换手率%", "chengjiaoe": "成交额",
        "chengjiaoliang": "成交量", "ddejingliang": "大单净量",
        "market": "市场",
    }
    df = df.rename(columns=rename_map)
    return df

# 用法
df = ths_hot_reason("2026-05-09")
print(f"当日强势股: {len(df)} 只")
print(df[["代码", "名称", "涨幅%", "题材归因"]].head(10))
```

#### 同花顺热点字段速查

| 原字段 | 中文 | 说明 |
|---|---|---|
| code | 代码 | 6 位股票代码 |
| name | 名称 | 简称 |
| **reason** | **题材归因** | **核心字段，人工运营 tags，如"算力租赁+Token工厂+AI政务"** |
| zhangfu | 涨幅% | 当日涨幅 |
| huanshou | 换手率% | 当日换手 |
| chengjiaoe | 成交额 | 元 |
| chengjiaoliang | 成交量 | 股 |
| ddejingliang | 大单净量 | 主力净流入指标 |
| close | 收盘价 | 元 |
| zhangdie | 涨跌额 | 元 |
| market | 市场 | 沪/深/北 |

### 6.2 同花顺北向资金 — hsgtApi 实时分钟流向 + 本地自缓存历史

> **V2.1 重大变更：** eastmoney 全系北向数据（akshare `stock_hsgt_hist_em`、datacenter API、push2his kamt.kline）自 2024-08 后净买额字段全部返回 NaN/None/0，属上游行业性断供。已改为**本地 CSV 自缓存模式**——每次拉实时数据后自动把收盘数据写入 `~/.tradingagents/cache/northbound_daily.csv`，历史越跑越丰富。

```python
import requests
import pandas as pd
from pathlib import Path

HSGT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Chrome/117.0.0.0 Safari/537.36"
    ),
    "Host": "data.hexin.cn",
    "Referer": "https://data.hexin.cn/",
}

def hsgt_realtime() -> pd.DataFrame:
    """
    沪深股通当日实时分钟流向（含集合竞价 09:10–15:00，262 个时间点）。
    返回字段: time, hgt(沪股通累计净买入), sgt(深股通累计净买入)
    单位: 亿元
    """
    url = "https://data.hexin.cn/market/hsgtApi/method/dayChart/"
    r = requests.get(url, headers=HSGT_HEADERS, timeout=10)
    d = r.json()
    times = d.get("time", [])
    hgt = d.get("hgt", [])
    sgt = d.get("sgt", [])

    n = len(times)
    return pd.DataFrame({
        "time": times,
        "hgt_yi": hgt[:n] + [None] * (n - len(hgt)),
        "sgt_yi": sgt[:n] + [None] * (n - len(sgt)),
    })

# === V2.1 自缓存辅助函数 ===

def _northbound_cache_path() -> Path:
    """北向资金本地 CSV 缓存路径"""
    p = Path.home() / ".tradingagents" / "cache" / "northbound_daily.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def _save_northbound_snapshot(date: str, hgt: float, sgt: float):
    """写入/更新当天北向收盘数据到 CSV"""
    path = _northbound_cache_path()
    rows = {}
    if path.exists():
        for line in path.read_text().strip().split("\n")[1:]:
            parts = line.split(",")
            if len(parts) == 3:
                rows[parts[0]] = line
    rows[date] = f"{date},{hgt},{sgt}"
    with open(path, "w") as f:
        f.write("date,hgt,sgt\n")
        for d in sorted(rows.keys()):
            f.write(rows[d] + "\n")

def _load_northbound_history(n: int = 20) -> pd.DataFrame:
    """读取最近 N 天北向历史"""
    path = _northbound_cache_path()
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    return df.tail(n)

# 用法 1: 实时分钟流向
df = hsgt_realtime()
print(f"分钟点数: {len(df)}")
print(df.tail(5))

# 用法 2: 自动缓存今日收盘数据
if not df.empty:
    last = df.dropna().iloc[-1]
    _save_northbound_snapshot("2026-05-12", last["hgt_yi"], last["sgt_yi"])

# 用法 3: 读取历史
hist = _load_northbound_history(20)
print(hist)
```

### 6.3 百度股市通 — 概念板块归属（V2.1 新增）

**核心价值：** 一次调用拿到个股所属的行业（申万一级/二级）、概念（多个）、地域三维分类，含当日涨跌幅。

```python
import requests

_BAIDU_PAE_HEADERS = {
    "Host": "finance.pae.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
    "Accept": "application/vnd.finance-web.v1+json",
    "Origin": "https://gushitong.baidu.com",
    "Referer": "https://gushitong.baidu.com/",
}

def baidu_concept_blocks(code: str) -> dict:
    """
    百度股市通概念板块归属。
    返回: {industry: [...], concept: [...], region: [...], concept_tags: [...]}
    """
    url = (
        f"https://finance.pae.baidu.com/api/getrelatedblock"
        f"?code={code}&market=ab"
        f"&typeCode=all&finClientType=pc"
    )
    r = requests.get(url, headers=_BAIDU_PAE_HEADERS, timeout=10)
    d = r.json()
    if str(d.get("ResultCode", -1)) != "0":
        raise RuntimeError(f"百度PAE错误: {d}")

    result = {"industry": [], "concept": [], "region": [], "concept_tags": []}
    for block in d.get("Result", []):
        block_type = block.get("type", "")
        for item in block.get("list", []):
            entry = {
                "name": item.get("name", ""),
                "change_pct": item.get("increase", ""),
                "desc": item.get("desc", ""),
            }
            if "行业" in block_type:
                result["industry"].append(entry)
            elif "概念" in block_type:
                result["concept"].append(entry)
                result["concept_tags"].append(entry["name"])
            elif "地域" in block_type:
                result["region"].append(entry)
    return result

# 用法
blocks = baidu_concept_blocks("688017")
print("行业:", [b["name"] for b in blocks["industry"]])
print("概念:", blocks["concept_tags"])
print("地域:", [b["name"] for b in blocks["region"]])
```

> **踩坑：** `ResultCode` 返回类型不稳定——有时 int `0`，有时 string `"0"`。必须用 `str()` 统一比较。

### 6.4 百度股市通 — 个股资金流向（V2.1 新增）

实时分钟级 + 历史 20 交易日的主力/散户资金流向。

```python
import requests

def baidu_fund_flow_realtime(code: str, date: str) -> list[dict]:
    """
    个股资金流向（分钟级）。
    date: YYYYMMDD 紧凑格式
    返回: [{time, mainForce, retail, super, large, price}, ...]
    """
    url = (
        f"https://finance.pae.baidu.com/vapi/v1/fundflow"
        f"?code={code}&market=ab&date={date}"
        f"&finClientType=pc"
    )
    r = requests.get(url, headers=_BAIDU_PAE_HEADERS, timeout=10)
    d = r.json()
    if str(d.get("ResultCode", -1)) != "0":
        return []

    raw = d.get("Result", {}).get("update_data", "")
    if not raw:
        return []

    rows = []
    for segment in raw.split(";"):
        parts = segment.split(",")
        if len(parts) >= 9:
            rows.append({
                "time": parts[0],
                "mainForce": float(parts[2]) if parts[2] else 0,
                "retail": float(parts[3]) if parts[3] else 0,
                "super": float(parts[4]) if parts[4] else 0,
                "large": float(parts[5]) if parts[5] else 0,
                "price": float(parts[8]) if parts[8] else 0,
            })
    return rows

def baidu_fund_flow_history(code: str, days: int = 20) -> list[dict]:
    """
    个股资金流向（日级，最近 N 交易日）。
    返回: [{date, close, change_pct, superNetIn, largeNetIn, mediumNetIn, littleNetIn, mainIn}, ...]
    """
    url = (
        f"https://finance.pae.baidu.com/vapi/v1/fundsortlist"
        f"?code={code}&market=ab&pn=0&rn={days}"
        f"&finClientType=pc"
    )
    r = requests.get(url, headers=_BAIDU_PAE_HEADERS, timeout=10)
    d = r.json()
    if str(d.get("ResultCode", -1)) != "0":
        return []

    rows = []
    for item in d.get("Result", {}).get("list", []):
        rows.append({
            "date": item.get("showtime", ""),
            "close": item.get("closepx", ""),
            "change_pct": item.get("ratio", ""),
            "superNetIn": item.get("superNetIn", ""),
            "largeNetIn": item.get("largeNetIn", ""),
            "mediumNetIn": item.get("mediumNetIn", ""),
            "littleNetIn": item.get("littleNetIn", ""),
            "mainIn": item.get("extMainIn", ""),
        })
    return rows

# 用法 1: 分钟级实时
realtime = baidu_fund_flow_realtime("000858", "20260512")
if realtime:
    last = realtime[-1]
    signal = "bullish" if last["mainForce"] > 0 else "bearish"
    print(f"主力净流入: {last['mainForce']}万 → {signal}")

# 用法 2: 20日历史
history = baidu_fund_flow_history("000858")
for h in history[:5]:
    print(f"{h['date']}: 主力={h['mainIn']}万 超大单={h['superNetIn']}万")
```

> **踩坑：** 实时数据格式是分号分隔的字符串（非 JSON 数组），`date` 参数用紧凑格式 `20260512` 而非 `2026-05-12`。

### 6.5 龙虎榜席位（V2.1 新增）

akshare 三函数聚合——上榜记录 + 买卖席位 TOP5 + 机构买卖统计。

```python
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def dragon_tiger_board(code: str, trade_date: str, look_back: int = 30) -> dict:
    """
    龙虎榜数据聚合。
    trade_date: YYYY-MM-DD
    look_back: 回看天数
    返回: {records: [...], seats: {buy: [...], sell: [...]}, institution: {...}}
    """
    start = datetime.strptime(trade_date, "%Y-%m-%d") - timedelta(days=look_back)
    start_str = start.strftime("%Y%m%d")
    end_str = trade_date.replace("-", "")

    # 1. 上榜记录
    records = []
    try:
        df = ak.stock_lhb_detail_em(
            start_date=start_str,
            end_date=end_str
        )
        if not df.empty:
            df_stock = df[df["代码"] == code]
            for _, row in df_stock.iterrows():
                records.append({
                    "date": str(row.get("日期", "")),
                    "reason": row.get("解读", ""),
                    "net_buy": row.get("龙虎榜净买额", 0),
                    "turnover": row.get("换手率", 0),
                })
    except Exception:
        pass

    # 2. 最近上榜的买卖席位
    seats = {"buy": [], "sell": []}
    if records:
        latest_date = records[0]["date"].replace("-", "")[:8]
        try:
            df_detail = ak.stock_lhb_stock_detail_em(
                symbol=code,
                date=latest_date,
                flag="买入"
            )
            if not df_detail.empty:
                for _, row in df_detail.head(5).iterrows():
                    seats["buy"].append({
                        "name": row.get("营业部名称", ""),
                        "buy_amt": row.get("买入额", 0),
                        "sell_amt": row.get("卖出额", 0),
                        "net": row.get("净额", 0),
                    })
        except Exception:
            pass
        try:
            df_detail = ak.stock_lhb_stock_detail_em(
                symbol=code,
                date=latest_date,
                flag="卖出"
            )
            if not df_detail.empty:
                for _, row in df_detail.head(5).iterrows():
                    seats["sell"].append({
                        "name": row.get("营业部名称", ""),
                        "buy_amt": row.get("买入额", 0),
                        "sell_amt": row.get("卖出额", 0),
                        "net": row.get("净额", 0),
                    })
        except Exception:
            pass

    # 3. 机构买卖统计
    institution = {}
    try:
        df_inst = ak.stock_lhb_jgmmtj_em(symbol=code)
        if not df_inst.empty:
            row = df_inst.iloc[0]
            institution = {
                "buy_count": row.get("买入机构数", 0),
                "sell_count": row.get("卖出机构数", 0),
                "net_amount": row.get("机构净买入额", 0),
            }
    except Exception:
        pass

    return {"records": records, "seats": seats, "institution": institution}

# 用法
data = dragon_tiger_board("002475", "2026-05-12")
print(f"近30日上榜 {len(data['records'])} 次")
for r in data["records"]:
    print(f"  {r['date']}: {r['reason']}")
if data["seats"]["buy"]:
    print("买入席位 TOP5:")
    for s in data["seats"]["buy"]:
        print(f"  {s['name']}: 买{s['buy_amt']}万 卖{s['sell_amt']}万 净{s['net']}万")
```

> **ST 股注意：** 5% 涨跌停更容易触发龙虎榜（"连续三日偏离值累计达12%"），科创板 20% 涨跌停则较少触发。

### 6.6 限售解禁日历（V2.1 新增）

个股历史解禁 + 未来 90 天待解禁预警。

```python
import akshare as ak
from datetime import datetime, timedelta

def lockup_expiry(code: str, trade_date: str, forward_days: int = 90) -> dict:
    """
    限售解禁日历。
    返回: {history: [...], upcoming: [...]}
    """
    # 1. 历史解禁记录
    history = []
    try:
        df = ak.stock_restricted_release_queue_em(symbol=code)
        if not df.empty:
            for _, row in df.head(15).iterrows():
                history.append({
                    "date": str(row.get("解禁时间", "")),
                    "type": row.get("限售股类型", ""),
                    "shares": row.get("解禁数量", 0),
                    "ratio": row.get("实际解禁市值占总市值比例", 0),
                })
    except Exception:
        pass

    # 2. 未来待解禁
    upcoming = []
    end_date = datetime.strptime(trade_date, "%Y-%m-%d") + timedelta(days=forward_days)
    end_str = end_date.strftime("%Y%m%d")
    today_str = trade_date.replace("-", "")
    try:
        df = ak.stock_restricted_release_detail_em(
            date=today_str
        )
        if not df.empty:
            df_stock = df[df["股票代码"] == code]
            for _, row in df_stock.iterrows():
                upcoming.append({
                    "date": str(row.get("解禁日期", "")),
                    "type": row.get("限售股类型", ""),
                    "shares": row.get("解禁数量", 0),
                    "float_ratio": row.get("占流通股比例", 0),
                })
    except Exception:
        pass

    return {"history": history, "upcoming": upcoming}

# 用法
data = lockup_expiry("002475", "2026-05-12")
print(f"历史解禁 {len(data['history'])} 批")
for h in data["history"][:5]:
    print(f"  {h['date']}: {h['type']} 数量={h['shares']}")
if data["upcoming"]:
    print(f"未来90天待解禁 {len(data['upcoming'])} 批")
else:
    print("未来90天无待解禁")
```

**限售股类型参考：**
- 首发原股东限售股份（IPO 后 1-3 年）
- 首发机构配售股份（IPO 战略配售）
- 定向增发机构配售股份（6-18 个月）
- 股权激励限售股份

### 6.7 行业横向对比（V2.1 新增）

同花顺 90 行业板块涨跌幅排名，一次调用看全市场行业轮动。

```python
import akshare as ak

def industry_comparison(top_n: int = 20) -> dict:
    """
    全行业涨跌幅排名（同花顺 ~90 个行业）。
    返回: {top: [...], bottom: [...], total: int}
    """
    df = ak.stock_board_industry_summary_ths()
    if df.empty:
        return {"top": [], "bottom": [], "total": 0}

    rows = []
    for i, row in df.iterrows():
        rows.append({
            "rank": i + 1,
            "name": row.get("板块", ""),
            "change_pct": row.get("涨跌幅", 0),
            "turnover_yi": row.get("总成交额", 0),
            "net_inflow_yi": row.get("净流入", 0) if "净流入" in df.columns else None,
            "up_count": row.get("上涨家数", 0),
            "down_count": row.get("下跌家数", 0),
            "leader": row.get("领涨股", ""),
        })

    return {
        "top": rows[:top_n],
        "bottom": rows[-top_n:],
        "total": len(rows),
    }

# 用法
data = industry_comparison(20)
print(f"共 {data['total']} 个行业")
print("\nTOP 10 涨幅:")
for r in data["top"][:10]:
    print(f"  {r['rank']}. {r['name']}: {r['change_pct']}% 成交{r['turnover_yi']}亿 领涨{r['leader']}")
print("\nBOTTOM 5 跌幅:")
for r in data["bottom"][-5:]:
    print(f"  {r['rank']}. {r['name']}: {r['change_pct']}%")
```

> **踩坑：** 成交额列名是 `总成交额`（不是 `成交额`），领涨股列名是 `领涨股`（不是 `领涨股票`），金额单位已经是亿元。该函数无日期参数，返回最新交易日数据。

### 6.8 全市场龙虎榜（V2.1 新增）

每日全市场龙虎榜汇总——当日所有触发龙虎榜的股票 + 上榜原因 + 买卖净额 + 换手率。直接调东财 datacenter API，不依赖 akshare（akshare `stock_lhb_detail_em` 存在空页面解析 bug）。

```python
import requests
from datetime import datetime

def daily_dragon_tiger(trade_date: str = None, min_net_buy: float = None) -> dict:
    """
    全市场龙虎榜。
    trade_date: YYYY-MM-DD（默认当日）
    min_net_buy: 净买入下限（万元），None 不过滤
    返回: {date, total_records, stocks: [{code, name, reason, close, change_pct,
           net_buy_wan, buy_wan, sell_wan, turnover_pct}]}
    """
    if trade_date is None:
        trade_date = datetime.now().strftime("%Y-%m-%d")
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_DAILYBILLBOARD_DETAILSNEW",
        "columns": "ALL",
        "filter": f"(TRADE_DATE>='{trade_date}')(TRADE_DATE<='{trade_date}')",
        "pageNumber": "1",
        "pageSize": "500",
        "sortTypes": "-1",
        "sortColumns": "BILLBOARD_NET_AMT",
        "source": "WEB",
        "client": "WEB",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://data.eastmoney.com/",
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    d = r.json()
    if not d.get("success") or not d.get("result") or not d["result"].get("data"):
        return {"date": trade_date, "total_records": 0, "stocks": [],
                "note": "无数据（非交易日或盘后未更新）"}
    data = d["result"]["data"]
    actual_date = data[0].get("TRADE_DATE", "")[:10] if data else trade_date
    stocks = []
    for row in data:
        net_buy = (row.get("BILLBOARD_NET_AMT") or 0) / 10000
        if min_net_buy is not None and net_buy < min_net_buy:
            continue
        stocks.append({
            "code": row.get("SECURITY_CODE", ""),
            "name": row.get("SECURITY_NAME_ABBR", ""),
            "reason": row.get("EXPLANATION", ""),
            "close": row.get("CLOSE_PRICE") or 0,
            "change_pct": round(float(row.get("CHANGE_RATE") or 0), 2),
            "net_buy_wan": round(net_buy, 1),
            "buy_wan": round((row.get("BILLBOARD_BUY_AMT") or 0) / 10000, 1),
            "sell_wan": round((row.get("BILLBOARD_SELL_AMT") or 0) / 10000, 1),
            "turnover_pct": round(float(row.get("TURNOVERRATE") or 0), 2),
        })
    return {"date": actual_date, "total_records": len(stocks), "stocks": stocks}

# 用法
data = daily_dragon_tiger("2026-05-09")
print(f"{data['date']} 龙虎榜共 {data['total_records']} 条记录")
for s in data["stocks"][:10]:
    print(f"  {s['code']} {s['name']}: {s['reason']} | 净买{s['net_buy_wan']}万 涨跌{s['change_pct']}%")

# 只看净买入 > 5000 万的
data = daily_dragon_tiger("2026-05-09", min_net_buy=5000)
print(f"\n净买入 > 5000万: {data['total_records']} 条")
```

> **与 6.5 龙虎榜席位的区别：** 6.5 是"查某只股票的龙虎榜历史 + 席位明细"（个股维度），6.8 是"查某天全市场所有上榜股票"（全市场维度）。前者回答"002475 最近上过龙虎榜吗"，后者回答"今天龙虎榜哪些票净买入最大"。

> **数据源：** 东财 datacenter API（`RPT_DAILYBILLBOARD_DETAILSNEW`），绕过 akshare 的解析 bug。pageSize=500 足够覆盖单日所有记录（通常 80-120 条）。非交易日或收盘前调用返回空数据。

### 6.9 信号层组合用法：题材热度 + 资金验证

```python
# 拉当日强势股 reason
df_hot = ths_hot_reason()

# 词频统计 reason 列里的题材关键词
from collections import Counter
all_tags = []
for r in df_hot["题材归因"].dropna():
    tags = [t.strip() for t in str(r).split("+") if t.strip()]
    all_tags.extend(tags)

cnt = Counter(all_tags)
print("当日 TOP 10 题材热度:")
for tag, n in cnt.most_common(10):
    print(f"  {tag}: {n} 只")

# 同时拉北向当日流向，看资金流方向是否对应题材
df_north = hsgt_realtime()
hgt_close = df_north["hgt_yi"].dropna().iloc[-1] if not df_north.empty else 0
sgt_close = df_north["sgt_yi"].dropna().iloc[-1] if not df_north.empty else 0
print(f"\n北向收盘累计: 沪股通 {hgt_close} 亿 / 深股通 {sgt_close} 亿")

# V2.1: 叠加行业对比，看哪些行业资金在流入
comp = industry_comparison(10)
print("\n行业资金流入 TOP 5:")
for r in sorted(comp["top"], key=lambda x: x.get("net_inflow_yi") or 0, reverse=True)[:5]:
    print(f"  {r['name']}: 净流入 {r.get('net_inflow_yi', 'N/A')} 亿")
```

---

## 估值计算公式

### 前向PE

```python
def forward_pe(price: float, eps_forecast: float) -> float:
    """前向PE = 当前股价 / 未来年度一致预期EPS"""
    if eps_forecast <= 0:
        return float("inf")
    return price / eps_forecast
```

### PE消化时间

```python
import math

def pe_digestion(current_pe: float, cagr: float, target_pe: float = 30) -> float:
    """
    当前PE消化到目标PE需要多少年。
    target_pe 固定30x（A股成长股合理估值锚点）。
    cagr: 用 下一年EPS / 当年EPS - 1
    """
    if current_pe <= target_pe:
        return 0.0
    if cagr <= 0:
        return float("inf")
    return math.log(current_pe / target_pe) / math.log(1 + cagr)
```

### PEG

```python
def calc_peg(pe: float, cagr: float) -> float:
    """
    PEG = 前向PE / (CAGR * 100)
    PEG < 1   → 便宜
    PEG 1-1.5 → 合理
    PEG > 1.5 → 贵
    """
    if cagr <= 0:
        return float("inf")
    return pe / (cagr * 100)
```

### 投资框架速查

```
壁垒 → 增速 → PE消化 → PEG校验

1. 有壁垒吗？(tech_moat / capacity_moat) → 没有则排除
2. 增速多少？(CAGR > 30% 才有意义)
3. PE多久消化到30x？(< 2年合理, > 4年太贵)
4. PEG多少？(< 1 便宜, 1-1.5 合理, > 1.5 贵)

30x PE 锚点: A股成长股的合理估值重力线，所有行业统一用30x。
期权定价例外: PEG > 3 但壁垒极深时，本质是看涨期权，不适用PEG框架。
```

---

## 完整调研流程

### 流程 A: 单票完整估值（30秒）

```python
import akshare as ak
import urllib.request
import math

def full_valuation(code: str) -> dict:
    """单票完整估值分析"""
    # 1. 腾讯实时行情
    prefix = "sh" if code.startswith(("6","9")) else ("bj" if code.startswith("8") else "sz")
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode("gbk")
    vals = data.split('"')[1].split("~")
    price = float(vals[3])
    mcap = float(vals[44])
    pe_ttm = float(vals[39]) if vals[39] else 0
    pb = float(vals[46]) if vals[46] else 0

    # 2. 机构一致预期
    df = ak.stock_profit_forecast_ths(symbol=code, indicator="预测年报每股收益")
    eps_cur = eps_next = None
    analyst_count = 0
    years_sorted = sorted(df["年度"].unique())
    for _, row in df.iterrows():
        y = str(row["年度"])
        if y == str(years_sorted[0]) if len(years_sorted) > 0 else False:
            eps_cur = float(row["均值"])
            analyst_count = int(row["预测机构数"])
        elif y == str(years_sorted[1]) if len(years_sorted) > 1 else False:
            eps_next = float(row["均值"])

    # 3. 估值指标
    pe_fwd = price / eps_cur if eps_cur else float("inf")
    cagr = (eps_next / eps_cur - 1) if (eps_cur and eps_next) else 0
    peg = pe_fwd / (cagr * 100) if cagr > 0 else float("inf")
    digest = (
        math.log(pe_fwd / 30) / math.log(1 + cagr)
        if pe_fwd > 30 and cagr > 0 else 0
    )

    return {
        "name": vals[1],
        "price": price,
        "mcap_yi": mcap,
        "pe_ttm": pe_ttm,
        "pb": pb,
        "eps_cur": eps_cur,
        "eps_next": eps_next,
        "pe_fwd": round(pe_fwd, 1) if eps_cur else None,
        "cagr_pct": round(cagr * 100, 0) if cagr else None,
        "peg": round(peg, 2) if peg != float("inf") else None,
        "digest_years": round(digest, 1),
        "analyst_count": analyst_count,
    }

# 用法
result = full_valuation("688017")
print(result)
```

### 流程 B: 批量估值对比

```python
stocks = ["688017", "300308", "300476", "002463"]
for code in stocks:
    try:
        r = full_valuation(code)
        print(f"{r['name']}({code}): PE_fwd={r['pe_fwd']}x PEG={r['peg']} 消化={r['digest_years']}年 覆盖={r['analyst_count']}家")
    except Exception as e:
        print(f"{code}: 失败 - {e}")
```

### 流程 C: 主题研报批量检索

```python
# Step 1: iwencai 多 query 语义搜索
queries = [
    "人形机器人产业链深度 2026",
    "人形机器人减速器 丝杠",
    "特斯拉Optimus 国产供应链",
]
seen_uids = set()
all_articles = []
for q in queries:
    arts = iwencai_search(q, channel="report", size=50)
    for a in arts:
        uid = a.get("uid", "")
        if uid not in seen_uids:
            seen_uids.add(uid)
            all_articles.append(a)
print(f"共 {len(all_articles)} 篇去重后研报")

# Step 2: 东财补充同标的研报 + PDF
for a in all_articles[:10]:
    stocks = a.get("stock_infos") or []
    for s in stocks:
        stock_code = s.get("code", "")
        if stock_code:
            em = eastmoney_reports(stock_code, max_pages=1)
            print(f"  {stock_code}: 东财 {len(em)} 篇")
```

### 流程 D: 新标的快速调研（V2.2 增强版）

```python
code = "688017"

# 1. 有无机构覆盖？
forecast = ak.stock_profit_forecast_ths(symbol=code, indicator="预测年报每股收益")
print(f"机构覆盖: {'有' if not forecast.empty else '无'}")

# 2. 实时估值
quotes = tencent_quote([code])
q = quotes[code]
print(f"PE={q['pe_ttm']} PB={q['pb']} 市值={q['mcap_yi']}亿")

# 3. PE消化 → 用 full_valuation()
# 4. PEG校验

# 5. V2.2: 近3年财务趋势（判断增长质量）
trend = financial_trend(code, 3)
for t in trend:
    print(f"  {t['date']}: 营收={t['revenue']}(+{t['revenue_yoy']}) 净利={t['net_profit']}(+{t['net_profit_yoy']})")

# 6. V2.2: 技术面（判断买卖时机）
tech = technical_analysis(code)
print(f"  MA20={tech['ma20']} MA60={tech['ma60']} RSI={tech['rsi14']}")
print(f"  信号: {tech['trend_signal']}")

# 7. V2.1: 概念板块归属
blocks = baidu_concept_blocks(code)
print(f"概念: {', '.join(blocks['concept_tags'][:10])}")

# 8. V2.2: 同行业PE/PB对比（判断在同行中贵不贵）
comp = industry_pe_pb_comparison(code)
if "error" not in comp:
    t = comp['target']
    print(f"  行业PE均值={comp['pe_mean']} 中位数={comp['pe_median']} 排名={comp['pe_rank']}")
    print(f"  相对中位数: {comp['pe_vs_median']}")

# 9. V2.1: 资金流向
flow = baidu_fund_flow_history(code)
if flow:
    recent = flow[0]
    print(f"最近主力净流入: {recent['mainIn']}万")

# 10. V2.1: 龙虎榜
dtb = dragon_tiger_board(code, "2026-05-12")
print(f"近30日上龙虎榜: {len(dtb['records'])} 次")

# 11. V2.1: 解禁预警
lockup = lockup_expiry(code, "2026-05-12")
print(f"未来90天待解禁: {len(lockup['upcoming'])} 批")
```

---

## 数据源优先级

| 优先级 | 数据源 | 用途 | 可靠性 | 封IP风险 |
|--------|--------|------|--------|---------|
| 1 | **mootdx** (TCP) | K线+五档盘口+逐笔成交+财务快照+F10 | 极稳定 | 极低 |
| 2 | **腾讯财经** (HTTP) | 实时PE/PB/市值/换手率/涨跌停+批量同行估值 | 稳定 | 低 |
| 3 | **akshare** (Python) | 研报+一致预期+新闻+公告+龙虎榜+解禁+行业+财务趋势 | 稳定 | 中(东财源) |
| 4 | **iwencai** (OpenAPI) | NL主题搜索研报(唯一能力) | 需X-Claw Header | 低 |
| 5 | **东财PDF** (HTTP) | 完整研报图表、评级 | 稳定但需下载 | 低 |
| 6 | **同花顺热点** (HTTP) | 当日强势股+题材归因 reason tags | 稳定 73ms | 极低（零鉴权） |
| 7 | **同花顺 hsgtApi** (HTTP) | 北向资金分钟级+自缓存历史 | 稳定 | 极低（零鉴权） |
| 8 | **百度股市通** (HTTP) | 概念板块+个股资金流向+同行股票列表 | 稳定 | 极低（零鉴权） |
| 9 | **同花顺 THS** (HTTP) | 财务摘要多期+行业名称/信息 | 稳定 | 极低 |
| 10 | **stockstats** (Python) | MA/MACD/RSI/BOLL技术指标计算 | 本地计算 | 无 |
| 11 | **筹码分布** (本地计算) | 获利盘/套牢盘/平均成本/抛压支撑/资金流向 | 本地计算+mootdx+akshare | 无 |

**原则：** 行情走 mootdx+腾讯（不封IP），研报走 akshare+东财PDF，iwencai 仅用于 NL 主题搜索，**信号层走同花顺+百度直连接口（零鉴权 + 编辑部人工运营 tags + 分钟级资金流向）**，**财务趋势走同花顺 THS，技术面走 mootdx K线 + stockstats 本地计算，筹码分布走 mootdx K线 + 指数衰减算法 + akshare资金流向，行业估值走同花顺行业列表 + 腾讯批量行情**。

---

## FAQ

### Q: mootdx 和腾讯有什么区别？
A: 互补关系。mootdx = 交易层（价格+盘口+K线），腾讯 = 估值层（PE/PB/市值/换手率/涨跌停价）。两者都不封IP。

### Q: iwencai 返回 401
A: 检查两点：(1) API Key 是否有效 (2) 是否携带了 X-Claw-* Headers。SkillHub 2.0 后必须带 X-Claw Headers，否则一律 401。

### Q: akshare 报 ConnectionError / 超时
A: 同花顺和东财有反爬，加 `time.sleep(1~3)` 再重试。mootdx 和腾讯不受影响。

### Q: stock_profit_forecast_ths 返回空 DataFrame
A: 该股票无机构覆盖。"预测年报每股收益" indicator 最稳定，"预测详细指标" 有时返回空。小盘/次新/ST 股常见。

### Q: 东财 PDF 下载 403
A: 必须带 `Referer: https://data.eastmoney.com/` header。

### Q: 腾讯 API 返回乱码
A: 编码是 GBK，必须 `decode("gbk")`。

### Q: 腾讯 API 字段 43 是 PB 吗？
A: **不是！** 43=振幅%，46=PB。网上很多教程写错了，这里是实测校准结果。

### Q: iwencai search 返回条数太少
A: `size` 参数默认 10，调到 50。隐藏参数，文档未写明但实测可用。

### Q: 哪些数据源需要 API Key？
A: 只有 iwencai 需要。mootdx / 腾讯 / akshare / 巨潮 / 同花顺 / 百度股市通全部免费无 key。

### Q: 同花顺热点接口需要 cookie 吗？
A: **不需要**。仅 User-Agent 即可，零鉴权 73ms 拿到 ~125 只当日强势股。但**不要去打 search.10jqka.com.cn 的 iwencai NL 选股接口** —— 那个有 hexin-v cookie JS 签名鉴权，跟热点接口完全两码事。

### Q: 同花顺热点 reason 字段为空怎么办？
A: 两种情况：(1) 当日盘后数据还没更新，等到 15:30 之后再调；(2) 个别 ST 股或暂停股没有人工标注。`reason` 字段允许 None，过滤 `df.dropna(subset=["题材归因"])` 即可。

### Q: hsgtApi 北向资金数据跟东财 push2 不一致？
A: 不是 bug，两个源采样口径不同。同花顺 hsgtApi 给**累计净买入**（每分钟从 09:10 累加），东财 push2 给**当前流入流出比**。做交叉验证时用 hsgtApi 看趋势，用东财看实时强度。

### Q: 同花顺热点接口能拉历史日期吗？
A: 可以。URL 里的 `date/{YYYY-MM-DD}/` 替换成历史日期即可，节假日和周末返回空数组。建议本地缓存（比如 SQLite 按日期存），避免重复拉。

### Q: 百度股市通 ResultCode 有时是 0 有时是 "0"？
A: 已知坑。`ResultCode` 返回类型不稳定——有时 int，有时 string。代码里必须用 `str(d.get("ResultCode", -1)) != "0"` 统一比较。无官方 API 文档，字段可能随时变更。

### Q: 北向资金历史数据为什么只有最近几天？
A: V2.1 改为本地自缓存模式。eastmoney 全系北向数据自 2024-08 起断供（净买额字段返回 NaN/0）。每次调用实时 API 后自动写入本地 CSV，历史越跑越丰富。新用户首次运行只有当天数据。

### Q: 龙虎榜 ST 股为什么上榜频率高？
A: ST 股涨跌停限制 5%（正常股 10%，科创板 20%），触发"连续三日偏离值累计达12%"的概率更高。科创板则相反，20% 涨跌停不容易触发龙虎榜。

### Q: 在海外服务器跑，mootdx 接口超时？
A: mootdx 走 TCP 直连通达信行情服务器，需国内 IP 才稳定。海外环境建议走代理或切换到 yfinance。腾讯财经和百度股市通不受影响。

### Q: 不用 Claude Code，能用吗？
A: 能。SKILL.md 本质是 Markdown + 内嵌 Python 代码。Codex、OpenClaw 或任何 AI 编程助手都能读取。你也可以直接把 Python 代码段复制出来在自己的脚本里跑。

### Q: 筹码分布能查吗？
A: **能（V2.3 新增）**。使用 `chip_distribution()` 函数，基于 mootdx 250根日K线 + 指数衰减算法（60日半衰期）在本地计算筹码分布，可输出获利盘/套牢盘比例、平均成本、90%集中区、上方抛压/下方支撑、筹码分布图。同时 `fund_flow_analysis()` 聚合 akshare 资金流向数据，`chip_and_fund_analysis()` 一次调用完成双维度联合分析。注意：算法为近似实现，与通达信客户端结果在大方向一致但具体价位占比可能有差异。

### Q: stock_profit_sheet_by_report_em 报错 NoneType？
A: 已知 bug。该接口依赖东财页面的 `hidctype` 元素，部分股票页面结构变更导致解析失败。**改用 `stock_financial_abstract_ths`（同花顺源）**，更稳定且含多期趋势数据。

### Q: 东财行业接口（push2域名）连不上？
A: push2.eastmoney.com 走 HTTPS + CDN，部分代理环境会阻断。**替代方案**：(1) 同花顺行业接口 `stock_board_industry_name_ths` + `stock_board_industry_info_ths` 不受影响；(2) 腾讯批量行情 + 百度概念板块可组合实现同行业PE/PB对比。

---

## 安装说明

```bash
# 1. 创建 skill 目录
mkdir -p ~/.claude/skills/a-stock-data

# 2. 将本文件复制为 SKILL.md
cp SKILL.md ~/.claude/skills/a-stock-data/SKILL.md

# 3. 安装 Python 依赖
pip install mootdx akshare requests pandas stockstats

# 4. (可选) 配置 iwencai API Key
export IWENCAI_API_KEY="your_key_here"

# 5. 启动 Claude Code，说"查一下688017的估值"即可自动激活
```

---

> 📦 https://github.com/simonlin1212/a-stock-data — Star ⭐ 是最好的支持

#!/usr/bin/env python3
"""紫光股份 (000938) 全栈深度分析"""
import warnings
warnings.filterwarnings("ignore")

import sys
import math
import numpy as np
import pandas as pd
from mootdx.quotes import Quotes
from stockstats import StockDataFrame

CODE = "000938"
MARKET = 0  # 深圳

# ============ 1. 实时行情 ============
print("=" * 60)
print("一、实时行情")
print("=" * 60)

client = Quotes.factory(market='std')

# mootdx 实时报价
quotes = client.quotes(symbol=[CODE])
if quotes is not None and not quotes.empty:
    q = quotes.iloc[0]
    print(f"  现价: {q.get('price', 'N/A')}")
    print(f"  今开/昨收: {q.get('open', 'N/A')} / {q.get('last_close', 'N/A')}")
    print(f"  最高/最低: {q.get('high', 'N/A')} / {q.get('low', 'N/A')}")
    print(f"  成交量: {q.get('vol', 'N/A')}")
    print(f"  成交额: {q.get('amount', 'N/A')}")

# 腾讯行情（PE/PB/市值等）
import urllib.request
prefix = "sz" if not CODE.startswith(("6","9")) else "sh"
url = f"https://qt.gtimg.cn/q={prefix}{CODE}"
req = urllib.request.Request(url)
req.add_header("User-Agent", "Mozilla/5.0")
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode("gbk")
vals = data.split('"')[1].split("~")

name = vals[1]
price = float(vals[3])
last_close = float(vals[4])
open_price = float(vals[5])
change_pct = float(vals[32])
high = float(vals[33])
low = float(vals[34])
amount_wan = float(vals[37])
turnover_pct = float(vals[38])
pe_ttm = float(vals[39])
amplitude = float(vals[43])
mcap_yi = float(vals[44])
float_mcap = float(vals[45])
pb = float(vals[46])
limit_up = float(vals[47])
limit_down = float(vals[48])
vol_ratio = float(vals[49])
pe_static = float(vals[52])

print(f"\n  【{name}】({CODE})")
print(f"  当前价: {price}元 ({change_pct:+.2f}%)")
print(f"  今开/昨收: {open_price} / {last_close}")
print(f"  最高/最低: {high} / {low}")
print(f"  振幅: {amplitude}%")
print(f"  PE(TTM): {pe_ttm:.2f}x")
print(f"  PE(静): {pe_static:.2f}x")
print(f"  PB: {pb:.2f}x")
print(f"  总市值: {mcap_yi:.0f}亿")
print(f"  流通市值: {float_mcap:.0f}亿")
print(f"  换手率: {turnover_pct}%")
print(f"  量比: {vol_ratio}")
print(f"  涨停/跌停: {limit_up} / {limit_down}")

# ============ 2. 财务趋势（近5年年报） ============
print("\n" + "=" * 60)
print("二、财务趋势（近5年年报）")
print("=" * 60)

import akshare as ak

# 东财业绩报表
dates_list = ['20241231', '20231231', '20221231', '20211231', '20201231']
results_fin = []
for d in dates_list:
    try:
        df = ak.stock_yjbb_em(date=d)
        r = df[df['股票代码'] == CODE]
        if not r.empty:
            row = r.iloc[0]
            results_fin.append({
                'date': d,
                'revenue': row.get('营业总收入-营业总收入', 'N/A'),
                'revenue_yoy': row.get('营业总收入-同比增长', 'N/A'),
                'net_profit': row.get('净利润-净利润', 'N/A'),
                'net_profit_yoy': row.get('净利润-同比增长', 'N/A'),
                'eps': row.get('每股收益', 'N/A'),
                'roe': row.get('净资产收益率', 'N/A'),
                'gross_margin': row.get('销售毛利率', 'N/A'),
            })
    except Exception as e:
        print(f"  {d}: 获取失败 {e}")

for r in results_fin:
    print(f"  {r['date']}: 营收={r['revenue']} 同比={r['revenue_yoy']} | "
          f"净利={r['net_profit']} 同比={r['net_profit_yoy']} | "
          f"EPS={r['eps']} ROE={r['roe']} 毛利率={r['gross_margin']}")

# ============ 3. 机构一致预期与估值 ============
print("\n" + "=" * 60)
print("三、机构一致预期与估值")
print("=" * 60)

try:
    df_forecast = ak.stock_profit_forecast_ths(symbol=CODE, indicator="预测年报每股收益")
    if not df_forecast.empty:
        print(f"  机构覆盖情况:")
        eps_data = {}
        for _, row in df_forecast.iterrows():
            year = str(row['年度'])
            count = int(row['预测机构数'])
            eps_mean = row['均值']
            eps_max = row['最大值']
            eps_data[year] = {'count': count, 'mean': eps_mean, 'max': eps_max}
            print(f"    {year}年: {count}家机构, EPS均值={eps_mean}, 最大值={eps_max}")

        # 计算估值
        years_sorted = sorted(eps_data.keys())
        if len(years_sorted) >= 2:
            eps_cur = float(eps_data[years_sorted[0]]['mean'])
            eps_next = float(eps_data[years_sorted[1]]['mean'])
            pe_fwd = price / eps_cur if eps_cur > 0 else float('inf')
            cagr = (eps_next / eps_cur - 1) if eps_cur > 0 else 0
            peg = pe_fwd / (cagr * 100) if cagr > 0 else float('inf')
            digest = math.log(pe_fwd / 30) / math.log(1 + cagr) if pe_fwd > 30 and cagr > 0 else 0

            print(f"\n  前向PE({years_sorted[0]}E): {pe_fwd:.1f}x")
            print(f"  EPS增速(CAGR): {cagr*100:.1f}%")
            print(f"  PEG: {peg:.2f}" if peg != float('inf') else "  PEG: inf")
            print(f"  PE消化到30x需: {digest:.1f}年" if digest > 0 else "  PE消化到30x: 已低于30x")
    else:
        print("  无机构覆盖数据")
except Exception as e:
    print(f"  获取失败: {e}")

# ============ 4. 筹码分布 ============
print("\n" + "=" * 60)
print("四、筹码分布")
print("=" * 60)

try:
    k = client.bars(symbol=CODE, category=4, offset=250)
    if k is not None and not k.empty:
        cp = float(k['close'].iloc[-1])
        chip = {}
        td = len(k)
        half_life = 60

        for idx in range(td):
            row = k.iloc[idx]
            da = td - idx - 1
            decay = float(np.exp(-np.log(2) * da / half_life))
            lo = int(row['low'])
            hi = int(row['high'])
            vol = float(row['vol'])
            nb = max(hi - lo, 1)
            vpb = vol * decay / nb
            for p in range(lo, hi + 1):
                chip[p] = chip.get(p, 0) + vpb

        tc = sum(chip.values())
        wa = sum(p * v for p, v in chip.items()) / tc

        profit_vol = sum(v for p, v in chip.items() if p < cp)
        profit_pct = profit_vol / tc * 100
        loss_pct = 100 - profit_pct

        # 90%集中区
        cum = 0
        p5 = p95 = None
        for p in sorted(chip.keys()):
            cum += chip[p]
            if p5 is None and cum / tc >= 0.05:
                p5 = p
            if cum / tc >= 0.95:
                p95 = p
                break

        # 上方抛压
        above = {p: v for p, v in chip.items() if p > int(cp)}
        below = {p: v for p, v in chip.items() if p < int(cp)}

        pressure_price = pressure_ratio = above_total = None
        if above:
            mp = max(above, key=above.get)
            above_total = sum(above.values()) / tc * 100
            pressure_price = mp
            pressure_ratio = above[mp] / tc * 100

        support_price = support_ratio = below_total = None
        if below:
            ms = max(below, key=below.get)
            below_total = sum(below.values()) / tc * 100
            support_price = ms
            support_ratio = below[ms] / tc * 100

        print(f"  当前价: {cp}")
        print(f"  市场平均成本: {wa:.2f}")
        print(f"  偏离度: {(cp/wa-1)*100:+.1f}%")
        print(f"  获利盘: {profit_pct:.1f}%")
        print(f"  套牢盘: {loss_pct:.1f}%")
        print(f"  90%筹码集中区: {p5}~{p95}")
        print(f"  上方抛压位: {pressure_price}元(占比{pressure_ratio:.1f}%) 上方合计{above_total:.1f}%")
        print(f"  下方支撑位: {support_price}元(占比{support_ratio:.1f}%) 下方合计{below_total:.1f}%")

        # 筹码分布图（精简版，只显示主要区域）
        print(f"\n  筹码分布图:")
        max_vol = max(chip.values())
        # 找到当前价附近的范围
        cp_int = int(round(cp))
        show_range = range(max(cp_int - 15, min(chip.keys())), min(cp_int + 15, max(chip.keys()) + 1))
        for p in sorted(chip.keys()):
            if p not in show_range:
                continue
            pct = chip[p] / tc * 100
            bar_len = int(chip[p] / max_vol * 30)
            bar = "█" * bar_len
            marker = " <=" if abs(p - cp_int) < 1 else ""
            print(f"    {p:3d} | {pct:5.1f}% | {bar}{marker}")

except Exception as e:
    print(f"  筹码分布获取失败: {e}")

# ============ 5. 资金流向 ============
print("\n" + "=" * 60)
print("五、资金流向")
print("=" * 60)

try:
    df_flow = ak.stock_individual_fund_flow(stock=CODE, market="sz")
    if not df_flow.empty:
        df_flow['主力净流入-净额'] = pd.to_numeric(df_flow['主力净流入-净额'], errors='coerce')
        df_flow['超大单净流入-净额'] = pd.to_numeric(df_flow['超大单净流入-净额'], errors='coerce')
        df_flow['大单净流入-净额'] = pd.to_numeric(df_flow['大单净流入-净额'], errors='coerce')

        for d in [5, 10, 20]:
            tail = df_flow.tail(d)
            main_net = tail['主力净流入-净额'].sum() / 1e8
            super_net = tail['超大单净流入-净额'].sum() / 1e8
            large_net = tail['大单净流入-净额'].sum() / 1e8
            pos_days = (tail['主力净流入-净额'] > 0).sum()
            print(f"  近{d}日: 主力净流入{main_net:+.2f}亿 超大单{super_net:+.2f}亿 大单{large_net:+.2f}亿 "
                  f"净流入天数={pos_days}/{d}")

        print(f"\n  近5日资金明细:")
        for _, r in df_flow.tail(5).iterrows():
            date = str(r['日期'])
            close = r['收盘价']
            change = r['涨跌幅']
            main = float(r['主力净流入-净额']) / 1e8 if pd.notna(r['主力净流入-净额']) else 0
            super_v = float(r['超大单净流入-净额']) / 1e8 if pd.notna(r['超大单净流入-净额']) else 0
            large_v = float(r['大单净流入-净额']) / 1e8 if pd.notna(r['大单净流入-净额']) else 0
            print(f"    {date}: 收盘{close} 涨{change}% 主力{main:+.2f}亿 超大单{super_v:+.2f}亿 大单{large_v:+.2f}亿")
except Exception as e:
    print(f"  资金流向获取失败: {e}")

# ============ 6. 技术面 ============
print("\n" + "=" * 60)
print("六、技术面")
print("=" * 60)

try:
    klines = client.bars(symbol=CODE, category=4, offset=120)
    if klines is not None and not klines.empty:
        df_k = pd.DataFrame(klines)
        sdf = StockDataFrame.retype(df_k)

        # MA均线
        df_k['ma5'] = df_k['close'].rolling(5).mean()
        df_k['ma10'] = df_k['close'].rolling(10).mean()
        df_k['ma20'] = df_k['close'].rolling(20).mean()
        df_k['ma60'] = df_k['close'].rolling(60).mean()
        df_k['ma120'] = df_k['close'].rolling(120).mean()

        cur_price = df_k['close'].iloc[-1]
        ma5 = df_k['ma5'].iloc[-1]
        ma10 = df_k['ma10'].iloc[-1]
        ma20 = df_k['ma20'].iloc[-1]
        ma60 = df_k['ma60'].iloc[-1]
        ma120 = df_k['ma120'].iloc[-1] if pd.notna(df_k['ma120'].iloc[-1]) else None

        # MACD
        macd_val = sdf['macd'].iloc[-1]
        signal_val = sdf['macds'].iloc[-1]
        hist_val = sdf['macdh'].iloc[-1]

        # RSI
        rsi_val = sdf['rsi_14'].iloc[-1]

        # BOLL
        boll_ub = sdf['boll_ub'].iloc[-1] if 'boll_ub' in sdf.columns else None
        boll_lb = sdf['boll_lb'].iloc[-1] if 'boll_lb' in sdf.columns else None

        # 均线排列
        ma_list = [ma5, ma10, ma20, ma60]
        is_bullish = all(ma_list[i] > ma_list[i+1] for i in range(len(ma_list)-1) if pd.notna(ma_list[i]) and pd.notna(ma_list[i+1]))
        is_bearish = all(ma_list[i] < ma_list[i+1] for i in range(len(ma_list)-1) if pd.notna(ma_list[i]) and pd.notna(ma_list[i+1]))

        print(f"  当前价: {cur_price:.2f}")
        print(f"  MA5={ma5:.2f} MA10={ma10:.2f} MA20={ma20:.2f} MA60={ma60:.2f}", end="")
        if ma120:
            print(f" MA120={ma120:.2f}")
        else:
            print()
        print(f"  MACD: DIF={macd_val:.4f} DEA={signal_val:.4f} 柱={hist_val:.4f}")
        print(f"  RSI14={rsi_val:.2f}")
        if pd.notna(boll_ub):
            print(f"  BOLL: 上轨={boll_ub:.2f} 下轨={boll_lb:.2f}")

        if is_bullish:
            print(f"  均线排列: 多头排列(看多)")
        elif is_bearish:
            print(f"  均线排列: 空头排列(看空)")
        else:
            print(f"  均线排列: 交叉排列(震荡)")

        # MACD金叉/死叉
        hist_prev = sdf['macdh'].iloc[-2] if len(sdf) > 1 else 0
        if hist_prev < 0 and hist_val > 0:
            print(f"  MACD信号: 金叉(买入)")
        elif hist_prev > 0 and hist_val < 0:
            print(f"  MACD信号: 死叉(卖出)")
        else:
            print(f"  MACD信号: 无交叉")

        if rsi_val > 70:
            print(f"  RSI信号: 超买(注意回调)")
        elif rsi_val < 30:
            print(f"  RSI信号: 超卖(关注反弹)")
        else:
            print(f"  RSI信号: 中性")

        if cur_price > ma20:
            print(f"  站上20日线")
        else:
            print(f"  跌破20日线")
except Exception as e:
    print(f"  技术面获取失败: {e}")

# ============ 7. 研报 ============
print("\n" + "=" * 60)
print("七、研报要点")
print("=" * 60)

try:
    import requests as req_lib
    REPORT_API = "https://reportapi.eastmoney.com/report/list"
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    session = req_lib.Session()
    session.headers.update({"User-Agent": UA, "Referer": "https://data.eastmoney.com/"})

    params = {
        "industryCode": "*", "pageSize": "20", "industry": "*",
        "rating": "*", "ratingChange": "*",
        "beginTime": "2024-01-01", "endTime": "2030-01-01",
        "pageNo": "1", "fields": "", "qType": "0",
        "orgCode": "", "code": CODE, "rcode": "",
        "p": "1", "pageNum": "1", "pageNumber": "1",
    }
    r = session.get(REPORT_API, params=params, timeout=30)
    d = r.json()
    rows = d.get("data") or []

    if rows:
        print(f"  近期研报共 {len(rows)} 篇，展示前10篇:")
        for row in rows[:10]:
            date = (row.get("publishDate") or "")[:10]
            org = row.get("orgSName") or "未知"
            title = (row.get("title") or "")[:50]
            rating = row.get("emRatingName") or ""
            eps_this = row.get("predictThisYearEps") or ""
            eps_next = row.get("predictNextYearEps") or ""
            eps_str = f"EPS(今/明)={eps_this}/{eps_next}" if eps_this or eps_next else ""
            print(f"    {date} | {org} | {rating} | {title}")
            if eps_str:
                print(f"      {eps_str}")
    else:
        print("  无近期研报")
except Exception as e:
    print(f"  研报获取失败: {e}")

# ============ 8. 概念板块 ============
print("\n" + "=" * 60)
print("八、概念板块归属")
print("=" * 60)

try:
    baidu_headers = {
        "Host": "finance.pae.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
        "Accept": "application/vnd.finance-web.v1+json",
        "Origin": "https://gushitong.baidu.com",
        "Referer": "https://gushitong.baidu.com/",
    }
    url = f"https://finance.pae.baidu.com/api/getrelatedblock?code={CODE}&market=ab&typeCode=all&finClientType=pc"
    r = req_lib.get(url, headers=baidu_headers, timeout=10)
    d = r.json()
    if str(d.get("ResultCode", -1)) == "0":
        for block in d.get("Result", []):
            block_type = block.get("type", "")
            items = block.get("list", [])
            names = [item.get("name", "") for item in items[:10]]
            if "行业" in block_type:
                print(f"  行业: {', '.join(names)}")
            elif "概念" in block_type:
                print(f"  概念: {', '.join(names)}")
            elif "地域" in block_type:
                print(f"  地域: {', '.join(names)}")
except Exception as e:
    print(f"  概念板块获取失败: {e}")

# ============ 9. 同行业估值对比 ============
print("\n" + "=" * 60)
print("九、同行业估值对比")
print("=" * 60)

try:
    # 获取同行业个股
    peer_codes = []
    if str(d.get("ResultCode", -1)) == "0":
        for block in d.get("Result", []):
            if "行业" in block.get("type", ""):
                for item in block.get("list", []):
                    c = item.get("code", "")
                    if c and c.isdigit() and len(c) == 6:
                        peer_codes.append(c)

    if peer_codes:
        peer_codes = list(dict.fromkeys(peer_codes))[:30]
        # 腾讯批量行情
        prefixed = []
        for c in peer_codes:
            if c.startswith(("6", "9")):
                prefixed.append(f"sh{c}")
            elif c.startswith("8"):
                prefixed.append(f"bj{c}")
            else:
                prefixed.append(f"sz{c}")

        url_q = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
        req_q = urllib.request.Request(url_q)
        req_q.add_header("User-Agent", "Mozilla/5.0")
        resp_q = urllib.request.urlopen(req_q, timeout=10)
        data_q = resp_q.read().decode("gbk")

        peers = []
        for line in data_q.strip().split(";"):
            if not line.strip() or "=" not in line or '"' not in line:
                continue
            key = line.split("=")[0].split("_")[-1]
            v = line.split('"')[1].split("~")
            if len(v) < 53:
                continue
            c = key[2:]
            pe = float(v[39]) if v[39] else 0
            pb_v = float(v[46]) if v[46] else 0
            nm = v[1]
            mc = float(v[44]) if v[44] else 0
            pr = float(v[3]) if v[3] else 0
            chg = float(v[32]) if v[32] else 0
            if pe > 0:
                peers.append({
                    "code": c, "name": nm, "price": pr,
                    "pe": pe, "pb": pb_v, "mcap": mc,
                    "change_pct": chg, "is_target": c == CODE,
                })

        if peers:
            df_peers = pd.DataFrame(peers)
            pe_mean = df_peers['pe'].mean()
            pe_median = df_peers['pe'].median()
            pb_mean = df_peers['pb'].mean()
            pb_median = df_peers['pb'].median()

            target = next((p for p in peers if p['is_target']), None)
            if target:
                pe_rank = sorted(peers, key=lambda x: x['pe']).index(target) + 1
                print(f"  {target['name']}({target['code']}): PE={target['pe']:.1f}x PB={target['pb']:.2f}x")
                print(f"  行业PE均值={pe_mean:.1f} 中位数={pe_median:.1f}")
                print(f"  行业PB均值={pb_mean:.2f} 中位数={pb_median:.2f}")
                print(f"  PE排名: {pe_rank}/{len(peers)}")
                print(f"  相对行业PE中位数: {((target['pe']/pe_median-1)*100):+.1f}%")

            print(f"\n  同行业PE排名(前10):")
            for i, p in enumerate(sorted(peers, key=lambda x: x['pe'])[:10], 1):
                marker = " ★" if p['is_target'] else ""
                print(f"    {i}. {p['code']} {p['name']}: PE={p['pe']:.1f}x PB={p['pb']:.2f}x 市值={p['mcap']:.0f}亿{marker}")
except Exception as e:
    print(f"  同行业对比获取失败: {e}")

# ============ 10. 基础数据 ============
print("\n" + "=" * 60)
print("十、基础数据 (F10)")
print("=" * 60)

try:
    # 公司概况
    text = client.F10(symbol=CODE, name="公司概况")
    if text:
        lines = text.strip().split("\n")
        for line in lines[:15]:
            print(f"  {line.strip()}")
except Exception as e:
    print(f"  F10获取失败: {e}")

print("\n" + "=" * 60)
print("分析完成!")
print("=" * 60)

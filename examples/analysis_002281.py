# -*- coding: utf-8 -*-
import urllib.request
import akshare as ak
import pandas as pd
import numpy as np
from mootdx.quotes import Quotes
from stockstats import StockDataFrame

code = '002281'
prefix = 'sz'

# ============ 1. 腾讯实时行情 ============
print("=" * 60)
print("1. 实时行情（腾讯财经）")
print("=" * 60)
url = f'https://qt.gtimg.cn/q={prefix}{code}'
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')
vals = data.split('"')[1].split('~')
print(f"名称: {vals[1]}")
print(f"当前价: {vals[3]}")
print(f"昨收: {vals[4]}")
print(f"今开: {vals[5]}")
print(f"涨跌额: {vals[31]}")
print(f"涨跌幅: {vals[32]}%")
print(f"最高: {vals[33]}")
print(f"最低: {vals[34]}")
print(f"成交额(万): {vals[37]}")
print(f"换手率: {vals[38]}%")
print(f"PE(TTM): {vals[39]}")
print(f"振幅: {vals[43]}%")
print(f"总市值(亿): {vals[44]}")
print(f"流通市值(亿): {vals[45]}")
print(f"PB: {vals[46]}")
print(f"涨停价: {vals[47]}")
print(f"跌停价: {vals[48]}")
print(f"量比: {vals[49]}")
print(f"PE(静): {vals[52]}")

# ============ 2. 财务快照 ============
print("\n" + "=" * 60)
print("2. 财务快照（mootdx）")
print("=" * 60)
c = Quotes.factory(market='std')
fin = c.finance(symbol=code)
if fin is not None and len(fin) > 0:
    key_fields = ['eps', 'bvps', 'roe', 'profit', 'income',
                  'liutongguben', 'zongguben', 'meigugongjijin',
                  'meiguweifeipeili', 'meigujingzichan']
    for col in fin.columns:
        v = fin[col].iloc[0]
        print(f"  {col} = {v}")

# ============ 3. 资金流向 ============
print("\n" + "=" * 60)
print("3. 资金流向（akshare）")
print("=" * 60)
df = ak.stock_individual_fund_flow(stock=code, market='sz')
df['主力净流入-净额'] = pd.to_numeric(df['主力净流入-净额'], errors='coerce')
df['超大单净流入-净额'] = pd.to_numeric(df['超大单净流入-净额'], errors='coerce')
df['大单净流入-净额'] = pd.to_numeric(df['大单净流入-净额'], errors='coerce')
df['收盘价'] = pd.to_numeric(df['收盘价'], errors='coerce')
df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')

d5 = df.tail(5)
d10 = df.tail(10)
d20 = df.tail(20)
for label, d in [('5日', d5), ('10日', d10), ('20日', d20)]:
    mv = d['主力净流入-净额'].sum()
    sv = d['超大单净流入-净额'].sum()
    lv = d['大单净流入-净额'].sum()
    pos = (d['主力净流入-净额'] > 0).sum()
    print(f"{label}: 主力{mv/1e8:.2f}亿 超大单{sv/1e8:.2f}亿 大单{lv/1e8:.2f}亿 净流入天数={pos}/{len(d)}")

print("\n近5日资金流向明细:")
for _, r in d5.iterrows():
    print(f"  {r['日期']} 收盘{r['收盘价']:.2f} 涨{r['涨跌幅']:.2f}% 主力{r['主力净流入-净额']/1e8:.2f}亿 超大单{r['超大单净流入-净额']/1e8:.2f}亿 大单{r['大单净流入-净额']/1e8:.2f}亿")

print("\n近20日资金流向:")
for _, r in df.tail(20).iterrows():
    print(f"  {r['日期']} 收盘{r['收盘价']:.2f} 涨{r['涨跌幅']:.2f}% 主力{r['主力净流入-净额']/1e8:.2f}亿 超大单{r['超大单净流入-净额']/1e8:.2f}亿 大单{r['大单净流入-净额']/1e8:.2f}亿")

# ============ 4. 筹码分布 ============
print("\n" + "=" * 60)
print("4. 筹码分布（mootdx K线 + 指数衰减算法）")
print("=" * 60)
k = c.bars(symbol=code, category=4, offset=250)
cp = float(k['close'].iloc[-1])
chip = {}
td = len(k)
for idx in range(td):
    row = k.iloc[idx]
    da = td - idx - 1
    decay = float(np.exp(-np.log(2) * da / 60))
    lo = int(row['low'])
    hi = int(row['high'])
    vol = float(row['vol'])
    nb = max(hi - lo, 1)
    vpb = vol * decay / nb
    for p in range(lo, hi + 1):
        chip[p] = chip.get(p, 0) + vpb

tc = sum(chip.values())
wa = sum(p * v for p, v in chip.items()) / tc
pc = sum(v for p, v in chip.items() if p < cp)
pf = pc / tc * 100

print(f"当前价: {cp:.2f}")
print(f"市场平均成本: {wa:.2f}")
print(f"偏离度: {(cp/wa-1)*100:.1f}%")
print(f"获利盘比例: {pf:.1f}%")
print(f"套牢盘比例: {100-pf:.1f}%")

cum = 0
p5 = p95 = None
for p in sorted(chip.keys()):
    cum += chip[p]
    if p5 is None and cum / tc >= 0.05:
        p5 = p
    if cum / tc >= 0.95:
        p95 = p
        break
print(f"90%筹码集中区: {p5}~{p95}")

mv2 = max(chip.values())
print("\n筹码分布图:")
for bk in sorted(chip.keys()):
    vol2 = chip[bk]
    pct = vol2 / tc * 100
    bl = int(vol2 / mv2 * 30)
    mk = " <=" if abs(bk - round(cp)) < 1 else ""
    print("%5d | %5.1f%% | %s%s" % (bk, pct, chr(9608) * bl, mk))

above = {p: v for p, v in chip.items() if p > int(cp)}
below = {p: v for p, v in chip.items() if p < int(cp)}
if above:
    mp = max(above, key=above.get)
    at = sum(above.values()) / tc * 100
    print(f"上方抛压位: {mp}元 (占比{above[mp]/tc*100:.1f}%) 上方合计{at:.1f}%")
if below:
    ms = max(below, key=below.get)
    bt = sum(below.values()) / tc * 100
    print(f"下方支撑位: {ms}元 (占比{below[ms]/tc*100:.1f}%) 下方合计{bt:.1f}%")

for days, label in [(5, '5日'), (20, '20日'), (60, '60日')]:
    c2 = k.tail(days)
    avg = (c2['close'] * c2['vol']).sum() / c2['vol'].sum()
    print(f"{label}均价: {avg:.2f} 偏离: {(cp/avg-1)*100:.1f}%")

# ============ 5. 技术面 ============
print("\n" + "=" * 60)
print("5. 技术面（MA/MACD/RSI/BOLL）")
print("=" * 60)
klines = c.bars(symbol=code, category=4, offset=120)
if klines is not None and not klines.empty:
    df_tech = pd.DataFrame(klines)
    sdf = StockDataFrame.retype(df_tech)

    macd_val = sdf['macd'].iloc[-1]
    signal_val = sdf['macds'].iloc[-1]
    hist_val = sdf['macdh'].iloc[-1]
    rsi_val = sdf['rsi_14'].iloc[-1]
    boll_ub = sdf['boll_ub'].iloc[-1] if 'boll_ub' in sdf.columns else None
    boll_lb = sdf['boll_lb'].iloc[-1] if 'boll_lb' in sdf.columns else None

    df_tech['ma5'] = df_tech['close'].rolling(5).mean()
    df_tech['ma10'] = df_tech['close'].rolling(10).mean()
    df_tech['ma20'] = df_tech['close'].rolling(20).mean()
    df_tech['ma60'] = df_tech['close'].rolling(60).mean()
    df_tech['ma120'] = df_tech['close'].rolling(120).mean()

    price = df_tech['close'].iloc[-1]
    print(f"当前价: {price:.2f}")
    for ma in ['ma5', 'ma10', 'ma20', 'ma60', 'ma120']:
        v = df_tech[ma].iloc[-1]
        if pd.notna(v):
            dev = (price / v - 1) * 100
            print(f"  {ma}: {v:.2f} (偏离{dev:+.1f}%)")
        else:
            print(f"  {ma}: N/A")

    print(f"\nMACD: {macd_val:.4f}")
    print(f"Signal: {signal_val:.4f}")
    print(f"Hist: {hist_val:.4f}")
    hist_prev = sdf['macdh'].iloc[-2] if len(sdf) > 1 else 0
    if hist_prev < 0 and hist_val > 0:
        print("  → MACD金叉!")
    elif hist_prev > 0 and hist_val < 0:
        print("  → MACD死叉!")

    print(f"\nRSI14: {rsi_val:.2f}")
    if rsi_val > 70:
        print("  → 超买区间，注意回调风险")
    elif rsi_val < 30:
        print("  → 超卖区间，关注反弹机会")

    if boll_ub and pd.notna(boll_ub):
        print(f"\nBOLL: 上轨={boll_ub:.2f} 下轨={boll_lb:.2f}")
        if price > boll_ub:
            print("  → 突破布林上轨")
        elif price < boll_lb:
            print("  → 跌破布林下轨")

    # 均线排列判断
    ma_list = [df_tech[f'ma{n}'].iloc[-1] for n in [5, 10, 20, 60]]
    if all(pd.notna(m) for m in ma_list):
        if all(ma_list[i] > ma_list[i+1] for i in range(len(ma_list)-1)):
            print("\n均线排列: 多头排列(看多)")
        elif all(ma_list[i] < ma_list[i+1] for i in range(len(ma_list)-1)):
            print("\n均线排列: 空头排列(看空)")
        else:
            print("\n均线排列: 交叉排列(震荡)")

# ============ 6. 机构一致预期 ============
print("\n" + "=" * 60)
print("6. 机构一致预期EPS")
print("=" * 60)
try:
    df_eps = ak.stock_profit_forecast_ths(symbol=code, indicator="预测年报每股收益")
    if not df_eps.empty:
        print(df_eps.to_string())
    else:
        print("无机构覆盖数据")
except Exception as e:
    print(f"获取失败: {e}")

# ============ 7. 财务趋势 ============
print("\n" + "=" * 60)
print("7. 近3年财务趋势")
print("=" * 60)
try:
    df_fin = ak.stock_financial_abstract_ths(symbol=code)
    if not df_fin.empty:
        df_annual = df_fin[df_fin['报告期'].str.contains('12-31')].head(3)
        for _, row in df_annual.iterrows():
            print(f"  {row['报告期']}: 营收={row.get('营业总收入','N/A')} (+{row.get('营业总收入同比增长率','N/A')}) | "
                  f"净利={row.get('净利润','N/A')} (+{row.get('净利润同比增长率','N/A')}) | "
                  f"ROE={row.get('净资产收益率','N/A')} 毛利率={row.get('销售毛利率','N/A')}")
    else:
        print("无财务趋势数据")
except Exception as e:
    print(f"获取失败: {e}")

# ============ 8. 研报 ============
print("\n" + "=" * 60)
print("8. 最近研报")
print("=" * 60)
try:
    import requests
    REPORT_API = "https://reportapi.eastmoney.com/report/list"
    UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Referer": "https://data.eastmoney.com/"})
    params = {
        "industryCode": "*", "pageSize": "10", "industry": "*",
        "rating": "*", "ratingChange": "*",
        "beginTime": "2000-01-01", "endTime": "2030-01-01",
        "pageNo": "1", "fields": "", "qType": "0",
        "orgCode": "", "code": code, "rcode": "",
        "p": "1", "pageNum": "1", "pageNumber": "1",
    }
    r = session.get(REPORT_API, params=params, timeout=30)
    d = r.json()
    rows = d.get("data") or []
    print(f"共 {len(rows)} 篇研报（最近10篇）:")
    for rec in rows[:10]:
        eps_cur = rec.get('predictThisYearEps', 'N/A')
        eps_next = rec.get('predictNextYearEps', 'N/A')
        rating = rec.get('emRatingName', 'N/A')
        print(f"  {rec.get('publishDate','')[:10]} | {rec.get('orgSName','')} | {rec.get('title','')[:50]} | 评级:{rating} | EPS(今/明):{eps_cur}/{eps_next}")
except Exception as e:
    print(f"获取失败: {e}")

# ============ 9. 概念板块 ============
print("\n" + "=" * 60)
print("9. 概念板块归属")
print("=" * 60)
try:
    import requests as rq
    headers = {
        "Host": "finance.pae.baidu.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
        "Accept": "application/vnd.finance-web.v1+json",
        "Origin": "https://gushitong.baidu.com",
        "Referer": "https://gushitong.baidu.com/",
    }
    url2 = f"https://finance.pae.baidu.com/api/getrelatedblock?code={code}&market=ab&typeCode=all&finClientType=pc"
    r2 = rq.get(url2, headers=headers, timeout=10)
    d2 = r2.json()
    if str(d2.get("ResultCode", -1)) == "0":
        for block in d2.get("Result", []):
            btype = block.get("type", "")
            items = block.get("list", [])
            names = [it.get("name", "") for it in items[:15]]
            print(f"  {btype}: {', '.join(names)}")
    else:
        print("获取失败")
except Exception as e:
    print(f"获取失败: {e}")

print("\n===== 分析完成 =====")

#!/usr/bin/env python3
import akshare as ak
import pandas as pd
import numpy as np
from mootdx.quotes import Quotes

CODE = "600522"

# === 1. 资金流向 ===
print("=" * 80)
print("1. 资金流向趋势 (东财)")
print("=" * 80)
df = ak.stock_individual_fund_flow(stock=CODE, market="sh")
df['主力净流入-净额'] = pd.to_numeric(df['主力净流入-净额'], errors='coerce')
df['超大单净流入-净额'] = pd.to_numeric(df['超大单净流入-净额'], errors='coerce')
df['大单净流入-净额'] = pd.to_numeric(df['大单净流入-净额'], errors='coerce')
df['主力净流入-净占比'] = pd.to_numeric(df['主力净流入-净占比'], errors='coerce')

recent20 = df.tail(20)
print(f"\n{'日期':>12} {'收盘':>6} {'涨跌%':>6} {'主力(亿)':>10} {'占比%':>6} {'超大单(亿)':>10} {'大单(亿)':>10}")
print("-" * 75)
for _, row in recent20.iterrows():
    m = row['主力净流入-净额']/1e8
    s = row['超大单净流入-净额']/1e8
    b = row['大单净流入-净额']/1e8
    print(f"{str(row['日期']):>12} {row['收盘价']:>6} {row['涨跌幅']:>6.2f} {m:>+10.2f} {row['主力净流入-净占比']:>6.2f} {s:>+10.2f} {b:>+10.2f}")

for n, label in [(5, "5日"), (10, "10日"), (20, "20日")]:
    c = df.tail(n)
    ms = c['主力净流入-净额'].sum()/1e8
    ss = c['超大单净流入-净额'].sum()/1e8
    bs = c['大单净流入-净额'].sum()/1e8
    ap = c['主力净流入-净占比'].mean()
    ud = len(c[c['主力净流入-净额']>0])
    print(f"\n近{label}: 主力={ms:+.2f}亿 超大单={ss:+.2f}亿 大单={bs:+.2f}亿 占比均值={ap:+.2f}% 净流入天数={ud}/{n}")

m5 = df.tail(5)['主力净流入-净额'].sum()
m20 = df.tail(20)['主力净流入-净额'].sum()
if m5 > 0 and m20 > 0:
    trend = "主力持续净流入，资金面强势"
elif m5 < 0 and m20 < 0:
    trend = "主力持续净流出，资金面弱势"
elif m5 < 0 and m20 > 0:
    trend = "主力近期由流入转流出，资金面转弱"
else:
    trend = "主力近期由流出转流入，资金面转强"
print(f"\n资金趋势: {trend}")

# === 2. 筹码分布 ===
print("\n" + "=" * 80)
print("2. 筹码分布估算 (K线+成交量 指数衰减模型)")
print("=" * 80)

client = Quotes.factory(market='std')
klines = client.bars(symbol=CODE, category=4, offset=250)
if klines is not None:
    df_k = pd.DataFrame(klines)
    cp = df_k['close'].iloc[-1]
    
    chip = {}
    td = len(df_k)
    for i, row in df_k.iterrows():
        da = td - i - 1
        decay = np.exp(-np.log(2) * da / 60)
        lo, hi, vol = row['low'], row['high'], row['vol']
        if hi <= lo:
            pk = round(lo, 0)
            chip[pk] = chip.get(pk, 0) + vol * decay
        else:
            nb = max(int(hi - lo), 1)
            vpb = vol * decay / nb
            for p_val in range(int(lo), int(hi)+1):
                chip[p_val] = chip.get(p_val, 0) + vpb
    
    tc = sum(chip.values())
    pc = sum(v for p, v in chip.items() if p < cp)
    lc = sum(v for p, v in chip.items() if p > cp)
    wa = sum(p * v for p, v in chip.items()) / tc
    
    print(f"当前价: {cp:.2f}元")
    print(f"加权平均成本: {wa:.2f}元 (偏离 {(cp/wa-1)*100:+.1f}%)")
    print(f"获利盘: {pc/tc*100:.1f}%  套牢盘: {lc/tc*100:.1f}%")
    
    cum = 0
    p5 = p95 = None
    for p in sorted(chip.keys()):
        cum += chip[p]
        pct = cum / tc * 100
        if p5 is None and pct >= 5: p5 = p
        if pct >= 95: p95 = p; break
    print(f"90%筹码集中区间: {p5} ~ {p95}元")
    
    print(f"\n筹码分布图 (当前价={cp:.2f}元):")
    print(f"{'价位':>6} | {'占比':>5} | 分布")
    print("-" * 60)
    mv = max(chip.values())
    for bk in sorted(chip.keys()):
        vol = chip[bk]
        pct = vol / tc * 100
        bl = int(vol / mv * 35)
        mk = " <=" if abs(bk - round(cp)) < 1 else ""
        bar = chr(9608) * bl
        print(f"{bk:>5}元 | {pct:>5.1f}% | {bar}{mk}")
    
    above = {p: v for p, v in chip.items() if p > int(cp)}
    below = {p: v for p, v in chip.items() if p < int(cp)}
    if above:
        mp = max(above, key=above.get)
        at = sum(above.values())/tc*100
        print(f"\n上方最大压力: {mp}元 (占比{above[mp]/tc*100:.1f}%) 套牢总量{at:.1f}%")
    if below:
        ms2 = max(below, key=below.get)
        bt = sum(below.values())/tc*100
        print(f"下方最强支撑: {ms2}元 (占比{below[ms2]/tc*100:.1f}%) 获利总量{bt:.1f}%")
    
    for days, label in [(5, "5日"), (20, "20日"), (60, "60日")]:
        c = df_k.tail(days)
        avg = (c['close'] * c['vol']).sum() / c['vol'].sum()
        print(f"{label}成交均价: {avg:.2f}元 (偏离{(cp/avg-1)*100:+.1f}%)")

print("\n完成")

"""半导体行业综合性价比分析：估值+增速+资金+机构覆盖"""
import urllib.request
import requests
import pandas as pd
import akshare as ak
import time

print("=" * 80)
print("半导体行业综合性价比分析")
print("维度：PE/PB估值 + 一致预期EPS增速 + PEG + 资金流向 + 机构覆盖")
print("=" * 80)

# ============ 1. 重点半导体股（大市值+中小市值潜力股）============
SEMI_FOCUS = [
    # 大市值龙头
    "688981",  # 中芯国际
    "002371",  # 北方华创
    "688012",  # 中微公司
    "688041",  # 海光信息
    "688008",  # 澜起科技
    "603501",  # 豪威集团
    "600584",  # 长电科技
    "002156",  # 通富微电
    "688396",  # 华润微
    "688082",  # 盛美上海
    # 中市值
    "688187",  # 时代电气
    "002049",  # 紫光国微
    "603160",  # 汇顶科技
    "002409",  # 雅克科技
    "688200",  # 华峰测控
    "688120",  # 华海清科
    "688072",  # 拓荆科技
    "300666",  # 江丰电子
    "300604",  # 长川科技
    "688122",  # 西部超导
    "300223",  # 北京君正
    "688536",  # 思瑞浦
    "688009",  # 中国通号
    "300454",  # 深信服
    "688131",  # 皓元医药
]

# ============ 2. 腾讯批量行情 ============
def tencent_quote_batch(codes):
    all_result = {}
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
    resp = urllib.request.urlopen(req, timeout=15)
    data = resp.read().decode("gbk")
    
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 53:
            continue
        code = key[2:]
        try:
            all_result[code] = {
                "name": vals[1],
                "price": float(vals[3]) if vals[3] else 0,
                "change_pct": float(vals[32]) if vals[32] else 0,
                "pe_ttm": float(vals[39]) if vals[39] else 0,
                "pb": float(vals[46]) if vals[46] else 0,
                "mcap_yi": float(vals[44]) if vals[44] else 0,
                "turnover": float(vals[38]) if vals[38] else 0,
            }
        except:
            continue
    return all_result

print("\n[1/4] 拉取实时行情...")
quotes = tencent_quote_batch(SEMI_FOCUS)
print(f"  获取 {len(quotes)} 只股票行情")

# ============ 3. 一致预期EPS + PEG ============
print("\n[2/4] 拉取机构一致预期EPS（可能需要1-2分钟）...")

eps_data = {}
for code in SEMI_FOCUS:
    try:
        df = ak.stock_profit_forecast_ths(symbol=code, indicator="预测年报每股收益")
        if df is not None and not df.empty:
            rows = df.to_dict("records")
            eps_data[code] = rows
    except:
        pass
    time.sleep(0.5)

print(f"  获取 {len(eps_data)} 只股票的一致预期")

# ============ 4. 百度资金流向（20日历史）============
print("\n[3/4] 拉取20日资金流向...")

BAIDU_HEADERS = {
    "Host": "finance.pae.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
    "Accept": "application/vnd.finance-web.v1+json",
    "Origin": "https://gushitong.baidu.com",
    "Referer": "https://gushitong.baidu.com/",
}

fund_flow = {}
for code in SEMI_FOCUS:
    try:
        url = f"https://finance.pae.baidu.com/vapi/v1/fundsortlist?code={code}&market=ab&pn=0&rn=20&finClientType=pc"
        r = requests.get(url, headers=BAIDU_HEADERS, timeout=10)
        d = r.json()
        if str(d.get("ResultCode", -1)) != "0":
            continue
        items = d.get("Result", {}).get("list", [])
        if items:
            total_main = sum(float(it.get("netAmount", 0)) for it in items[:10] if it.get("netAmount"))
            fund_flow[code] = {
                "main_10d": total_main / 10000,  # 万元转亿
                "days": len(items),
            }
    except:
        pass
    time.sleep(0.3)

print(f"  获取 {len(fund_flow)} 只股票的资金流向")

# ============ 5. 东财研报覆盖 ============
print("\n[4/4] 拉取研报覆盖数...")

report_count = {}
for code in SEMI_FOCUS[:15]:  # 只查前15只重点
    try:
        url = "https://reportapi.eastmoney.com/report/list"
        params = {
            "industryCode": "*", "pageSize": "10", "industry": "*",
            "rating": "*", "ratingChange": "*",
            "beginTime": "2025-01-01", "endTime": "2030-01-01",
            "pageNo": "1", "fields": "", "qType": "0",
            "orgCode": "", "code": code, "rcode": "", "p": "1",
            "pageNum": "1", "pageNumber": "1",
        }
        r = requests.get(url, params=params, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"})
        d = r.json()
        total = d.get("hits", 0)
        # 取最近研报评级
        records = d.get("data") or []
        latest_rating = records[0].get("emRatingName", "") if records else ""
        report_count[code] = {"total": total, "latest_rating": latest_rating}
    except:
        pass
    time.sleep(0.3)

print(f"  获取 {len(report_count)} 只股票的研报覆盖")

# ============ 6. 综合分析 ============
print("\n" + "=" * 80)
print("综合分析结果")
print("=" * 80)

results = []
for code, q in quotes.items():
    if q["pe_ttm"] <= 0 or q["mcap_yi"] < 50:
        continue
    
    row = {
        "code": code,
        "name": q["name"],
        "price": q["price"],
        "pe_ttm": q["pe_ttm"],
        "pb": q["pb"],
        "mcap_yi": q["mcap_yi"],
        "change_pct": q["change_pct"],
        "turnover": q["turnover"],
    }
    
    # 一致预期EPS → 算增速和PEG
    if code in eps_data:
        eps_rows = eps_data[code]
        # 找2025和2026的预测EPS
        eps_by_year = {}
        for er in eps_rows:
            year = str(er.get("年度", ""))
            avg = er.get("均值", 0)
            org_count = er.get("预测机构数", 0)
            if avg and org_count and org_count >= 3:
                try:
                    eps_by_year[year] = {"eps": float(avg), "orgs": int(org_count)}
                except:
                    pass
        
        # 算增速
        years_sorted = sorted(eps_by_year.keys(), reverse=True)
        if len(years_sorted) >= 2:
            latest = eps_by_year[years_sorted[0]]
            prev = eps_by_year[years_sorted[1]]
            if prev["eps"] > 0:
                growth = (latest["eps"] - prev["eps"]) / prev["eps"] * 100
                row["eps_growth"] = round(growth, 1)
                row["eps_latest_year"] = years_sorted[0]
                row["eps_prev_year"] = years_sorted[1]
                row["eps_latest"] = latest["eps"]
                row["eps_prev"] = prev["eps"]
                row["org_count"] = latest["orgs"]
                
                # PEG = PE / 增速
                if growth > 0:
                    row["peg"] = round(q["pe_ttm"] / growth, 2)
                
                # 前向PE（用最新预测EPS）
                if latest["eps"] > 0:
                    row["forward_pe"] = round(q["price"] / latest["eps"], 1)
    
    # 资金流向
    if code in fund_flow:
        row["main_flow_10d_yi"] = round(fund_flow[code]["main_10d"], 2)
    
    # 研报覆盖
    if code in report_count:
        row["report_count"] = report_count[code]["total"]
        row["latest_rating"] = report_count[code]["latest_rating"]
    
    results.append(row)

df = pd.DataFrame(results)

# ============ 7. 输出 ============
print("\n### 一、估值+增速+PEG 综合表")
print(f"(仅显示有一致预期数据的股票)")
df_eps = df[df["eps_growth"].notna()].sort_values("peg")

print(f"\n{'代码':<8} {'名称':<8} {'价格':>6} {'PE':>6} {'前向PE':>6} {'PB':>5} {'市值亿':>7} {'EPS增速%':>8} {'PEG':>5} {'机构数':>5} {'涨幅%':>6}")
print("-" * 90)
for _, r in df_eps.iterrows():
    peg_str = f"{r['peg']:.2f}" if pd.notna(r.get('peg')) else "N/A"
    fpe_str = f"{r['forward_pe']:.1f}" if pd.notna(r.get('forward_pe')) else "N/A"
    print(f"{r['code']:<8} {r['name']:<8} {r['price']:>6.1f} {r['pe_ttm']:>6.1f} {fpe_str:>6} {r['pb']:>5.2f} {r['mcap_yi']:>7.0f} {r['eps_growth']:>8.1f} {peg_str:>5} {r['org_count']:>5.0f} {r['change_pct']:>6.2f}")

print("\n### 二、PEG解读")
print("PEG < 1.0 → 估值低于增速，性价比高")
print("PEG 1.0-1.5 → 估值合理")
print("PEG > 1.5 → 估值偏高")

low_peg = df_eps[df_eps["peg"] < 1.5]
if not low_peg.empty:
    print(f"\nPEG < 1.5 的股票（{len(low_peg)} 只）：")
    for _, r in low_peg.sort_values("peg").iterrows():
        flow_str = ""
        if pd.notna(r.get('main_flow_10d_yi')):
            flow_str = f"  资金10日: {r['main_flow_10d_yi']:.2f}亿"
        rating_str = ""
        if r.get('latest_rating'):
            rating_str = f"  最新评级: {r['latest_rating']}"
        print(f"  {r['code']} {r['name']}: PE={r['pe_ttm']:.1f} 前向PE={r.get('forward_pe','N/A')} 增速={r['eps_growth']:.1f}% PEG={r['peg']:.2f} 市值={r['mcap_yi']:.0f}亿{flow_str}{rating_str}")

print("\n### 三、资金流向 + 估值双维度")
print(f"\n{'代码':<8} {'名称':<8} {'PE':>6} {'PEG':>5} {'市值亿':>7} {'10日主力净流入(亿)':>16} {'涨幅%':>6}")
print("-" * 70)
df_flow = df[df["main_flow_10d_yi"].notna()].sort_values("main_flow_10d_yi", ascending=False)
for _, r in df_flow.iterrows():
    peg_str = f"{r['peg']:.2f}" if pd.notna(r.get('peg')) else "N/A"
    print(f"{r['code']:<8} {r['name']:<8} {r['pe_ttm']:>6.1f} {peg_str:>5} {r['mcap_yi']:>7.0f} {r['main_flow_10d_yi']:>16.2f} {r['change_pct']:>6.2f}")

print("\n### 四、无一致预期但估值偏低的股票")
df_no_eps = df[df["eps_growth"].isna() & (df["pe_ttm"] < 80) & (df["mcap_yi"] > 100)]
if not df_no_eps.empty:
    print(f"\n{'代码':<8} {'名称':<8} {'PE':>6} {'PB':>5} {'市值亿':>7} {'涨幅%':>6}")
    print("-" * 50)
    for _, r in df_no_eps.sort_values("pe_ttm").iterrows():
        print(f"{r['code']:<8} {r['name']:<8} {r['pe_ttm']:>6.1f} {r['pb']:>5.2f} {r['mcap_yi']:>7.0f} {r['change_pct']:>6.2f}")
else:
    print("  无")

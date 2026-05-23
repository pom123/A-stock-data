#!/usr/bin/env python3
"""a-stock-data 环境依赖检查脚本"""
import sys

deps = {
    'mootdx':    ('mootdx.quotes',     'mootdx'),
    'akshare':   ('akshare',           'akshare'),
    'requests':  ('requests',          'requests'),
    'pandas':    ('pandas',            'pandas'),
    'stockstats':('stockstats',        'stockstats'),
    'numpy':     ('numpy',             'numpy'),
}

print("a-stock-data 依赖检查")
print("=" * 40)

failed = []
for name, (mod, pkg) in deps.items():
    try:
        __import__(mod.split('.')[0])
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} — pip install {pkg}")
        failed.append(pkg)

# 可选依赖
print("\n可选依赖:")
try:
    import os
    key = os.environ.get("IWENCAI_API_KEY", "")
    if key:
        print(f"  ✅ IWENCAI_API_KEY 已配置")
    else:
        print(f"  ⚠️  IWENCAI_API_KEY 未配置（iwencai语义搜索不可用，其他功能不受影响）")
except:
    pass

print("\n" + "=" * 40)
if failed:
    print(f"❌ 缺少 {len(failed)} 个依赖，请运行: pip install {' '.join(failed)}")
    sys.exit(1)
else:
    print("✅ 所有依赖已安装，环境就绪！")

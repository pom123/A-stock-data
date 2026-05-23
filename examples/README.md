# examples/

本目录包含示例脚本，**非 Skill 运行时依赖**。

Agent 加载 SKILL.md 后会直接使用其中内嵌的代码段，无需引用本目录下的任何文件。

## 文件说明

| 文件 | 说明 |
|------|------|
| `analysis_000938.py` | 紫光股份全栈分析示例（行情+财务+估值+筹码+资金+技术面+研报） |
| `analysis_002050.py` | 三花智控全栈分析示例 |
| `analysis_002281.py` | 光迅科技全栈分析示例 |
| `analysis_600893.py` | 航发动力全栈分析示例 |
| `analysis_chip_fund.py` | 筹码+资金流联合分析示例（对应 SKILL.md 的 `chip_and_fund_analysis()`） |

> **注意**：`chip.py`、`chip2.py`、`chip3.py` 为筹码分布算法的迭代版本，最终版已内化到 SKILL.md 的 `chip_distribution()` 函数中，已从本目录移除。

## 运行方式

```bash
# 确保依赖已安装
pip install mootdx akshare requests pandas stockstats

# 运行示例
python analysis_000938.py
```

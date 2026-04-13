# 🧠 大语言模型强化学习算法 · 深度知识库

> **从 TRPO 到 GRPO，把大模型 RL 的每一个公式都讲透。**

---

## ✨ 这是什么？

这是一份**专为工程师和研究者打造的大模型强化学习（RLHF）系统性笔记**，覆盖从数学理论到工程实践的完整链路。

不是论文摘要，不是科普读物。每一个公式都有来龙去脉，每一个算法都有工程直觉。

---

## 📖 内容速览

### 🔢 第一章：理论基础

把 RL 的数学底层**彻底拆开**——

- **MDP 建模**：LLM 是如何被抽象成马尔可夫决策过程的
- **$J(\pi)$**：轨迹式 vs 分布式，两种视角推导期望回报函数
- **$d_\pi(s)$**：足迹热力图，理解分布偏移为什么让训练崩掉
- **$A(s,a)$**：优势函数、TD Error、为什么 PPO 离不开它
- **重要性采样**：旧数据怎么"撑起"新模型的更新
- **KL 散度**：防止模型"刷分跑偏"的数学防线
- **PDL 引理**：从全局目标 $J(\pi)$ 到可求解的局部替代 $L(\pi)$，核心推导

### ⚔️ 第二章：算法演进史诗

从数学家到工程师，从 2015 到 2024，一条清晰的进化路线——

| 算法 | 年份 | 一句话核心 |
|------|------|------------|
| **TRPO** | 2015 | 用 KL 散度建硬围栏，但算二阶导数太贵了 |
| **PPO** | 2017 | 不建围栏，直接在 Loss 上加限速器（Clip）|
| **DPO** | 2023 | 直接优化偏好，绕过整个 RL 训练循环 |
| **GRPO** | 2024 | 干掉 Critic，组内竞争替代价值估算（DeepSeek-R1）|
| **SAPO/GSPO** | 2024 | Sequence-Level Ratio，让长短句梯度平等 |

### 🔧 第三章：工程实践

- veRL 框架的 GRPO 实现思路
- MoE 训推不一致问题

---

## 🚀 快速阅读

**想读完整版（单文件）：**

```bash
# 直接打开合并好的完整文档
open 大语言模型的强化学习算法.md
```

**想按章节读：**

```
output/
├── chapter_1-理论基础/
│   ├── 1.1-核心数学概念解析/    # 7个核心概念，每个独立md
│   ├── 1.2-性能差异引理PDL/
│   └── 1.3-替代目标函数L/
├── chapter_2-强化学习具体算法/
│   ├── 2.1-TRPO算法/
│   ├── 2.2-PPO算法/             # 含 PPO 完整流水线架构图
│   ├── 2.3-DPO算法/
│   ├── 2.4-GRPO算法/            # 含 PPO vs GRPO 对比图
│   ├── 2.5-SAPO_GSPO/
│   └── 2.6-学术前沿/
└── chapter_3-工程实践/
```

**想自己合并生成电子书：**

```bash
python build_book.py              # 生成完整 md
python build_book.py --toc        # 打印目录
```

---

## 🤝 一起来完善它！

这个知识库还差很多——**欢迎 PR！**

以下方向都缺人填坑：

- [ ] 📐 **PPO 代码实现** —— 用 PyTorch 从零写一个 mini PPO
- [ ] 🧮 **GRPO 代码实现** —— veRL / TRL 中的 GRPO 实现解析
- [ ] 📊 **算法对比实验** —— PPO vs DPO vs GRPO 在不同任务上的表现
- [ ] 🔬 **DeepSeek-R1 解读** —— GRPO + 规则奖励如何炼出推理能力
- [ ] 🏗️ **RLHF 工程全景** —— 数据标注 → RM 训练 → PPO 对齐全链路
- [ ] 📝 **更多算法** —— REINFORCE、A3C、SAC 在 LLM 中的应用

**贡献方式：**
1. Fork 本仓库
2. 在对应章节目录新建 `x.x_你的内容.md`，按现有格式写
3. 更新 `output/README.md` 目录
4. 提 PR，附上你的参考资料链接

---

## 📚 参考资料

1. [【青稞Talk 102期】从 TRPO 到 SAPO：大模型 RL 算法演进](https://www.bilibili.com/video/BV1na6mBME2P/?vd_source=3c2daa94b6eb2d7117c23f3be2f2c93a)
2. [【青稞Talk 107期】JustRL: 用"最笨"的 RL 方法刷新 1.5B 推理模型新基准](https://www.bilibili.com/video/BV155fZBKE64/?spm_id_from=333.337.search-card.all.click&vd_source=3c2daa94b6eb2d7117c23f3be2f2c93a)
3. [强化学习的数学原理 - 西湖大学 赵世钰](https://www.bilibili.com/video/BV1sd4y167NS/?spm_id_from=333.1007.top_right_bar_window_custom_collection.content.click)

---

## 🏷️ 关键词

`RLHF` `PPO` `GRPO` `DPO` `TRPO` `DeepSeek-R1` `LLM对齐` `强化学习` `大模型训练` `Actor-Critic` `GAE` `KL散度` `重要性采样` `优势函数` `策略梯度` `性能差异引理` `替代目标函数` `Reward Hacking` `MDP` `Proximal Policy Optimization` `Group Relative Policy Optimization`

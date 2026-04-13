# 大语言模型的强化学习算法

> 本知识库由原始 PPTX/DOCX 文档转写而成，完整保留了所有数学公式（LaTeX格式）和文字内容。

---

## 目录结构

```
output/
├── chapter_1/                          # 第1章：理论基础
│   ├── 1.1/                            # 1.1 核心数学概念解析
│   │   ├── 1.1.1_大模型中的RL建模.md
│   │   ├── 1.1.2_期望回报函数.md
│   │   ├── 1.1.3_状态贴现访问频率.md
│   │   ├── 1.1.4_优势函数.md
│   │   ├── 1.1.5_采样和更新.md
│   │   ├── 1.1.6_重要性采样.md
│   │   └── 1.1.7_KL散度.md
│   ├── 1.2/                            # 1.2 性能差异引理 PDL
│   │   └── 1.2_性能差异引理PDL.md
│   └── 1.3/                            # 1.3 替代目标函数
│       └── 1.3_替代目标函数L.md
│
├── chapter_2/                          # 第2章：强化学习具体算法
│   ├── 2.1/                            # 2.1 TRPO 算法
│   │   └── 2.1_TRPO算法.md
│   ├── 2.2/                            # 2.2 PPO 算法
│   │   ├── 2.2.1_近端截断Clipping.md
│   │   ├── 2.2.2_Actor_Critic架构.md
│   │   ├── 2.2.3_GAE优势估算.md
│   │   └── 2.2.4_PPO完整流水线.md
│   ├── 2.3/                            # 2.3 DPO 算法
│   │   └── 2.3_DPO算法.md
│   ├── 2.4/                            # 2.4 GRPO 算法
│   │   └── 2.4_GRPO算法.md
│   ├── 2.5/                            # 2.5 SAPO / GSPO
│   │   └── 2.5_SAPO_GSPO.md
│   └── 2.6/                            # 2.6 学术前沿
│       └── 2.6_学术前沿.md
│
└── chapter_3/                          # 第3章：工程实践
    └── 3_工程实践.md
```

---

## 快速导航

### 第1章：理论基础

| 小节 | 核心内容 | 关键公式 |
|------|----------|----------|
| [1.1.1 大模型中的RL建模](chapter_1/1.1/1.1.1_大模型中的RL建模.md) | MDP建模：状态/动作/策略/奖励 | $\pi(a\|s)$ |
| [1.1.2 期望回报函数](chapter_1/1.1/1.1.2_期望回报函数.md) | 轨迹式 vs 分布式 | $J(\pi) = \mathbb{E}_{\tau\sim\pi}[\sum \gamma^t r_t]$ |
| [1.1.3 状态贴现访问频率](chapter_1/1.1/1.1.3_状态贴现访问频率.md) | 足迹热力图、分布偏移 | $d_\pi(s) = (1-\gamma)\sum_{t=0}^\infty \gamma^t P(s_t=s\|\pi)$ |
| [1.1.4 优势函数](chapter_1/1.1/1.1.4_优势函数.md) | V/Q/A函数、TD Error | $A(s,a) = Q(s,a) - V(s)$ |
| [1.1.5 采样和更新](chapter_1/1.1/1.1.5_采样和更新.md) | On-policy采样、梯度上升 | $J(\pi) = \sum_s d_\pi(s)\sum_a \pi(a\|s)R(s,a)$ |
| [1.1.6 重要性采样](chapter_1/1.1/1.1.6_重要性采样.md) | 数据复用、方差爆炸 | $r_t(\theta) = \frac{\pi_\theta(a\|s)}{\pi_{old}(a\|s)}$ |
| [1.1.7 KL散度](chapter_1/1.1/1.1.7_KL散度.md) | 防止"忘本"惩罚项 | $\text{奖励} = R(s,a) - \beta D_{KL}(\pi_\theta\|\|\pi_{ref})$ |
| [1.2 性能差异引理PDL](chapter_1/1.2/1.2_性能差异引理PDL.md) | 局部→全局、The Catch-22 | $J(\pi_{new}) - J(\pi_{old}) = \mathbb{E}_{d_{\pi_{new}}}[A^{\pi_{old}}]$ |
| [1.3 替代目标函数L](chapter_1/1.3/1.3_替代目标函数L.md) | 狸猫换太子、一阶导数等价 | $L^{surr}(\pi) = \mathbb{E}\left[\frac{\pi(a\|s)}{\pi_{old}(a\|s)}A^{\pi_{old}}\right]$ |

### 第2章：强化学习具体算法

| 算法 | 核心思想 | 关键公式 |
|------|----------|----------|
| [2.1 TRPO](chapter_2/2.1/2.1_TRPO算法.md) | 硬约束KL散度，二阶优化 | $\max L$ s.t. $\bar{D}_{KL} \leq \delta$ |
| [2.2.1 PPO Clipping](chapter_2/2.2/2.2.1_近端截断Clipping.md) | 启发式软截断，一阶优化 | $L^{CLIP} = \mathbb{E}[\min(r_t A_t, \text{clip}(r_t, 1\pm\epsilon)A_t)]$ |
| [2.2.2 Actor-Critic架构](chapter_2/2.2/2.2.2_Actor_Critic架构.md) | 四模型架构：Actor/Critic/RM/Ref | $A_t = Q_t - V(s_t)$ |
| [2.2.3 GAE优势估算](chapter_2/2.2/2.2.3_GAE优势估算.md) | 偏差方差折中 | $\hat{A}_t = \sum_{l=0}^\infty (\gamma\lambda)^l \delta_{t+l}$ |
| [2.2.4 PPO完整流水线](chapter_2/2.2/2.2.4_PPO完整流水线.md) | Rollout→Evaluation→Update | $R_t = r_{score} - \beta\log\frac{\pi_\theta}{\pi_{ref}}$ |
| [2.3 DPO](chapter_2/2.3/2.3_DPO算法.md) | 绕过RL，直接偏好优化 | $\mathcal{L}_{DPO} = -\log\sigma(\beta\log\frac{\pi_\theta(y_w)}{\pi_{ref}(y_w)} - \ldots)$ |
| [2.4 GRPO](chapter_2/2.4/2.4_GRPO算法.md) | 取消Critic，组内竞争 | $A_i = r_i - \text{mean}(r_1,\ldots,r_G)$ |
| [2.5 SAPO/GSPO](chapter_2/2.5/2.5_SAPO_GSPO.md) | 序列级Ratio，解决单位不匹配 | $\rho(\mathbf{y}\|\mathbf{x}) = \frac{\pi_\theta(\mathbf{y}\|\mathbf{x})}{\pi_{old}(\mathbf{y}\|\mathbf{x})}$ |
| [2.6 学术前沿](chapter_2/2.6/2.6_学术前沿.md) | PRM过程奖励、自我博弈 | — |

### 第3章：工程实践

| 内容 | 说明 |
|------|------|
| [3. 工程实践](chapter_3/3_工程实践.md) | veRL/GRPO实现、MoE训推不一致 |

---

## 算法演进关系

```
理论基础（第1章）
    ↓ PDL + 替代目标函数L
TRPO (2015) → 硬约束KL，二阶优化，算力瓶颈
    ↓ 启发式近似
PPO (2017)  → 软截断Clip，一阶优化，工业标准
    ↓ 去掉Critic
GRPO (2024) → 组内竞争，极致省显存，DeepSeek-R1
    ↓ 序列级对齐
SAPO/GSPO   → Sequence-Level Ratio，解决单位不匹配
    ↓ 跳过RL
DPO (2023)  → 直接偏好优化，无需奖励模型
```

---

## 参考资料

1. 【青稞Talk 102期】从 TRPO 到 SAPO：大模型 RL 算法演进
2. 【青稞Talk 107期】JustRL: 用"最笨"的 RL 方法刷新 1.5B 推理模型新基准

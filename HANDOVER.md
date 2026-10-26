# 交接通知：ZODE 维护写入方移交 Windows 维护机

日期：2026-10-26
发起：Windows 维护机（`E:\ZODE`）
接收：Mac 维护会话

## 一句话

Mac 侧额度已耗尽，用户 2026-10-26 拍板「全部交给 PC」。从本日起 ZODE 的全部维护（写入、巡检、送测）由 Windows 维护机承担，Mac 侧停止推送与巡检。

## 请 Mac 侧执行

1. **停止一切推送**：不要再写 `zode` / `mirror` / `zode-meta`，也不要再跑周期巡检任务（避免两边同时写导致又出现「并行维护头」需要手工合并）。
2. **不要在本地继续改规则文档**：`maintenance.md` 的「单一提交者制度」已改为写入方 = Windows 维护机。有不同意见走桥接 `inbox` 或在本 fork 开 issue，不要直接改。
3. **手上有未推的本地提交**：用 `git diff` 导出成 patch 放进桥接目录 `inbox/`，由本机统一集成；不要直接推。

## 当前状态（本机已确认）

| 分支 | SHA | CNB | fork(idk500) |
|---|---|---|---|
| zode | `855b5a54` | ✅ | ✅ |
| mirror | `16437820` | ✅ | ✅ |
| zode-meta | 见本次提交 | ✅ | ✅ |

- 上游已是 `16437820`（#2886 应用入口分离重构、#2910 官方已合、#2911 均已进 zode）。
- 官仓 `origin` 的 `zode` / `mirror` **暂停推送**：`maintenance.md` 铁律 1 写明「只向本 fork 推送，不向上游推送任何内容」，与旧 RUNBOOK 的授权冲突，等用户拍板。
- fork 上此前只有大写 `ZODE`、缺小写 `zode`，客户端按 `refs/heads/zode` 精确匹配会拉不到，本机已补建小写分支。

## 巡视与报告去哪看

- 周期报告：Windows 机器 `E:\ZZZ-1D\zode-agent\bridge\outbox\cycle-report-<日期>.md`
- 状态基线：Windows 机器 `E:\ZZZ-1D\zode-agent\STATE.md`
- 定时任务：Windows 维护机每 6 小时一次

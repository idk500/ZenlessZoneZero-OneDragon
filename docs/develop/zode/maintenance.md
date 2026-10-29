# ZODE 维护规则

ZODE（**Z**enless **O**ne **D**ragon **E**nhanced）是本 fork 的增强发行分支：集成社区精选 PR 与维护者增强功能，通过游戏内既有的代码更新机制分发给选择本通道的用户。

本文是 ZODE 的运行规则，维护会话（人工或 AI）必须遵守。对规则有异议，在本 fork 开 issue 讨论；规则的修改本身走本 fork 的 PR。

## 分支通道

| 分支 | 内容 | 同步方式 |
|---|---|---|
| `main` | 官方主分支（含 fork 自动化提交） | 合并官方 main |
| `mirror` | 官方最新镜像，零本地改动 | fast-forward 指向官方 main |
| `zode` | 增强：官方 main + 维护者增强 + 精选 PR 镜像 | 见下方「维护周期」 |

三个分支都通过设置页的「idk500 增强源」使用；`mirror` 与 `zode` 仅该源可用。

发行副本放在两个地方：CNB（`cnb.cool/zzz1d/ZODE`）与 GitHub fork（`idk500/ZenlessZoneZero-OneDragon`）。维护机先推 CNB 再推 fork；GitHub 侧另有每小时一次的兜底同步，把 fork 的三个分支快进到 CNB 的最新提交（只快进，不 force），避免维护机推 GitHub 失败时用户长时间拉不到新代码。

## 铁律

1. **只向本 fork 推送。** 不向上游仓库推送任何内容，不开 PR、不开 issue；唯一例外见铁律 6 与「不静默修复」：在上游 PR 下提交评审评论。上游仓库只接收**用户本人手动指定的功能**，由用户自己发起 PR——维护会话不代建、不自动建，推上去也合不进官方仓。
2. **merge-based，禁止改写历史。** 只做普通 merge 与普通 push，禁止 rebase、禁止 force push——用户的增量更新与更新去重都依赖「历史只增不改」。
3. **PR 以原始提交合入。** fetch 上游 `refs/pull/N/head` 后直接 merge，保留原作者姓名、邮箱与提交日期；禁止 squash、禁止 cherry-pick 改写身份。
4. **合并消息必须署名原作者**：`<PR原type>: 合入 PR #N <标题>（@<作者>）`。type 沿用 PR 自己的 conventional 前缀。
5. **合入数量不设上限**：队列按序合入，冲突项记入 parked 并试队列下一个，连续 3 个冲突即停车（安全阀）；每个 PR 合入前照常过校验，校验不过不合入。
6. **不静默修复待合 PR。** 校验发现待合 PR 有问题时，不自行修复后合入；按下方「不静默修复」政策交原作者确认，长期无应答才转本 fork 众审。

## 维护周期

1. fetch 官方 main，merge 进 zode（`--no-ff`，消息 `feat: 同步官方 main 至 <短id>`）；mirror 同步为官方 main 指针。随后检查 `feat/background-update-check` 是否有未进入 zode 的新提交，有则 `--no-ff` merge（消息 `feat: 合入增强分支新提交`）。
2. 从清单队列按序合入 PR（数量不设上限，见铁律 5）：fetch `refs/pull/N/head` 并把拿到的 SHA 记入清单（作者后续 force-push 不影响已 pin 的内容）；`git merge-tree --write-tree` 预检冲突，干净则合入；冲突记入 parked 并试队列下一个，连续 3 个冲突即停车。
3. 校验：本次触碰的 `.py` 过 py_compile / ruff，`.yml` 过 YAML 解析；失败则回退该 merge，按「不静默修复」政策处理，本期不合入该 PR、试队列下一个。
4. 推送 zode；更新清单并备份到 `zode-meta` 分支。
5. 快照仓库 traffic 数据（clones / views 原始值）留存于 `zode-meta` 的 `telemetry.yml`（GitHub 仅保留 14 天滚动窗口）。口径：fetch 更新不计数，该数据反映新装与页面访问趋势，不等于活跃用户数。

**评审前置**：任何 PR 入队、定性冲突或立仲裁案之前，必须读取该 PR 的**描述与全部评论**（`gh pr view N --comments`）——作者常在评论区写明与其他改动的关联、独立性与冲突处置建议，跳过这一步会把「相邻行可两全」误判成「结构性重叠」（2026-10-22 issues/2 教训：作者首条评论早已写明与 #2735 独立，仲裁立案时未读，导致误立案后又返工）。

## 冲突分类

- **Class 1（自动推进）**：只有唯一合理答案的冲突——上游改名/搬移/删除后的功能重新挂载、import/语法修补、上游已有等价实现则弃我方、**生成文件（如 `assets/game_data/screen_info/_od_merged.yml`）与分包源的双向冲突：接受上游分包改动后用重生成脚本（`tools/regen_screen_merged.py`）重建合并文件**。自动解决，记入清单 resolved 区。（生成文件口径为 2026-10-29 用户裁定：合并后重生成是唯一合理解，不再因此停车。）
- **Class 2（仲裁）**：多解冲突——两个 PR 用不同实现修同一问题、或与上游演进互斥且各有合理性。流程：
  1. 在**本 fork** 开 issue，标题「[仲裁] <主题>（PR #A vs #B/上游）」；
  2. 正文给出双方方案 diff 要点、影响面、中立分析与推荐及理由；
  3. @相关 PR 作者；候选方案各发一条评论，👍 计票；
  4. **持续等待直到有人应答**（投票或实质性讨论），不设自动截止：窗口期后无票不关帖、不执行 fallback，每个维护周期顺带复查；有人应答后，有票按票决、讨论有结论按结论办；应答后仍无明确方向才 fallback：先跟上游方向，其次采纳分析推荐；
  5. 结论在帖内说明后关闭，写入清单 arbited 区。

  帖子排版遵循下方「对外内容规范」，正文开头给「状态速览 + 投票入口锚点」；写明投票操作步骤（点方案评论的 👍）。

## 对外内容规范

在本 fork 的所有 issue / discussion / 评论 / 文档中：

- 引用官方仓的 PR / Issue 一律用**短显文本链接** `[官方#N](官方仓完整URL)`——显示短、点击直达。禁止全名裸链（`OneDragon-Anything/ZenlessZoneZero-OneDragon#N` 会淹没正文），也禁止裸 `#N`（在本 fork 语境会错误指向本 fork 自己）；
- 仲裁与长周期事项的 issue **正文随进展直接编辑维护**（GitHub 保留编辑历史），让任何访客一眼看到当前状态；评论只做时间线记录，不承担「当前状态」职责。

## 不静默修复

校验发现待合 PR 存在需要修改的问题（lint / import 排序 / 小缺陷等）时，维护会话不自行修复后合入，改为：

1. 在**上游 PR** 下提交评审评论，写明问题与期望的更改（可附建议 diff）——这是对铁律 1「不碰上游」的唯一豁免：只评论，不推送、不开新 PR / issue；
2. 等作者确认并更新 PR 后，fetch 新的 head（更新清单 pin SHA）再合入；
3. 作者连续 2 个维护周期无应答 → 在本 fork 开 issue 发起众审：贴出问题、建议更改与等待记录，社区确认后由维护者本地应用等价修改合入，并在清单记录「经众审绕过原作者」。

历史上已合入的静默修复不追溯处理。

## 上游合并了已镜像的 PR 怎么办

无需处理。PR 的原始提交已在 zode 历史中；上游 squash 合并后，两边净变更一致，git merge 自动判干净——不冲突、不重复。只有上游用**别的改动**碰了同一代码段才是真实分歧，按上面的冲突分类处理。

## fork 分支卫生

fork 上的分支分三类：发行通道（`main` / `mirror` / `zode`）、维护（`zode-meta`）、开发与历史（其余）。保护名单：上述通道分支与 `feat/background-update-check`（维护者活跃开发线），永不清理。

对保护名单外的开发分支：

- 内容已被 zode 吸收（祖先关系或补丁等价，`git cherry` 判定）→ 删除分支；
- 有独特内容且可无冲突合入 → 保留分支，记入清单 `candidates` 区作为改进候选；
- 有独特内容且冲突复杂 → 先打 `archive/idk500/<分支名>` 标签存证再删分支；**合并价值不明确的高复杂度任务，在本 fork 开 issue 邀请社区协助审查，不闭门硬解**；
- 无独有提交的自动化/测试残留 → 直接删除。

被归档的分支随时可找回：`git fetch idk500 tag archive/idk500/<分支名>`。

## 贡献者须知

- 你的 PR 被合入 zode 时保留原始提交与完整作者信息，合并消息与首页「公告要闻」第一条都会标注你的 ID。
- 你的 PR 在合入前若被发现小问题，我们会把建议更改评论在你的 PR 下等你确认后合入，不会替你改完悄悄合入；长期收不到回复才会转本 fork 众审。
- 不希望自己的 PR 被本分支镜像？在本 fork 开 issue 说明，我们以 revert 对应合并提交的方式移除，不改写历史。
- 对某个仲裁结论有异议，直接在仲裁 issue 里参与讨论；新事实出现可重开。

## 清单与备份

`zode-manifest/manifest.yml`（仓库外维护，备份于 `zode-meta` 分支）记录：

- `baseline`：增强分支基线（来源与合入时间）
- `merged`：已镜像 PR（number / pin SHA / 标题 / 作者 / 日期）
- `queue`：候选队列
- `parked`：冲突挂起
- `excluded`：排除项及理由
- `resolved`：Class 1 自动解决记录
- `arbited`：Class 2 仲裁结论

## 单一提交者制度（2026-10-25 定，同日 23:10 修订）

ZODE / mirror / zode-meta / 各发行分支**只允许一处写入**：Windows 维护机（`E:\Z1D`，每日定时 + 用户触发的交互会话；2026-10-29 目录大迁移前为 `E:\ZODE`）。2026-10-25 晚写入方从 Mac 会话移交本机，Mac 及其余机器一律不直接推送这些分支。

移交理由：唯一测试环境在 Windows（GUI 与真实自动化只能在这里跑），写入方与测试环境分离会让「合入前必须实机验证」这条无法执行。

**改动一律落在 `zode` 分支，不在实机运行目录直接打补丁。** 实机运行目录（开发克隆）只负责跑和验证；发现问题回到 `zode` 分支改、推送、再由实例侧更新机制拉取。直接在运行目录改的问题有两个：只修好这一台机器，用户永远拿不到；下次切分支或更新就被覆盖，改动变成隐性丢失。

**其他机器的改动提交通道（二选一）**：
1. **桥接目录**（推荐）：改动说明 + git diff/patch 文件放入桥接 `inbox/`（`change-<主题>.md`），维护周期统一集成；本机桥接根目录为 `E:\ZZZ-1D\zode-agent\bridge\`（`inbox/` 收件、`outbox/` 放周期报告）。
2. **提案分支**：如需 git 原生流程，推到 `incoming/<主题>` 分支（仅此命名空间对外开放），维护周期 fetch 后审阅、择优合入，随后删除提案分支。

**任何机器提交前的强制自检**（防身份泄漏，源头规则）：
```shell
git config user.name   # 必须输出 Roy
git config user.email  # 必须输出 mr.fc@qq.com
```
不匹配则先 `git config --global user.name Roy && git config --global user.email mr.fc@qq.com` 再操作；维护会话提交前额外对本轮 diff 做 `grep -i <受保护关键词>` 兜底（关键词见维护记忆，不入任何仓库）。

## 分层执行制度（SOP 分级，2026-10-25 定）

维护工作按判断强度分三级，目的是让低成本模型承担日常，昂贵推理只花在例外上：

### L1 机械执行（廉价模型可独立完成，禁止自由发挥）

按本清单逐条执行，**只做清单内动作，遇到任何清单外情况即升级 L3 并停止**：

```text
1. 在 E:\Z1D\zode 工作副本内执行（2026-10-29 目录迁移后不再另建 worktree）
2. 删除 refs/remotes/idk500/*、refs/remotes/cnb/* 全部 tracking 引用，重新显式 refspec fetch，
   fetch 后核对引用值（rev-parse 输出）才可继续
3. 上游 main：优先 fetch origin；失败改拉 https://cnb.cool/OneDragon-Anything/ZenlessZoneZero-OneDragon.git
4. 上游有新提交：git merge --no-ff <上游tip> -m "feat: 同步官方 main 至 <短id>"
   - 无冲突 → 继续 5
   - 有冲突且属 Class 1（含生成文件 _od_merged.yml，解法=接受分包改动后重生成）→ 解后记 resolved 继续 5
   - 其余冲突 → 停止，升级 L3（不得自行解冲突）
5. 校验：触碰的 .py 逐个 py_compile（通过即可，存量 lint 不阻塞）
6. 推送：先 fetch 对应远端确认无并行推送，再推 CNB 与 GitHub（**分支名一律小写 `zode`**、
   `mirror`——客户端按 `refs/heads/zode` 精确大小写拉取，大小写不同等于该分支不存在）
7. zode-meta：在最新远端版本上追加 last_cycle（当天日期+一句状态）与 traffic 快照，双推
8. 桥接：读 `E:\Z1D\zode-agent\bridge\inbox\` 新文件；周期报告写 `E:\Z1D\zode-agent\bridge\outbox\cycle-report-<日期>.md`
9. 常规观察（各一行结论）：仲裁 issues/2 票况 / traffic 数 / 主仓 #2892、#2895、#2904 状态 / fork 分支清单
```

L1 的全部输出 = 周期报告。报告模板固定，不写分析性长文。

### L2 例行判断（需一定经验，可由强模型或人复核后执行）

- inbox 测试结果的逐项归因（bug 定位、复现建议、分级）
- PR 补榜评审（评审前置读评论 → 预检 → 一行结论）
- Class 1 冲突解法（上游等价实现采纳、import 修补——解完必须 git diff 自查并在报告列出改动点）
- 插件 registry 动态、跨仓联动判断

### L3 升级停止线（出现即停，写明现状等维护者/主会话）

- 任何 merge 冲突、任何推送被拒（含 non-fast-forward）
- tracking 引用与 ls-remote 不一致（幻影）
- 隐私关键词 grep 命中
- 桥接 inbox 出现无法归类的请求
- 任何「顺手优化」的诱惑

**纪律**：L1 中断后不做任何补救尝试（等待 L3），宁可空转一个周期。报告第一行标注本次执行级别（L1/L2/L3-升级）。

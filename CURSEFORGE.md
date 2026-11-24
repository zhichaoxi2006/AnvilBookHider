# CurseForge 文案 / Listing copy

## 1. Summary（项目简介字段）

**English（推荐，49 字符）**

```
Hide any enchantment from JEI's anvil recipes.
```

**中文（16 字）**

```
在 JEI 的铁砧配方中隐藏任意附魔。
```

---

## 2. Description — English

**Anvil Book Hider** keeps JEI's Anvil category readable.

JEI doesn't use Minecraft's anvil recipes. It generates its own for every enchanted book and every item that book can be applied to. For most enchantments that's already a long list — and for enchantments that work on *any* item it's thousands of entries. Ars Nouveau's **Reactive** is the usual offender: one book, every item in the game, so the Anvil tab becomes a wall of nearly identical recipes.

*I wrote this mod because I got tired of Ars Nouveau's Reactive enchantment flooding my JEI pages.*

This mod lets you list the enchantments you never want to see there. Any anvil recipe whose book (right input) or result carries one of the listed enchantments is hidden from JEI. Nothing else changes — the anvil still works exactly as before.

### Features

- Hide any enchantment from JEI's Anvil category — vanilla or modded, by registry ID.
- Simple config list, no commands needed; set it to `[]` to show everything again.
- Display-only: gameplay, recipes and the anvil itself are untouched.
- Unknown IDs (for example from a mod you don't have) are skipped with a log warning instead of breaking anything.
- No-op if JEI isn't installed.
- Lightweight: filtering runs once, when JEI builds its recipes.

### Configuration

File: `config/anvilbookhider-common.toml`

```toml
# Default: Ars Nouveau's "Reactive"
hiddenEnchantments = ["ars_nouveau:reactive"]

# Hide several at once
hiddenEnchantments = ["ars_nouveau:reactive", "minecraft:mending"]
```

- Entries are enchantment IDs in `namespace:path` form.
- Ars Nouveau is **not** required; the default entry is simply ignored when that mod isn't present.
- Changes apply the next time JEI builds its recipes, so rejoin the world or reconnect to the server.

### Requirements

- Minecraft 1.21.1
- NeoForge 21.1 or newer
- JEI 19 or newer (without JEI the mod does nothing)

Client-side mod: put it in the client's `mods` folder. Servers don't need it.

### Limitations

- Only affects what JEI displays. The real anvil, REI and EMI are unchanged.
- Filters by enchantment ID only; to hide the whole Anvil category, use JEI's own config.
- JEI is required for the mod to have any effect.

### License

MIT — see [`LICENSE`](LICENSE).

---

## 3. Description — 中文

**Anvil Book Hider（铁砧附魔书隐藏）** 让 JEI 的铁砧分类重新变得清爽。

JEI 并不读取原版铁砧配方，而是自己为“每种附魔书 × 每个可附魔物品”生成铁砧配方。对多数附魔来说这已经是一长串，而对能附到任意物品上的附魔（典型例子是新生魔艺的“反应”），几乎所有物品都会生成一条，铁砧页于是被大量几乎相同的配方占满。

*这个模组就是因为我受够了新生魔艺的“反应”附魔污染 JEI 页面而开发的。*

本模组让你列出不想看到的附魔：凡是右侧输入（附魔书）或产物带有这些附魔的铁砧配方，都会从 JEI 中隐藏。其他内容不受影响，铁砧本身的功能也完全不变。

### 功能

- 按注册名隐藏任意附魔（原版或模组），仅作用于 JEI 的铁砧分类。
- 只需修改配置，无需命令；列表改成 `[]` 即恢复全部显示。
- 只影响显示，不影响玩法、配方和铁砧本身。
- 配置里写了未安装模组的附魔时，只在日志中提示并跳过，不会报错。
- 未安装 JEI 时完全空操作。
- 轻量：仅在 JEI 构建配方时过滤一次。

### 配置

文件：`config/anvilbookhider-common.toml`

```toml
# 默认：新生魔艺的“反应”
hiddenEnchantments = ["ars_nouveau:reactive"]

# 同时隐藏多个
hiddenEnchantments = ["ars_nouveau:reactive", "minecraft:mending"]
```

- 每项都是附魔的注册名（`命名空间:路径`）。
- 不需要安装新生魔艺；未安装时默认项会被直接忽略。
- 修改后需重新进入世界或重连服务器：JEI 会在重建配方时重新读取配置。

### 环境需求

- Minecraft 1.21.1
- NeoForge 21.1 或更高
- JEI 19 或更高（没有 JEI 时本模组不产生任何效果）

客户端模组：放进客户端的 `mods` 文件夹即可，服务器无需安装。

### 已知限制

- 只改变 JEI 的显示，实际铁砧、REI、EMI 均不受影响。
- 只按附魔 ID 过滤；想整体关闭铁砧分类请使用 JEI 自带配置。
- 必须安装 JEI 才会生效。

### 许可证

MIT，详见 [`LICENSE`](LICENSE)。

---

## 发布前检查

1. `issueTrackerURL` 已设为 <https://github.com/zhichaoxi2006/AnvilBookHider/issues>；介绍末尾还可在 CurseForge 编辑器里补上 Modrinth 链接。
2. 介绍顶部的横幅建议在 CurseForge 编辑器里直接上传 `art/logo/banner-1280x720.png`，正文粘贴后可用编辑器把 `###` 行设为标题、把 `-` 行设为列表。
3. 中文标题可考虑用“铁砧附魔书隐藏”，搜索时更直观。

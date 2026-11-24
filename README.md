# Anvil Book Hider

NeoForge 1.21.1 模组：**通过配置文件隐藏 JEI 中指定附魔在铁砧的显示。**

JEI 没有原版铁砧配方，它会为“可附魔物品 × 附魔 × 等级”自动生成大量
“附魔书 + 物品 → 附魔物品”的铁砧配方。本模组在 JEI 载入配方后，把配置里列出的
附魔对应的铁砧配方从 JEI 中隐藏，其他玩法逻辑完全不受影响。

## 环境

| 项目 | 版本 |
| --- | --- |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.248 |
| ModDevGradle | 2.0.148 |
| Gradle Wrapper | 8.14 |
| JDK | 21 |
| JEI（编译期 API + 本地运行） | 19.27.0.340 |

* 模组 ID：`anvilbookhider`
* Java 包名：`com.zhichaoxi.anvilbookhider`
* 构建产物：`build/libs/anvilbookhider-1.0.0.jar`

## 目录结构

```
build.gradle                       构建脚本（ModDevGradle + JEI 依赖 + NeoForged 镜像）
gradle.properties                  版本号与模组元数据
settings.gradle
gradlew / gradlew.bat               Gradle Wrapper
src/main/java/com/zhichaoxi/anvilbookhider/
    AnvilBookHider.java            @Mod 入口，注册配置文件
    Config.java                    配置文件定义（hiddenEnchantments）
    compat/jei/AnvilBookHiderJeiPlugin.java
                                   @JeiPlugin，读取配置并在运行时隐藏铁砧配方
src/main/resources/
    META-INF/neoforge.mods.toml    模组元数据
    pack.mcmeta
```

## 常用命令

```powershell
.\gradlew.bat build          # 编译并打包到 build/libs/
.\gradlew.bat runClient      # 启动开发客户端（已带 JEI）
.\gradlew.bat runServer      # 启动开发服务端
.\gradlew.bat runData        # 数据生成
```

调试时可以用 `-PquickPlayWorld=<存档文件夹名>` 让客户端直接进入 `run/saves/` 里的存档：

```powershell
.\gradlew.bat runClient "-PquickPlayWorld=TestWorld"
```

Linux / macOS 使用 `./gradlew`。

## 配置文件

首次启动后会在 `run/config/`（正式游戏为 `.minecraft/config/`）生成
`anvilbookhider-common.toml`：

```toml
hiddenEnchantments = ["minecraft:mending", "minecraft:frost_walker"]
```

* 每项都是附魔的注册名（`命名空间:路径`），支持模组附魔，例如 `apotheosis:某附魔`。
* 默认是空列表，即什么都不隐藏。
* 修改后需要**重新进入世界 / 重连服务器**才会生效：JEI 会在重建配方时重新读取配置。

## 实现原理

1. JEI 的 `AnvilRecipeMaker` 为每个附魔生成铁砧配方：左槽为可附魔物品，右槽为
   该附魔的附魔书（`stored_enchantments` 组件），产物为附魔后的物品。
2. `AnvilBookHiderJeiPlugin` 实现 `IModPlugin#onRuntimeAvailable`，在 JEI 配方就绪后：
   * 用 `IRecipeManager#createRecipeLookup(RecipeTypes.ANVIL).includeHidden()` 取出所有铁砧配方；
   * 检查配方右槽（附魔书）和产物上的附魔 ID，与配置取交集；
   * 调用 `IRecipeManager#hideRecipes(RecipeTypes.ANVIL, ...)` 隐藏命中的配方。
3. `@JeiPlugin` 类只有在 JEI 存在时才会被 JEI 扫描加载，因此没装 JEI 时本模组是纯空操作，
   不会因为缺少类而崩溃。

成功隐藏时日志会输出：

```
[AnvilBookHider] Hid 42 anvil recipe(s) for enchantment(s) [minecraft:mending].
```

### 已验证的行为

开发客户端（NeoForge 21.1.248 + JEI 19.27.0.340）中，把配置设为
`hiddenEnchantments = ["minecraft:mending"]` 并进入世界后，日志输出：

```
[AnvilBookHider] Hid 67 anvil recipe(s) for enchantment(s) [minecraft:mending].
```

即 67 条“修补附魔书 + 物品”的铁砧配方已从 JEI 中移除，其余附魔的铁砧配方保留。

## 构建环境说明（网络）

`build.gradle` 会自动把 ModDevGradle 添加的 `https://maven.neoforged.net/` 仓库替换为官方
CDN 镜像 `https://neoforged.forgecdn.net/`（两者目录结构完全一致），因为
`maven.neoforged.net` 使用 cdn77，在部分网络（如中国大陆）不可达。
如需访问原始仓库，加上 `-PuseNeoForgedMirror=false`。

JEI 依赖来自 `https://modmaven.dev`（`dvs1.progwml6.com` 作为备用）。

## 已知限制

* 只隐藏 **JEI 的显示**，不影响铁砧实际功能，也不影响 REI / EMI。
* 配置在 JEI 重建配方时读取，改完配置需重新进入世界。
* 只按附魔 ID 过滤；如果想完全关闭 JEI 的铁砧分类，请用 JEI 自带配置。

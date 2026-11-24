package com.zhichaoxi.anvilbookhider;

import com.mojang.logging.LogUtils;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import org.slf4j.Logger;

/**
 * Entry point of Anvil Book Hider.
 *
 * <p>The mod itself does not touch the game: it only exposes a config file that
 * the optional JEI plugin ({@code com.zhichaoxi.anvilbookhider.compat.jei}) reads
 * to hide anvil recipes from JEI.</p>
 */
@Mod(AnvilBookHider.MODID)
public final class AnvilBookHider {
    public static final String MODID = "anvilbookhider";
    public static final Logger LOGGER = LogUtils.getLogger();

    public AnvilBookHider(ModContainer modContainer) {
        modContainer.registerConfig(ModConfig.Type.COMMON, Config.SPEC);
    }
}

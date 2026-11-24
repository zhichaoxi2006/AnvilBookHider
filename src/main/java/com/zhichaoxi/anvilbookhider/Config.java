package com.zhichaoxi.anvilbookhider;

import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.common.ModConfigSpec;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * Config definition.
 *
 * <p>The generated file is {@code config/anvilbookhider-common.toml}. Values are
 * read every time JEI reloads its recipes, so an edit takes effect on the next
 * world join.</p>
 */
public final class Config {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.ConfigValue<List<? extends String>> HIDDEN_ENCHANTMENTS;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();

        HIDDEN_ENCHANTMENTS = builder
                .comment(
                        "Enchantment IDs that must not be shown in JEI's Anvil category.",
                        "Every anvil recipe whose book (or result) carries one of these",
                        "enchantments is hidden from JEI.",
                        "Example: hiddenEnchantments = [\"minecraft:mending\", \"minecraft:frost_walker\"]",
                        "Changes are applied the next time JEI builds its recipes (i.e. when you join a world)."
                )
                .defineListAllowEmpty(
                        "hiddenEnchantments",
                        List.of(),
                        () -> "minecraft:mending",
                        Config::isEnchantmentId
                );

        SPEC = builder.build();
    }

    private Config() {
    }

    private static boolean isEnchantmentId(Object value) {
        return value instanceof String string && ResourceLocation.tryParse(string.trim()) != null;
    }

    /**
     * @return the configured enchantment IDs, parsed and de-duplicated.
     *         Empty when the config is not loaded yet or nothing is configured.
     */
    public static Set<ResourceLocation> hiddenEnchantments() {
        Set<ResourceLocation> ids = new LinkedHashSet<>();
        if (!SPEC.isLoaded()) {
            return ids;
        }
        for (String raw : HIDDEN_ENCHANTMENTS.get()) {
            if (raw == null) {
                continue;
            }
            ResourceLocation id = ResourceLocation.tryParse(raw.trim());
            if (id != null) {
                ids.add(id);
            }
        }
        return ids;
    }
}

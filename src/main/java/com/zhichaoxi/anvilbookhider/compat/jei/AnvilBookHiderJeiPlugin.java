package com.zhichaoxi.anvilbookhider.compat.jei;

import com.zhichaoxi.anvilbookhider.AnvilBookHider;
import com.zhichaoxi.anvilbookhider.Config;
import mezz.jei.api.IModPlugin;
import mezz.jei.api.JeiPlugin;
import mezz.jei.api.constants.RecipeTypes;
import mezz.jei.api.recipe.IRecipeManager;
import mezz.jei.api.recipe.vanilla.IJeiAnvilRecipe;
import mezz.jei.api.runtime.IJeiRuntime;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.ItemEnchantments;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;

/**
 * JEI plugin that removes the anvil recipes of the configured enchantments.
 *
 * <p>JEI generates an anvil recipe for every "enchanted book + item" pair
 * ({@code mezz.jei.library.plugins.vanilla.anvil.AnvilRecipeMaker}). Each recipe
 * puts the books of exactly one enchantment in the right input slot, so an
 * enchantment can be filtered out by inspecting the enchantments carried by the
 * right inputs (and, for custom recipes, by the result).</p>
 *
 * <p>This class is only loaded by JEI. It must never be referenced from the
 * {@code @Mod} class, otherwise the mod would crash when JEI is not installed.</p>
 */
@JeiPlugin
public final class AnvilBookHiderJeiPlugin implements IModPlugin {
    private static final ResourceLocation PLUGIN_UID =
            ResourceLocation.fromNamespaceAndPath(AnvilBookHider.MODID, "jei_plugin");

    private final Set<IJeiAnvilRecipe> hiddenByUs = new LinkedHashSet<>();

    @Override
    public ResourceLocation getPluginUid() {
        return PLUGIN_UID;
    }

    @Override
    public void onRuntimeAvailable(IJeiRuntime jeiRuntime) {
        IRecipeManager recipeManager = jeiRuntime.getRecipeManager();

        // If the runtime is reused (e.g. recipes were reloaded), start from a clean
        // slate so a changed config can also un-hide something again.
        if (!hiddenByUs.isEmpty()) {
            recipeManager.unhideRecipes(RecipeTypes.ANVIL, new ArrayList<>(hiddenByUs));
            hiddenByUs.clear();
        }

        Set<ResourceLocation> hiddenEnchantments = Config.hiddenEnchantments();
        if (hiddenEnchantments.isEmpty()) {
            AnvilBookHider.LOGGER.info("[AnvilBookHider] No enchantments are configured to be hidden from JEI's anvil display.");
            return;
        }

        List<IJeiAnvilRecipe> toHide = recipeManager.createRecipeLookup(RecipeTypes.ANVIL)
                .includeHidden()
                .get()
                .filter(recipe -> usesHiddenEnchantment(recipe, hiddenEnchantments))
                .toList();

        if (toHide.isEmpty()) {
            AnvilBookHider.LOGGER.info(
                    "[AnvilBookHider] No anvil recipes matched the configured enchantments {}.",
                    hiddenEnchantments
            );
            return;
        }

        recipeManager.hideRecipes(RecipeTypes.ANVIL, new ArrayList<>(toHide));
        hiddenByUs.addAll(toHide);

        AnvilBookHider.LOGGER.info(
                "[AnvilBookHider] Hid {} anvil recipe(s) for enchantment(s) {}.",
                toHide.size(),
                hiddenEnchantments
        );
    }

    @Override
    public void onRuntimeUnavailable() {
        hiddenByUs.clear();
    }

    /**
     * @return true when the recipe's books (right inputs) or results carry one of
     *         the enchantments that must stay hidden.
     */
    private static boolean usesHiddenEnchantment(IJeiAnvilRecipe recipe, Set<ResourceLocation> hiddenEnchantments) {
        return containsHiddenEnchantment(recipe.getRightInputs(), hiddenEnchantments)
                || containsHiddenEnchantment(recipe.getOutputs(), hiddenEnchantments);
    }

    private static boolean containsHiddenEnchantment(List<ItemStack> stacks, Set<ResourceLocation> hiddenEnchantments) {
        for (ItemStack stack : stacks) {
            if (stack.isEmpty()) {
                continue;
            }
            for (Holder<Enchantment> enchantment : enchantmentsOf(stack)) {
                Optional<ResourceKey<Enchantment>> key = enchantment.unwrapKey();
                if (key.isPresent() && hiddenEnchantments.contains(key.get().location())) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Reads both components used for enchantments: {@code stored_enchantments}
     * (enchanted books, {@code EnchantmentHelper#setEnchantments}) and
     * {@code enchantments} (regular enchanted items).
     */
    private static Set<Holder<Enchantment>> enchantmentsOf(ItemStack stack) {
        ItemEnchantments stored = stack.get(DataComponents.STORED_ENCHANTMENTS);
        if (stored != null && !stored.isEmpty()) {
            return stored.keySet();
        }
        ItemEnchantments applied = stack.get(DataComponents.ENCHANTMENTS);
        if (applied != null && !applied.isEmpty()) {
            return applied.keySet();
        }
        return Set.of();
    }
}

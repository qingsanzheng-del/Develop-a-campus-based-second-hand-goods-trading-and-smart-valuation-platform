<script setup>
import logoUrl from '../assets/logo_blue.png'

defineProps({
  size: { type: String, default: 'md' }, // sm | md | lg
  compact: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex items-center select-none" :class="compact ? 'gap-1.5' : 'gap-3'">
    <img
      :src="logoUrl"
      alt="广应科跳蚤市场"
      class="shrink-0"
      :class="size === 'lg' ? 'h-12' : size === 'sm' ? 'h-6' : 'h-6'"
    />
    <span
      class="brand-cn leading-none whitespace-nowrap"
      :class="size === 'lg' ? 'text-3xl' : size === 'sm' ? 'text-sm' : 'text-base'"
    >广应科跳蚤市场</span>
  </div>
</template>

<style scoped>
/* 喷漆字：粗黑 + 淡蓝喷绘溢色 + 明黄重影 */
.brand-cn {
  font-family: var(--font-display);
  font-weight: 900;
  letter-spacing: 0.05em;
  color: var(--color-brand-800);
  text-shadow:
    1.5px 1.5px 0 var(--color-accent),
    3px 3px 0 rgba(100, 149, 182, 0.4);
}
</style>

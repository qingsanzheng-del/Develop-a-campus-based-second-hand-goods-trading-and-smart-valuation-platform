<script setup>
defineProps({
  size: { type: String, default: 'md' }, // md | lg
  compact: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex items-center gap-3 select-none" :class="compact ? 'gap-2' : ''">
    <!-- 标记：淡蓝价格签 + 明黄泼墨 + 墨黑 ¥（粗粝手绘） -->
    <svg
      viewBox="0 0 140 140"
      class="rough shrink-0"
      :class="size === 'lg' ? 'w-20 h-20' : size === 'sm' ? 'w-9 h-9' : 'w-11 h-11'"
      aria-hidden="true"
    >
      <!-- 明黄泼墨（背后） -->
      <g fill="#ffd400">
        <circle cx="118" cy="104" r="21" />
        <circle cx="131" cy="82" r="9" />
        <circle cx="99" cy="128" r="7" />
        <path d="M122 60 q7 -7 15 -3 q-3 9 -11 6 z" />
      </g>
      <!-- 价格签主体（斜切角 + 手绘） -->
      <path
        d="M26 20 L94 20 L120 46 L120 112 Q120 122 110 122 L32 122 Q26 122 26 114 Z"
        fill="#6495b6"
        stroke="#17181a"
        stroke-width="5"
        stroke-linejoin="round"
      />
      <!-- 挂孔 -->
      <circle cx="50" cy="40" r="7.5" fill="#f4f1ea" stroke="#17181a" stroke-width="4.5" />
      <!-- ¥ 符号（粗黑手绘笔画） -->
      <g stroke="#17181a" stroke-width="7" stroke-linecap="round" fill="none">
        <path d="M54 62 L72 86 L90 62" />
        <line x1="72" y1="86" x2="72" y2="116" />
        <line x1="58" y1="77" x2="86" y2="77" />
        <line x1="60" y1="102" x2="84" y2="102" />
      </g>
      <!-- 淡蓝上的泼墨点缀 -->
      <g fill="#ffd400">
        <circle cx="98" cy="56" r="4.5" />
        <circle cx="107" cy="48" r="3" />
      </g>
      <!-- 蹭痕（干笔飞白） -->
      <g stroke="#f4f1ea" stroke-width="3" stroke-linecap="round" opacity="0.7">
        <line x1="40" y1="100" x2="52" y2="98" />
        <line x1="44" y1="108" x2="56" y2="106" />
      </g>
    </svg>

    <!-- 字标：喷漆粗黑字 + 印刷错位 -->
    <div class="leading-none min-w-0">
      <div
        class="brand-cn"
        :class="size === 'lg' ? 'text-4xl' : size === 'sm' ? 'text-base' : 'text-xl'"
      >
        广应科跳蚤市场
      </div>
      <div v-if="!compact" class="brand-sub font-mono text-ink-soft tracking-widest mt-1.5">
        校园二手 · 智能估价
      </div>
      <div v-if="!compact" class="brand-en font-mono text-ink-soft mt-0.5">CAMPUS FLEA MARKET</div>
    </div>
  </div>
</template>

<style scoped>
/* 喷漆字：粗黑 + 淡蓝喷绘溢色 + 明黄重影 */
.brand-cn {
  font-family: var(--font-display);
  font-weight: 900;
  letter-spacing: 0.08em;
  color: var(--color-brand-800);
  text-shadow:
    2px 2px 0 var(--color-accent),
    4px 4px 0 rgba(100, 149, 182, 0.4);
}
.brand-sub {
  font-size: 0.68rem;
  letter-spacing: 0.3em;
}
.brand-en {
  font-size: 0.55rem;
  letter-spacing: 0.42em;
}
</style>

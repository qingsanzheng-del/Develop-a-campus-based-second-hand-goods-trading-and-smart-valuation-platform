<script setup>
// 手绘涂鸦装饰：五角星 / 箭头 / 波浪 / 十字 / 喷点，用于打破留白
defineProps({
  accent: { type: Boolean, default: false },
})
</script>

<template>
  <svg viewBox="0 0 120 120" class="rough" aria-hidden="true">
    <!-- 五角星 -->
    <path
      d="M32 16 l6 14 15 1 -11 10 3 15 -13 -8 -13 8 3 -15 -11 -10 15 -1 z"
      fill="none"
      stroke="#17181a"
      stroke-width="3"
      stroke-linejoin="round"
    />
    <!-- 喷溅箭头 -->
    <path d="M84 20 q16 4 3 24" fill="none" stroke="#ff4d2e" stroke-width="4" stroke-linecap="round" />
    <path d="M98 16 l9 5 -10 5 z" fill="#ff4d2e" />
    <!-- 波浪线 -->
    <path
      d="M12 96 q10 -12 20 0 t20 0 t20 0 t20 0"
      fill="none"
      stroke="#6495b6"
      stroke-width="3"
      stroke-linecap="round"
    />
    <!-- 十字 -->
    <path d="M106 68 v20 M96 78 h20" stroke="#17181a" stroke-width="3" stroke-linecap="round" />
    <!-- 明黄喷点 -->
    <circle cx="16" cy="62" r="3.4" :fill="accent ? '#ffd400' : '#ffd400'" />
    <circle cx="8" cy="74" r="2.2" fill="#17181a" />
    <circle cx="27" cy="80" r="2.6" fill="#ffd400" />
    <circle cx="56" cy="8" r="2.4" fill="#17181a" />
  </svg>
</template>

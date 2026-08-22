<script setup>
const items = [
  '毕业季大甩卖',
  '支持 AI 智能估价',
  '拍照 3 张自动定价',
  '校内面交更放心',
  '让闲置找到新主人',
  '宿舍好物清仓',
  '一键发布 30 秒上架',
]
</script>

<template>
  <div class="overflow-hidden border-b-2 border-ink bg-accent" aria-hidden="true">
    <div class="ticker-track whitespace-nowrap py-1.5 font-display font-bold text-sm text-ink">
      <span v-for="n in 2" :key="n" class="inline-flex">
        <template v-for="(t, i) in items" :key="i">
          <span class="mx-4">{{ t }}</span>
          <span class="text-flare-deep">★</span>
        </template>
      </span>
    </div>
  </div>
</template>

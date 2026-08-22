<script setup>
import logoUrl from '../assets/logo_blue.png'

defineProps({
  size: { type: String, default: 'md' }, // sm | md | lg
  compact: { type: Boolean, default: false },
})
</script>

<template>
  <div class="flex items-center select-none">
    <img
      :src="logoUrl"
      alt="广应科跳蚤市场"
      class="shrink-0 h-auto"
      :class="size === 'lg' ? 'h-14' : size === 'sm' ? 'h-8' : 'h-9'"
    />
  </div>
</template>

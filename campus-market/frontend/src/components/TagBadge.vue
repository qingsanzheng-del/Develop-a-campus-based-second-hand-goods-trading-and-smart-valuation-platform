<script setup>
defineProps({
  text: { type: String, required: true },
})
</script>

<template>
  <span class="chip chip-brand">{{ text }}</span>
</template>

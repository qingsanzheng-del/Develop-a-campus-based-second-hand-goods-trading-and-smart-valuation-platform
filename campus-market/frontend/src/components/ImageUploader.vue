<script setup>
import { ref } from 'vue'
import { toast } from '../utils/toast'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  max: { type: Number, default: 3 },
})

const emit = defineEmits(['update:modelValue'])
const inputRef = ref(null)

function trigger() {
  inputRef.value?.click()
}

function onFile(e) {
  const files = Array.from(e.target.files || [])
  const remaining = props.max - props.modelValue.length
  if (remaining <= 0) {
    toast(`最多上传 ${props.max} 张图片`, 'error')
    return
  }
  const selected = files.slice(0, remaining)
  for (const f of selected) {
    if (!f.type.startsWith('image/')) {
      toast('仅支持图片文件', 'error')
      continue
    }
    const url = URL.createObjectURL(f)
    emit('update:modelValue', [...props.modelValue, { file: f, preview: url }])
  }
  e.target.value = ''
}

function remove(i) {
  const next = [...props.modelValue]
  URL.revokeObjectURL(next[i].preview)
  next.splice(i, 1)
  emit('update:modelValue', next)
}
</script>

<template>
  <div class="grid grid-cols-3 gap-3">
    <div v-for="(img, i) in modelValue" :key="i" class="relative polaroid" :style="{ '--tilt': `${(i % 3 - 1) * 1.2}deg` }">
      <img :src="img.preview" class="aspect-square" alt="预览" />
      <button
        type="button"
        class="absolute top-1 right-1 w-7 h-7 border-2 border-ink bg-white font-display font-bold hover:bg-flare hover:text-white active:bg-flare"
        @click="remove(i)"
      >✕</button>
    </div>

    <button
      v-if="modelValue.length < max"
      type="button"
      class="aspect-square border-[3px] border-dashed border-ink flex flex-col items-center justify-center text-ink-soft bg-white/40 hover:bg-accent/40 active:bg-accent"
      @click="trigger"
    >
      <span class="text-3xl font-display font-black leading-none">＋</span>
      <span class="text-xs font-mono mt-1">上传图片</span>
      <span class="text-[10px] font-mono text-ink-soft">{{ modelValue.length }}/{{ max }}</span>
    </button>

    <input ref="inputRef" type="file" accept="image/*" multiple class="hidden" @change="onFile" />
  </div>
</template>

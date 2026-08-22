<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from './components/NavBar.vue'
import SideDecor from './components/SideDecor.vue'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()
const toasts = ref([])

function addToast(e) {
  const { message, type = 'info' } = e.detail
  const id = Date.now() + Math.random()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }, 3200)
}

onMounted(() => {
  window.addEventListener('app:toast', addToast)
  window.addEventListener('app:unauthorized', () => {
    auth.logout()
    router.push('/login')
  })
})
</script>

<template>
  <!-- 全局手绘毛边滤镜（feTurbulence 位移，制造粗糙笔触/晕染） -->
  <svg width="0" height="0" style="position: absolute" aria-hidden="true">
    <defs>
      <filter id="rough">
        <feTurbulence type="fractalNoise" baseFrequency="0.055" numOctaves="2" seed="3" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="3" />
      </filter>
      <filter id="rough-more">
        <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="7" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="6" />
      </filter>
    </defs>
  </svg>

  <div class="min-h-full flex flex-col">
    <SideDecor />
    <NavBar />
    <main class="flex-1">
      <router-view />
    </main>

    <footer class="relative border-t-2 border-ink py-4 mt-6 overflow-hidden">
      <div class="absolute right-4 -top-1 w-16 h-16 bg-accent rotate-12 border-2 border-ink opacity-80"></div>
      <div class="max-w-6xl mx-auto px-4 space-y-2">
        <div class="flex flex-wrap items-center gap-2 text-xs">
          <span class="font-display font-bold text-base">跳蚤集市</span>
          <span class="font-mono tracking-widest text-ink-soft">校园二手 &amp; 智能估价</span>
          <span class="ml-auto flex gap-2">
            <span class="chip">关于我们</span>
            <span class="chip chip-accent">交易规则</span>
            <span class="chip chip-flare">举报反馈</span>
          </span>
        </div>
        <div class="font-mono text-xs text-ink-soft flex flex-wrap gap-x-4 gap-y-1">
          <span>♻ 让每一件闲置找到新主人</span>
          <span>📞 客服微信 campus-market</span>
          <span>🕐 每天 24h 可发帖</span>
          <span>📍 支持校内面交</span>
        </div>
      </div>
    </footer>

    <!-- 提示：粗黑描边 + 硬偏移，无圆角无光晕 -->
    <div class="fixed top-4 right-4 z-50 space-y-2 w-72">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="border-2 border-ink px-3 py-2 text-sm font-mono shadow-[3px_3px_0_var(--color-ink)]"
        :class="
          t.type === 'error'
            ? 'bg-flare text-white'
            : t.type === 'success'
              ? 'bg-accent text-ink'
              : 'bg-paper-deep text-ink'
        "
      >
        {{ t.type === 'error' ? '✕ ' : t.type === 'success' ? '✓ ' : '! ' }}{{ t.message }}
      </div>
    </div>
  </div>
</template>

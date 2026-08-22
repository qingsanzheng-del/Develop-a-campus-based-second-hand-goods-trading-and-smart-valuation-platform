<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import TagBadge from '../components/TagBadge.vue'
import Graffiti from '../components/Graffiti.vue'
import { useAuthStore } from '../stores/auth'
import { toast } from '../utils/toast'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const listing = ref(null)
const loading = ref(true)
const activeImg = ref(0)

const isOwner = computed(() => listing.value && listing.value.seller_id === auth.user?.id)

async function load() {
  loading.value = true
  try {
    const { data } = await api.get(`/listings/${route.params.id}`)
    listing.value = data
  } finally {
    loading.value = false
  }
}

async function copyContact() {
  try {
    await navigator.clipboard.writeText(listing.value.contact)
    toast('联系方式已复制', 'success')
  } catch {
    toast('复制失败，请手动复制', 'error')
  }
}

async function setStatus(status) {
  try {
    const { data } = await api.patch(`/listings/${listing.value.id}/status`, { status })
    listing.value = data
    toast(status === 'sold' ? '已标记为售出' : '已下架', 'success')
  } catch (e) {
    // 拦截器已提示
  }
}

onMounted(load)
</script>

<template>
  <div class="relative max-w-4xl mx-auto px-4 py-4">
    <Graffiti class="w-20 h-20 absolute -top-1 right-2 pointer-events-none opacity-80" />
    <div v-if="loading" class="space-y-4 animate-pulse">
      <div class="aspect-square sm:aspect-video bg-paper-deep border-2 border-ink/20"></div>
      <div class="h-7 bg-paper-deep border-2 border-ink/10 w-1/3"></div>
      <div class="h-24 bg-paper-deep border-2 border-ink/10"></div>
    </div>

    <template v-else-if="listing">
      <div class="grid sm:grid-cols-2 gap-6">
        <!-- 图片区：拍立得 -->
        <div>
          <div class="polaroid rough-more" style="--tilt: -0.8deg">
            <img
              v-if="listing.images && listing.images.length"
              :src="listing.images[activeImg]"
              :alt="listing.title"
              class="aspect-square"
            />
            <div v-else class="aspect-square bg-paper-deep flex items-center justify-center text-6xl">🛍️</div>
          </div>
          <div v-if="listing.images && listing.images.length > 1" class="flex gap-2 mt-3">
            <button
              v-for="(img, i) in listing.images"
              :key="i"
              class="w-16 h-16 border-2 overflow-hidden bg-white"
              :class="i === activeImg ? 'border-flare' : 'border-ink'"
              @click="activeImg = i"
            >
              <img :src="img" class="w-full h-full object-cover" alt="" />
            </button>
          </div>
        </div>

        <!-- 信息区 -->
        <div>
          <div class="flex items-start gap-2 flex-wrap">
            <h1 class="brutal-title text-2xl sm:text-3xl">{{ listing.title }}</h1>
            <span v-if="listing.status === 'sold'" class="stamp text-flare-deep">已售</span>
            <span v-else-if="listing.status === 'delisted'" class="stamp text-ink-soft">已下架</span>
          </div>

          <div class="mt-3 font-display font-black text-4xl text-brand-700">
            <span class="text-2xl text-flare-deep">¥</span>{{ listing.price_min }}<span
              v-if="listing.price_max && listing.price_max !== listing.price_min"
              class="text-xl text-ink-soft"
            > – {{ listing.price_max }}</span>
          </div>

          <div class="mt-3 flex flex-wrap gap-2">
            <TagBadge :text="listing.category" />
            <TagBadge :text="`成色：${listing.ai_condition}`" />
            <TagBadge v-for="(t, i) in listing.ai_tags" :key="i" :text="t" />
          </div>

          <div class="mt-4 border-2 border-ink bg-white p-3 font-mono text-sm leading-loose whitespace-pre-wrap clip-cut-bl">
            {{ listing.ai_copy || listing.description || '暂无描述' }}
          </div>

          <div class="mt-4 flex items-center justify-between font-mono text-xs text-ink-soft">
            <span class="flex items-center gap-2">
              🧑‍🎓 {{ listing.seller_name }}
              <span class="sticker bg-accent text-[10px]" style="--rot: -4deg">✦ 校内认证</span>
            </span>
            <span>{{ new Date(listing.created_at).toLocaleString() }}</span>
          </div>

          <!-- 联系方式 -->
          <div class="mt-4 border-[3px] border-ink bg-brand-100 p-3 flex items-center justify-between gap-3">
            <div class="min-w-0">
              <div class="font-mono text-[10px] tracking-widest text-brand-700">联系方式</div>
              <div class="font-display font-bold text-ink mt-0.5 break-all">{{ listing.contact || '未填写' }}</div>
            </div>
            <button class="btn-brutal btn-accent px-4 py-2 text-sm shrink-0" @click="copyContact">📋 一键复制</button>
          </div>

          <!-- 卖家操作 -->
          <div v-if="isOwner && listing.status === 'active'" class="mt-4 flex gap-3">
            <button class="btn-brutal btn-flare flex-1 py-2 text-sm" @click="setStatus('sold')">标记已售</button>
            <button class="btn-ghost flex-1 py-2 text-sm" @click="setStatus('delisted')">下架</button>
          </div>
        </div>
      </div>
    </template>

    <div v-else class="text-center py-16 text-ink-soft">
      <p class="brutal-title text-2xl">商品不存在或已删除</p>
      <router-link to="/" class="btn-ghost px-4 py-2 mt-4 inline-flex">返回首页</router-link>
    </div>
  </div>
</template>

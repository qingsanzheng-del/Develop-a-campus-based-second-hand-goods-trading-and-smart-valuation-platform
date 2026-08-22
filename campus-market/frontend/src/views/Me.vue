<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import { toast } from '../utils/toast'

const auth = useAuthStore()
const items = ref([])
const loading = ref(true)

const STATUS_TEXT = { active: '在售', sold: '已售', delisted: '已下架', pending: '待审核' }
const STATUS_CLASS = {
  active: 'chip-accent',
  sold: 'text-ink-soft bg-paper-deep',
  delisted: 'text-ink-soft bg-paper-deep',
  pending: 'chip-flare',
}

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/listings/mine')
    items.value = data
  } finally {
    loading.value = false
  }
}

async function setStatus(item, status) {
  try {
    await api.patch(`/listings/${item.id}/status`, { status })
    toast(status === 'sold' ? '已标记售出' : '已下架', 'success')
    load()
  } catch (e) {
    // 拦截器已提示
  }
}

onMounted(load)
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-4">
    <h1 class="brutal-title text-3xl">个人中心</h1>
    <p class="subnote text-sm mt-1">👋 {{ auth.user?.username }}，管理你发布的商品</p>

    <div v-if="loading" class="text-center py-16 text-ink-soft font-mono">加载中…</div>
    <div v-else-if="items.length === 0" class="text-center py-14 text-ink-soft">
      <div class="text-6xl mb-3">📦</div>
      <p class="brutal-title text-xl">你还没有发布任何商品</p>
      <router-link to="/publish" class="btn-brutal mt-4 px-5 py-2 inline-flex">去发布</router-link>
    </div>

    <div v-else class="mt-4 space-y-3">
      <div
        v-for="item in items"
        :key="item.id"
        class="bg-white border-2 border-ink p-3 flex items-center gap-4"
        :class="item.id % 2 === 0 ? 'clip-cut' : ''"
      >
        <img
          v-if="item.images && item.images.length"
          :src="item.images[0]"
          class="w-20 h-20 object-cover bg-paper-deep border-2 border-ink"
          alt=""
        />
        <div v-else class="w-20 h-20 bg-paper-deep border-2 border-ink flex items-center justify-center text-2xl">🛍️</div>

        <div class="flex-1 min-w-0">
          <div class="font-display font-bold text-ink truncate">{{ item.title }}</div>
          <div class="font-display font-bold text-brand-700 mt-0.5">¥{{ item.price_min }}</div>
          <span class="chip mt-1.5" :class="STATUS_CLASS[item.status]">
            {{ STATUS_TEXT[item.status] || item.status }}
          </span>
        </div>

        <div class="flex flex-col gap-2 shrink-0">
          <router-link :to="`/listing/${item.id}`" class="btn-ghost px-3 py-1.5 text-sm text-center">查看</router-link>
          <button
            v-if="item.status === 'active'"
            class="btn-brutal btn-flare px-3 py-1.5 text-sm"
            @click="setStatus(item, 'sold')"
          >标记已售</button>
          <button
            v-if="item.status === 'active'"
            class="btn-ghost px-3 py-1.5 text-sm"
            @click="setStatus(item, 'delisted')"
          >下架</button>
        </div>
      </div>
    </div>
  </div>
</template>

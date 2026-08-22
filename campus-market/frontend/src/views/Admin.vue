<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { toast } from '../utils/toast'

const TABS = [
  { key: '', label: '全部' },
  { key: 'pending', label: '待审核' },
  { key: 'active', label: '在售' },
  { key: 'sold', label: '已售' },
  { key: 'delisted', label: '已下架' },
]

const STATUS_TEXT = { active: '在售', sold: '已售', delisted: '已下架', pending: '待审核' }
const STATUS_CLASS = {
  active: 'chip-accent',
  sold: 'text-ink-soft bg-paper-deep',
  delisted: 'text-ink-soft bg-paper-deep',
  pending: 'chip-flare',
}

const tab = ref('')
const items = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/listings', { params: { status: tab.value } })
    items.value = data
  } finally {
    loading.value = false
  }
}

function switchTab(t) {
  tab.value = t
  load()
}

async function approve(item) {
  await api.post(`/admin/listings/${item.id}/approve`)
  toast('已通过审核', 'success')
  load()
}

async function delist(item) {
  await api.post(`/admin/listings/${item.id}/delist`)
  toast('已下架', 'success')
  load()
}

async function remove(item) {
  if (!confirm(`确定删除「${item.title}」？此操作不可恢复。`)) return
  await api.delete(`/admin/listings/${item.id}`)
  toast('已删除', 'success')
  load()
}

onMounted(load)
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-4">
    <h1 class="brutal-title text-3xl">管理后台</h1>
    <p class="subnote text-sm mt-1">审核、下架与删除商品</p>

    <div class="flex flex-wrap gap-2 mt-4 mb-4">
      <button
        v-for="t in TABS"
        :key="t.key"
        class="px-3 py-1.5 font-display font-bold text-sm border-2 border-ink"
        :class="tab === t.key ? 'bg-ink text-white' : 'bg-white text-ink hover:bg-brand-100 active:bg-accent'"
        @click="switchTab(t.key)"
      >
        {{ t.label }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-16 text-ink-soft font-mono">加载中…</div>
    <div v-else-if="items.length === 0" class="text-center py-16 text-ink-soft">
      <div class="text-6xl mb-3">🗂️</div>
      <p class="brutal-title text-xl">暂无相关商品</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="item in items"
        :key="item.id"
        class="bg-white border-2 border-ink p-3 flex items-center gap-4"
        :class="item.id % 2 === 0 ? 'clip-cut-bl' : ''"
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
          <div class="font-mono text-xs text-ink-soft mt-0.5">
            {{ item.category }} · ¥{{ item.price_min }} · {{ item.seller_name }}
          </div>
          <div class="mt-1.5 flex flex-wrap gap-2">
            <span class="chip" :class="STATUS_CLASS[item.status]">
              {{ STATUS_TEXT[item.status] || item.status }}
            </span>
            <span v-if="item.is_flagged" class="chip chip-flare">⚠ 违规待审</span>
          </div>
        </div>

        <div class="flex flex-col gap-2 shrink-0">
          <button
            v-if="item.status === 'pending'"
            class="btn-brutal btn-flare px-3 py-1.5 text-sm"
            @click="approve(item)"
          >通过</button>
          <button
            v-if="item.status !== 'delisted'"
            class="btn-ghost px-3 py-1.5 text-sm"
            @click="delist(item)"
          >下架</button>
          <button class="btn-ghost px-3 py-1.5 text-sm !border-flare-deep !text-flare-deep" @click="remove(item)">
            删除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

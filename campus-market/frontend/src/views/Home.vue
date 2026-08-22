<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import ListingCard from '../components/ListingCard.vue'
import SkeletonCard from '../components/SkeletonCard.vue'
import BrandLogo from '../components/BrandLogo.vue'
import TickerBar from '../components/TickerBar.vue'
import Graffiti from '../components/Graffiti.vue'

const CATEGORIES = ['全部', '数码', '书籍', '生活用品', '服饰鞋包', '运动户外', '其他']
const HOT_TAGS = ['iPhone', '考研书', '台灯', '宿舍神器', '相机', '吉他', '小电驴']

const listings = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 12
const category = ref('')
const keyword = ref('')
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    const { data } = await api.get('/listings', {
      params: { category: category.value, q: keyword.value, page: page.value, page_size: pageSize },
    })
    listings.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function selectCategory(c) {
  category.value = c === '全部' ? '' : c
  page.value = 1
  load()
}

function search() {
  page.value = 1
  load()
}

function hotSearch(t) {
  keyword.value = t
  search()
}

const totalPages = () => Math.max(1, Math.ceil(total.value / pageSize))

onMounted(load)
</script>

<template>
  <div>
    <!-- 走马灯：胶带滚动条 -->
    <TickerBar />

    <div class="max-w-6xl mx-auto px-4 py-5">
      <!-- 英雄区：海报拼贴 -->
      <section class="relative mb-5 border-[3px] border-ink bg-brand-50 clip-cut p-5 sm:p-7 overflow-hidden">
        <Graffiti class="w-24 h-24 absolute -right-2 -top-3" />
        <Graffiti class="w-16 h-16 absolute left-3 bottom-2 opacity-70" />
        <div class="absolute right-6 top-6 w-20 h-20 bg-accent rotate-12 border-2 border-ink opacity-90"></div>
        <div class="absolute right-24 bottom-5 w-14 h-14 bg-flare -rotate-6 border-2 border-ink opacity-80"></div>

        <BrandLogo size="lg" class="mb-3" />

        <h1 class="brutal-title text-4xl sm:text-5xl max-w-2xl">
          让每一件闲置<br />找到新主人
        </h1>
        <p class="subnote mt-3 text-sm">
          上传照片 · AI 智能估价 · 一键发布<br />不精致的集市，最真实的青春
        </p>

        <div class="mt-4 flex flex-wrap items-center gap-2">
          <router-link to="/publish" class="btn-brutal px-5 py-2.5 text-base">＋ 发布闲置</router-link>
          <span class="sticker bg-accent" style="--rot: -4deg">毕业甩卖</span>
          <span class="sticker bg-flare text-white" style="--rot: 3deg">9 成新</span>
          <span class="sticker bg-white" style="--rot: -2deg">可小刀 🔪</span>
        </div>
      </section>

      <!-- 数据印章条 -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
        <div class="stat">
          <div class="stat-num">AI</div>
          <div class="font-mono text-xs text-ink-soft mt-0.5">拍照即估价</div>
        </div>
        <div class="stat" style="transform: rotate(0.5deg)">
          <div class="stat-num">3 张</div>
          <div class="font-mono text-xs text-ink-soft mt-0.5">照片就够</div>
        </div>
        <div class="stat" style="transform: rotate(-0.6deg)">
          <div class="stat-num">30s</div>
          <div class="font-mono text-xs text-ink-soft mt-0.5">一键上架</div>
        </div>
        <div class="stat" style="transform: rotate(0.4deg)">
          <div class="stat-num">♻</div>
          <div class="font-mono text-xs text-ink-soft mt-0.5">循环不浪费</div>
        </div>
      </div>

      <!-- 筛选 + 搜索 -->
      <div class="flex flex-col sm:flex-row sm:items-end gap-3 mb-3">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="c in CATEGORIES"
            :key="c"
            class="px-3 py-1.5 font-display font-bold text-sm border-2 border-ink"
            :class="
              category === c || (c === '全部' && category === '')
                ? 'bg-accent text-ink'
                : 'bg-white text-ink hover:bg-brand-100 active:bg-ink active:text-white'
            "
            @click="selectCategory(c)"
          >
            {{ c }}
          </button>
        </div>
        <div class="sm:ml-auto flex gap-2">
          <input
            v-model="keyword"
            type="text"
            class="input-brutal !w-auto text-sm"
            placeholder="搜点啥…"
            @keyup.enter="search"
          />
          <button class="btn-brutal px-4 py-1.5 text-sm" @click="search">搜索</button>
        </div>
      </div>

      <!-- 热门标签 -->
      <div class="flex flex-wrap items-center gap-2 mb-4 text-xs">
        <span class="font-display font-bold text-ink">🔥 热门：</span>
        <button
          v-for="t in HOT_TAGS"
          :key="t"
          class="px-2 py-0.5 border-2 border-ink bg-paper-deep hover:bg-accent active:bg-ink active:text-white"
          @click="hotSearch(t)"
        >{{ t }}</button>
      </div>

      <!-- 商品网格 -->
      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        <SkeletonCard v-for="i in 8" :key="i" />
      </div>
      <div v-else-if="listings.length === 0" class="relative text-center py-16 text-ink-soft">
        <Graffiti class="w-20 h-20 mx-auto mb-3" />
        <p class="brutal-title text-xl">没找到相关好物</p>
        <p class="font-mono text-sm mt-2">换个关键词，或者发布你手边的闲置</p>
      </div>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-x-3 gap-y-6">
        <ListingCard v-for="l in listings" :key="l.id" :listing="l" />
      </div>

      <!-- 分页 -->
      <div v-if="totalPages() > 1" class="flex items-center justify-center gap-3 mt-7">
        <button
          :disabled="page <= 1"
          class="btn-ghost px-4 py-1.5 text-sm"
          @click="page--; load()"
        >← 上一页</button>
        <span class="font-mono text-sm">{{ page }} / {{ totalPages() }}</span>
        <button
          :disabled="page >= totalPages()"
          class="btn-ghost px-4 py-1.5 text-sm"
          @click="page++; load()"
        >下一页 →</button>
      </div>
    </div>
  </div>
</template>

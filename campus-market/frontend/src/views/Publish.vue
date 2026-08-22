<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import ImageUploader from '../components/ImageUploader.vue'
import Graffiti from '../components/Graffiti.vue'
import { toast } from '../utils/toast'

const router = useRouter()

const CATEGORIES = ['数码', '书籍', '生活用品', '服饰鞋包', '运动户外', '其他']

const images = ref([])
const description = ref('')
const analyzing = ref(false)
const publishing = ref(false)
const analyzed = ref(false)

const form = ref({
  title: '',
  category: '数码',
  condition: '',
  price_min: 0,
  price_max: 0,
  tags: [],
  valuation_note: '',
  copy: '',
  contact: '',
})

const tagInput = ref('')

async function analyze() {
  if (images.value.length === 0) {
    toast('请先上传 1-3 张图片', 'error')
    return
  }
  analyzing.value = true
  try {
    const fd = new FormData()
    images.value.forEach((img) => fd.append('files', img.file))
    fd.append('description', description.value)
    const { data } = await api.post('/ai/analyze', fd)
    images.value.forEach((img, i) => (img.server = data.images[i]))
    form.value = {
      title: data.title,
      category: data.category,
      condition: data.condition,
      price_min: data.price_min,
      price_max: data.price_max,
      tags: data.tags || [],
      valuation_note: data.valuation_note || '',
      copy: data.copy,
      contact: form.value.contact,
    }
    analyzed.value = true
    toast('AI 估价完成，请确认信息', 'success')
  } catch (e) {
    // 错误已在拦截器提示
  } finally {
    analyzing.value = false
  }
}

function addTag() {
  const t = tagInput.value.trim()
  if (t && !form.value.tags.includes(t)) {
    form.value.tags.push(t)
  }
  tagInput.value = ''
}

function removeTag(i) {
  form.value.tags.splice(i, 1)
}

async function publish() {
  if (!form.value.title.trim()) {
    toast('请填写标题', 'error')
    return
  }
  if (!form.value.contact.trim()) {
    toast('请填写联系方式', 'error')
    return
  }
  publishing.value = true
  try {
    const { data } = await api.post('/listings', {
      title: form.value.title,
      category: form.value.category,
      description: description.value,
      images: images.value.map((img) => img.server),
      ai_condition: form.value.condition,
      ai_tags: form.value.tags,
      ai_copy: form.value.copy,
      price_min: Number(form.value.price_min),
      price_max: Number(form.value.price_max),
      contact: form.value.contact,
    })
    toast(data.status === 'pending' ? '已提交，等待管理员审核' : '发布成功', 'success')
    router.push('/')
  } catch (e) {
    // 错误已在拦截器提示
  } finally {
    publishing.value = false
  }
}
</script>

<template>
  <div class="relative max-w-3xl mx-auto px-4 py-4">
    <Graffiti class="w-20 h-20 absolute -top-1 right-3 pointer-events-none opacity-80" />
    <h1 class="brutal-title text-3xl">发布商品</h1>
    <p class="subnote text-sm mt-1">上传 1-3 张照片，AI 自动识别并智能估价</p>
    <div class="mt-3 flex items-start gap-2 border-2 border-ink bg-accent/40 p-2.5 text-xs font-mono">
      <span class="text-base leading-none">💡</span>
      <span>小贴士：在光线充足处平放拍摄 3 张（正面 / 细节 / 瑕疵），估价更准、更好卖。</span>
    </div>

    <div class="mt-4 bg-white border-[3px] border-ink clip-cut p-5 space-y-5">
      <!-- 1 上传 -->
      <section>
        <h2 class="brutal-title text-lg mb-3">① 上传照片</h2>
        <ImageUploader v-model="images" :max="3" />
      </section>

      <!-- 2 补充说明 -->
      <section>
        <h2 class="brutal-title text-lg mb-3">② 补充说明（可选）</h2>
        <textarea
          v-model="description"
          rows="3"
          class="input-brutal"
          placeholder="例如：iPhone 14 用了两年，屏幕有轻微划痕…"
        ></textarea>
      </section>

      <!-- AI 分析按钮 -->
      <section class="text-center">
        <button
          :disabled="analyzing || images.length === 0"
          class="btn-brutal px-8 py-3 text-lg"
          @click="analyze"
        >
          <span v-if="analyzing" class="inline-flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
            AI 识别估价中…
          </span>
          <span v-else>✨ AI 智能估价</span>
        </button>
      </section>

      <!-- 分析中 -->
      <div v-if="analyzing" class="space-y-3">
        <p class="font-mono text-sm text-brand-700 text-center">AI 正在识别图片并智能估价，约需 10–20 秒，请稍候…</p>
        <div class="space-y-3 animate-pulse">
          <div class="h-5 bg-paper-deep border-2 border-ink/10 w-1/3"></div>
          <div class="h-4 bg-paper-deep border-2 border-ink/10 w-2/3"></div>
          <div class="h-4 bg-paper-deep border-2 border-ink/10 w-1/2"></div>
          <div class="h-20 bg-paper-deep border-2 border-ink/10"></div>
        </div>
      </div>

      <!-- 3 确认信息 -->
      <section v-if="analyzed && !analyzing" class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="brutal-title text-lg">③ 确认并完善信息</h2>
          <button
            :disabled="analyzing"
            class="btn-ghost px-3 py-1.5 text-sm"
            @click="analyze"
          >🔄 重新估价</button>
        </div>

        <div v-if="form.valuation_note" class="border-2 border-ink bg-accent/30 p-3 font-mono text-sm">
          <span class="font-display font-bold text-ink">💡 估价依据：</span>{{ form.valuation_note }}
        </div>

        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">标题</label>
          <input v-model="form.title" type="text" class="input-brutal" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-sm mb-1 text-ink-soft">分类</label>
            <select v-model="form.category" class="input-brutal">
              <option v-for="c in CATEGORIES" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
          <div>
            <label class="block font-mono text-sm mb-1 text-ink-soft">成色</label>
            <input v-model="form.condition" type="text" class="input-brutal" />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block font-mono text-sm mb-1 text-ink-soft">最低价（元）</label>
            <input v-model.number="form.price_min" type="number" min="0" class="input-brutal" />
          </div>
          <div>
            <label class="block font-mono text-sm mb-1 text-ink-soft">最高价（元）</label>
            <input v-model.number="form.price_max" type="number" min="0" class="input-brutal" />
          </div>
        </div>

        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">标签</label>
          <div class="flex flex-wrap gap-2 mb-2">
            <span
              v-for="(t, i) in form.tags"
              :key="i"
              class="chip chip-brand inline-flex items-center gap-1"
            >
              {{ t }}
              <button class="font-bold hover:text-flare-deep" @click="removeTag(i)">✕</button>
            </span>
          </div>
          <div class="flex gap-2">
            <input
              v-model="tagInput"
              type="text"
              class="input-brutal flex-1"
              placeholder="添加标签后回车"
              @keyup.enter="addTag"
            />
            <button class="btn-ghost px-3 py-2 text-sm" @click="addTag">添加</button>
          </div>
        </div>

        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">文案</label>
          <textarea v-model="form.copy" rows="4" class="input-brutal"></textarea>
        </div>

        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">联系方式（微信 / QQ / 手机号）</label>
          <input v-model="form.contact" type="text" class="input-brutal" placeholder="用于买家联系你" />
        </div>

        <button
          :disabled="publishing"
          class="btn-brutal w-full py-3 text-lg"
          @click="publish"
        >
          {{ publishing ? '发布中…' : '发布' }}
        </button>
      </section>
    </div>
  </div>
</template>

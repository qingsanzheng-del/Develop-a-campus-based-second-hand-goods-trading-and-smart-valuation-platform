<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import { toast } from '../utils/toast'
import BrandLogo from '../components/BrandLogo.vue'
import Graffiti from '../components/Graffiti.vue'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const confirm = ref('')
const loading = ref(false)

async function submit() {
  if (!username.value || !password.value) return
  if (password.value.length < 6) {
    toast('密码至少 6 位', 'error')
    return
  }
  if (password.value !== confirm.value) {
    toast('两次密码不一致', 'error')
    return
  }
  loading.value = true
  try {
    const { data } = await api.post('/auth/register', {
      username: username.value,
      password: password.value,
    })
    auth.setAuth(data.token, data.user)
    toast('注册成功', 'success')
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-sm mx-auto mt-8 px-4">
    <div class="text-center mb-4">
      <BrandLogo size="lg" class="justify-center" />
    </div>

    <div class="relative overflow-hidden brutal clip-cut-bl p-5">
      <Graffiti class="w-20 h-20 absolute -right-2 -top-2 pointer-events-none opacity-70" />
      <h1 class="brutal-title text-3xl">注册</h1>
      <p class="subnote text-xs mt-1">加入跳蚤集市</p>

      <form class="mt-5 space-y-3" @submit.prevent="submit">
        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">用户名</label>
          <input v-model="username" type="text" class="input-brutal" placeholder="2-50 个字符" />
        </div>
        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">密码</label>
          <input v-model="password" type="password" class="input-brutal" placeholder="至少 6 位" />
        </div>
        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">确认密码</label>
          <input v-model="confirm" type="password" class="input-brutal" placeholder="再输一遍" />
        </div>
        <button type="submit" :disabled="loading" class="btn-brutal w-full py-2.5 text-lg">
          {{ loading ? '注册中…' : '注册' }}
        </button>
      </form>

      <p class="mt-4 font-mono text-sm text-center text-ink-soft">
        已有账号？
        <router-link to="/login" class="font-bold underline decoration-flare decoration-2 underline-offset-2">去登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import BrandLogo from '../components/BrandLogo.vue'
import Graffiti from '../components/Graffiti.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)

async function submit() {
  if (!username.value || !password.value) return
  loading.value = true
  try {
    const { data } = await api.post('/auth/login', {
      username: username.value,
      password: password.value,
    })
    auth.setAuth(data.token, data.user)
    router.push(route.query.redirect || '/')
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

    <div class="relative overflow-hidden brutal clip-cut p-5">
      <Graffiti class="w-20 h-20 absolute -right-2 -top-2 pointer-events-none opacity-70" />
      <h1 class="brutal-title text-3xl">登录</h1>
      <p class="subnote text-xs mt-1">欢迎回到跳蚤集市</p>

      <form class="mt-5 space-y-3" @submit.prevent="submit">
        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">用户名</label>
          <input v-model="username" type="text" class="input-brutal" placeholder="你的昵称" />
        </div>
        <div>
          <label class="block font-mono text-sm mb-1 text-ink-soft">密码</label>
          <input v-model="password" type="password" class="input-brutal" placeholder="••••••" />
        </div>
        <button type="submit" :disabled="loading" class="btn-brutal w-full py-2.5 text-lg">
          {{ loading ? '登录中…' : '登录' }}
        </button>
      </form>

      <p class="mt-4 font-mono text-sm text-center text-ink-soft">
        还没有账号？
        <router-link to="/register" class="font-bold underline decoration-flare decoration-2 underline-offset-2">去注册</router-link>
      </p>
    </div>
  </div>
</template>

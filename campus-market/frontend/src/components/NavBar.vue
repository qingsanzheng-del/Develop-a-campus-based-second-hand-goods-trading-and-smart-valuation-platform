<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import BrandLogo from './BrandLogo.vue'

const router = useRouter()
const auth = useAuthStore()

function logout() {
  auth.logout()
  router.push('/')
}

const navLink =
  'px-3 py-1.5 border-2 border-transparent font-display text-sm font-bold hover:border-ink active:bg-ink active:text-white'
</script>

<template>
  <header class="sticky top-0 z-40 bg-paper border-b-[3px] border-ink">
    <div class="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between gap-3">
      <router-link to="/">
        <BrandLogo compact />
      </router-link>

      <nav class="flex items-center gap-1 text-sm">
        <router-link to="/" :class="navLink" active-class="!border-ink bg-accent">首页</router-link>
        <router-link to="/publish" :class="navLink" active-class="!border-ink bg-accent">发布</router-link>

        <template v-if="auth.token">
          <router-link v-if="auth.isAdmin" to="/admin" :class="navLink" active-class="!border-ink bg-accent">
            管理
          </router-link>
          <router-link to="/me" :class="navLink" active-class="!border-ink bg-accent">我的</router-link>
          <button class="btn-ghost ml-2 px-3 py-1.5 text-sm" @click="logout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn-brutal ml-2 px-4 py-1.5 text-sm">登录</router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import Graffiti from './Graffiti.vue'
// 侧边留白装饰：仅在宽屏（xl+）显示，填补 max-w-6xl 内容区两侧的空白
// 竖排旧招牌 + 涂鸦 + 贴纸 + 公告栏，纯装饰、不挡点击（pointer-events-none）
</script>

<template>
  <!-- ============ 左侧装饰 ============ -->
  <aside
    class="hidden xl:block fixed left-4 top-24 bottom-4 w-20 z-10 pointer-events-none select-none"
    aria-hidden="true"
  >
    <!-- 竖排旧招牌 -->
    <div class="writing-vertical brutal-title text-2xl tracking-[0.3em] text-brand-700">
      广应科跳蚤市场
    </div>

    <Graffiti class="w-16 h-16 mt-6 -ml-1" />

    <!-- 贴纸串 -->
    <div class="mt-8 flex flex-col gap-3 items-start">
      <span class="sticker bg-flare text-white" style="--rot: -5deg">全场可刀</span>
      <span class="sticker bg-accent" style="--rot: 4deg">面交优先</span>
      <span class="sticker bg-brand-300" style="--rot: -3deg">支持小刀</span>
    </div>

    <!-- 旧公告栏 -->
    <div class="mt-8 border-2 border-ink bg-paper-deep p-2 rotate-[-2deg] shadow-[3px_3px_0_var(--color-ink)]">
      <div class="font-display font-bold text-[10px] text-flare-deep tracking-widest">★ 公告栏 ★</div>
      <div class="font-mono text-[9px] leading-tight text-ink-soft mt-1 space-y-0.5">
        <div>求：台灯</div>
        <div>出：考研书</div>
        <div>换：吉他</div>
      </div>
    </div>

    <Graffiti class="w-12 h-12 mt-8 opacity-70" />
  </aside>

  <!-- ============ 右侧装饰 ============ -->
  <aside
    class="hidden xl:block fixed right-4 top-24 bottom-4 w-20 z-10 pointer-events-none select-none"
    aria-hidden="true"
  >
    <!-- 竖排口号 -->
    <div class="writing-vertical brutal-title text-xl tracking-[0.3em] text-brand-800 ml-auto">
      让闲置找到新主人
    </div>

    <Graffiti class="w-14 h-14 mt-6 ml-auto" />

    <!-- 印章 -->
    <div class="mt-8 flex flex-col gap-3 items-end">
      <span class="stamp text-flare-deep">已售</span>
      <span class="stamp text-brand-600">9 新</span>
      <span class="stamp text-ink">校内</span>
    </div>

    <!-- 数据小票 -->
    <div class="mt-8 border-2 border-ink bg-white p-2 rotate-[2deg] shadow-[3px_3px_0_var(--color-ink)]">
      <div class="font-mono text-[9px] text-ink-soft space-y-0.5 leading-tight">
        <div>NO. 2026</div>
        <div class="border-t border-dashed border-ink-soft/50 pt-0.5">今日上新</div>
        <div>AI 估价 · 30s</div>
      </div>
    </div>

    <Graffiti class="w-12 h-12 mt-8 ml-auto opacity-70" />
  </aside>
</template>

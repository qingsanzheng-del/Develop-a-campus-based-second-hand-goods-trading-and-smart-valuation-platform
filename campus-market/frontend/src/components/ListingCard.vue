<script setup>
defineProps({
  listing: { type: Object, required: true },
})
</script>

<template>
  <router-link :to="`/listing/${listing.id}`" class="group block" :class="listing.status === 'sold' ? 'opacity-60' : ''">
    <!-- 拍立得：白边贴附 + 轻微倾斜 + 胶带 -->
    <div class="polaroid" :style="{ '--tilt': `${(listing.id % 5 - 2) * 0.9}deg` }">
      <img
        v-if="listing.images && listing.images.length"
        :src="listing.images[0]"
        :alt="listing.title"
        class="aspect-square"
        loading="lazy"
      />
      <div v-else class="aspect-square bg-paper-deep flex items-center justify-center text-4xl">🛍️</div>
      <span
        v-if="listing.status === 'sold'"
        class="stamp absolute top-2 right-2 text-flare-deep bg-white/90"
        style="font-size: 0.8rem"
      >已售</span>
      <span
        v-else-if="listing.status === 'delisted'"
        class="stamp absolute top-2 right-2 text-ink-soft bg-white/90"
        style="font-size: 0.8rem"
      >下架</span>
    </div>

    <!-- 信息区：粗黑标题 + 错落排版 -->
    <div class="px-1 mt-3">
      <h3 class="brutal-title text-base truncate" style="text-shadow: 1px 1px 0 var(--color-accent)">
        {{ listing.title }}
      </h3>
      <div class="mt-1.5 font-display font-bold text-lg text-brand-700">
        <span class="text-flare-deep">¥</span>{{ listing.price_min }}<span
          v-if="listing.price_max && listing.price_max !== listing.price_min"
          class="text-sm text-ink-soft"
        >–{{ listing.price_max }}</span>
      </div>
      <div class="mt-2 flex items-center justify-between font-mono text-xs text-ink-soft">
        <span class="truncate">{{ listing.seller_name }}</span>
        <span>{{ listing.created_at?.slice(0, 10) }}</span>
      </div>
    </div>
  </router-link>
</template>

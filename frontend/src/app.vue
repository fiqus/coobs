<template>
  <div>
    <component :is="layout">
      <router-view></router-view>
    </component>
  </div>
</template>

<script>
  export default {
    computed: {
      layout() {
        return `${this.$route.meta.layout || 'navbar'}-layout`;
      }
    }
  }
</script>

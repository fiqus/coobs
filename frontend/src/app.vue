<template>
  <div>
    <component :is="layout">
      <template v-slot:page-content>
        <router-view></router-view>
      </template>
    </component>
  </div>
</template>

<script>
export default {
  computed: {
    layout() {
      return `${this.$route.meta.layout || "navbar"}-layout`;
    }
  }
};
</script>

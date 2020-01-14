<template>
  <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center justify-content-between p-2 mb-3 rounded">
    <h3 class="h6 mb-0 text-gray-100">
      <i class="fas fa-exclamation-circle"></i>
      <span v-html="$t(error.message, error.message)"></span>
    </h3>
  </div>
</template>

<script>
  // Use this component in combination with error-handler mixin
  export default {
    props: {
      error: {
        type: Object,
        default: () => {
          return {
            exists: false,
            message: "",
            backgroundClass: "bg-danger"
          }
        }
      }
    }
  }
</script>


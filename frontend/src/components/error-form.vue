<template>
  <div v-if="error.exists" :class="error.backgroundClass" class="form-row d-sm-flex align-items-center justify-content-between p-2 mb-3 rounded h6 text-gray-100">
    <div class="col-11">
      <i class="fas fa-exclamation-circle"></i>
      <span class="ml-3" v-html="$t(error.message, error.message)"></span>
    </div>
    <div class="col-1 text-right">
      <button class="btn btn-sm btn-circle btn-danger" @click.prevent="close()">
        <i class="fas fa-times"></i>
      </button>
    </div>
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
    },
    methods: {
      close() {
        this.error.exists = false;
        this.$emit("clean");
      }
    }
  }
</script>


<template>
  <div class="form-group">
    <label>
      {{label}}
    </label>
    <input class="form-control"
      :class="{'is-invalid': error}"
      :name="name"
      :type="type"
      v-model="value"
      @input="onInput"/>
    <div v-if="error" class="invalid-feedback">
      {{errorMessage}}
    </div>
  </div>
</template>
<script>
export default {
  props: {
    value: {
      type: String
    },
    name: {
      type: String
    },
    type: {
      String,
      default: "text"
    },
    label: {
      type: String
    },
    error: {
      type: Boolean,
      default: false
    },
    errorMessage: {
      type: String
    }
  },
  methods: {
    onInput() {
      this.$emit('input', this.value);
    }
  }
}
</script>


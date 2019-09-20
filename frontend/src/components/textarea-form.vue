<template>
  <div class="form-group">
    <label v-if="label">
      {{label}}
    </label>
    <textarea class="form-control min-height-150"
      :class="{'is-invalid': error}"
      :name="name"
      :placeholder="placeholder"
      :type="type"
      v-model="value"
      @input="onInput">
    </textarea>
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
    },
    placeholder: {
      type: String,
      default: ""
    },
  },
  methods: {
    onInput() {
      this.$emit('input', this.value);
    }
  }
}
</script>


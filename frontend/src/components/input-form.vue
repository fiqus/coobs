<template>
  <div class="form-group">
    <label v-if="label">
      {{label}}
    </label>
    <input class="form-control form-control-user"
      :class="{'is-invalid': error}"
      :name="name"
      :placeholder="placeholder"
      :type="type"
      :disabled="disabled"
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
    },
    placeholder: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    onInput() {
      this.$emit("input", this.value);
    }
  }
};
</script>


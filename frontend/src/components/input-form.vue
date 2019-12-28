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
    <small v-if="helpText" class="form-text text-muted font-italic">{{helpText}}</small>
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
    },
    helpText: {
      type: String,
      default: ""
    }
  },
  methods: {
    onInput() {
      this.$emit("input", this.value);
    }
  }
};
</script>


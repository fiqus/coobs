<template>
  <div class="form-group">
    <select class="custom-select" :class="{'is-invalid': error}" v-model="value" @input="onInput">
      <option selected value="">{{defaultValue}}</option>
      <option v-for="option in options" :key="option.id" :value="option.id">
        {{option.name}}
      </option>
    </select>
    <div v-if="error" class="invalid-feedback">
      {{errorMessage}}
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      value: {
        type: Number
      },
      options: {
        type: Array
      },
      defaultValue: {
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
      onInput(event) {
        this.$emit('input', parseInt(event.target.value));
      }
    }
  }
</script>
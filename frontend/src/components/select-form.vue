<template>
  <div class="form-group">
    <select class="custom-select" v-model="value" @input="onInput">
      <option selected value="">{{defaultValue}}</option>
      <option v-for="option in options" :key="option.id" :value="option.id">
        {{option.name}}
      </option>
    </select>
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
      }
    },
    methods: {
      onInput(event) {
        this.$emit('input', parseInt(event.target.value));
      }
    }
  }
</script>
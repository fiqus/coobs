<template>
  <div class="form-group">
    <label v-if="label">
      {{label}}
    </label>
    <select class="custom-select" :class="{'is-invalid': error}" v-model="value" @input="onInput">
      <option v-if ="placeholder" value="null" disabled selected>{{$t('selectLabel')}} {{$t(placeholder)}}</option>
      <option v-if ="defaultValue" selected value="">{{defaultValue}}</option>
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
    label: {
      type: String
    },
    options: {
      type: Array
    },
    defaultValue: {
      type: String
    },
    placeholder: {
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
      this.$emit("input", parseInt(event.target.value));
    }
  }
};
</script>
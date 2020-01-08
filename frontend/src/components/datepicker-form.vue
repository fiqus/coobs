<template>
  <div class="form-group">
    <label>{{label}}</label>
    <datepicker
      :input-class="inputClasses"
      v-model="value"
      :format="format"
      :typeable="typeable"
      :disabled-dates="disabledDates"
      :use-utc="true"
      @selected="onDateSelected">
    </datepicker>
    <div v-if="error" class="invalid-feedback" :style="errorDivStyle">
      {{errorMessage}}
    </div>
  </div>
</template>

<script>
import Datepicker from "vuejs-datepicker";

export default {
  props: {
    value: {
      type: String
    },
    name: {
      type: String
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
    disabled: {
      type: Boolean,
      default: false
    },
    format: {
      type: String
    },
    typeable: {
      type: Boolean,
      default: false
    },
    disabledDates: {
      type: Object
    }
  },
  components: {
    "datepicker": Datepicker
  },
  computed: {
    inputClasses() {
      const classes = "form-control";
      return this.error ? `${classes} is-invalid` : classes;
    },
    errorDivStyle() {
      return this.error ? "display: block !important;" : "";
    }
  },
  methods: {
    onDateSelected(newDate) {
      this.$emit("input", newDate);
    },
  }
};
</script>


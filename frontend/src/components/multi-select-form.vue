<template>
  <div class="form-group">
    <label>{{label}}</label>
    <multiselect
      :class="{'is-invalid': error}"
      ref="refMultiselect"
      v-model="value"
      :placeholder="placeholder"
      track-by="id"
      label="name"
      :options="options"
      :multiple="true"
      :taggable="true"
      @input="onInput"
       />
    <div style="display: block !important;" v-if="error" class="invalid-feedback">
      {{errorMessage}}
    </div>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  components: {
    "multiselect": Multiselect,
  },
  props: {
    value: {
      type: Array
    },
    label: {
      type: String
    },
    options: {
      type: Array
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
    }
  },
  watch: {
    "error": function _watch$vpartnersInvolved$error (isInvalid) {
      const fixedClass = "multiselect__tags";
      if (!isInvalid) {
        this.$refs.refMultiselect.$refs.tags.className = fixedClass;
      } else {
        this.$refs.refMultiselect.$refs.tags.className = `${fixedClass} form-control form-control-user is-invalid`;
      }
    }
  },
  methods: {
    onInput() {
      this.$emit("input", this.value);
    }
  }
}
</script>


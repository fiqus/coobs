<template>
  <form v-on:submit.prevent="submitFilters">
    <div class="row">
      <div class="col-sm" v-for="(filter, idx) in filters" :key="idx">
        <select-form
          v-model="filter.value"
          :options="filter.options"
          :label="$t(filter.label, filter.label)">
        </select-form>
      </div>
    </div>

    <error-form :error="errorFilter" @clean="cleanError()"/>

    <div class="mb-3">
      <button type="submit" class="btn btn-warning">
        <i class="fa fa-filter"></i>
        {{$t("apply")}}
      </button>
      <button type="button" class="btn btn-secondary" @click.stop="cleanFilters()">
        <i class="fa fa-eraser"></i>
        {{$t("clean")}}
      </button>
    </div>
  </form>
</template>

<script>
  import {required} from "vuelidate/lib/validators";
  import SelectForm from "./select-form.vue";
  import ErrorForm from "./error-form.vue";
  import errorHandlerMixin from "./../mixins/error-handler";

  export default {
    props: {
      filters: {
        type: Array,
        required: true
      }
    },
    components: {
      "select-form": SelectForm,
      "error-form": ErrorForm
    },
    mixins: [errorHandlerMixin],
    computed: {
      filtersAreInvalid() {
        return Object.values(this.$v.filters.$each.$iter).every((filter) => {
          return filter.$error;
        });
      },
      errorFilter() {
        return {
          exists: this.filtersAreInvalid,
          message: "selectAtLeastOneFilter",
          backgroundClass: "bg-danger"
        }
      },
    },
    methods: {
      cleanError() {
        this.$v.filters.$reset();
      },
      cleanFilters() {
        this.filters.forEach((filter) => {
          filter.value = null;
        })
        this.$v.filters.$reset();
        this.$emit("applyFilters");
      },
      submitFilters() {
        this.$v.filters.$touch();
        if (!this.filtersAreInvalid) {
          const params = this.filters.reduce((acc, filter) => {
            if (filter.value) {
              acc[filter.key] = filter.value;
            }
            return acc;
          }, {});
          this.$emit("applyFilters", params);
        }
      },
    },
    validations: {
      filters: {
        $each: {
          value: {required}
        }
      }
    }
  }
</script>


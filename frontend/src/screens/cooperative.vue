<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t("editCooperative")}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        :label="$t('name')"
        name="name"
        type="text"
        v-model="cooperative.name"
        :disabled="false">
      </input-form>

      <input-form
        :label="$t('businessName')"
        name="business name"
        type="text"
        v-model="cooperative.businessName"
        :error="$v.cooperative.businessName.$error"
        error-message="Required">
      </input-form>
      <datepicker-form
        :label="$t('startingDate')"
        name="starting date"
        format="dd/MM/yyyy"
        v-model="cooperative.startingDate"
        @input="onDateSelected">
      </datepicker-form>

      <div class="form-row" v-if="$store.state.SDGEnabled">
        <div class="col-1 py-1">
          <bootstrap-toggle class="form-control"
            v-model="cooperative.sustainableDevelopmentGoalsActive"
            data-toggle="toggle"
            :options="{on: $t('yes'), off: $t('no'), onstyle: 'success', offstyle: 'danger', size: 'normal'}"
            :disabled="false" />
        </div>
        <div class="col-9">
          <label class="form-text ml-4">{{$t('sustainableDevelopmentGoalsActiveHelp')}}</label>
        </div>
      </div>
      <error-form :error="error" />

      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> {{$t("save")}}</button>
			</div>
    </form>
  </div>
</template>

<script>
import InputForm from "../components/input-form.vue";
import DatePickerForm from "../components/datepicker-form.vue";
import BootstrapToggle from "vue-bootstrap-toggle";
import swal from "sweetalert";
import {required} from "vuelidate/lib/validators";
import {httpGet} from "../api-client.js";
import ErrorForm from "../components/error-form.vue";
import errorHandlerMixin from "./../mixins/error-handler";

export default {
  components: {
    "input-form": InputForm,
    "datepicker-form": DatePickerForm,
    "bootstrap-toggle": BootstrapToggle,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
  created() {
    httpGet(`/cooperatives/${this.user.cooperativeId}`)
      .then((response) => {
        this.cooperative = response.data;
      });
  },
  data() {
    return {
      user: this.$store.state.user,
      cooperativeId: this.$store.state.user.cooperativeId,
      cooperative: {}
    };
  },
  methods: {
    onDateSelected(newDate) {
      this.cooperative.startingDate = new Date(newDate).toISOString().slice(0, 10);
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        this.$store.dispatch("updateCooperative", this.cooperative)
          .then(() => {
            swal(this.$t("editedCoopMsg"), {
              icon: "success",
              buttons: false,
              timer: 2000
            });
          })
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations: {
    cooperative: {
      businessName: {required}
    }
  }
};
</script>

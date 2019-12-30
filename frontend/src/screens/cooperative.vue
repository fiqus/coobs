<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
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
        @input="onDateSelected('from', $event)">
      </datepicker-form>
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
import swal from "sweetalert";
import {required} from "vuelidate/lib/validators";
import {httpGet, httpPut} from "../api-client.js";
import {getUser} from "../services/user-service";

export default {
  components: {
    "input-form": InputForm,
    "datepicker-form": DatePickerForm
  },
  created() {
    httpGet(`/cooperatives/${this.user.cooperativeId}`)
      .then((response) => {
        this.cooperative = response.data;
      });
  },
  data() {
    return {
      user: getUser(),
      cooperative: {},
      title: this.$t("editCooperative")
    };
  },
  methods: {
    onDateSelected(dateField, value) {
      this.cooperative[`startingDate_${dateField}`] = new Date(value).toISOString().slice(0,10);
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        httpPut(`/cooperatives/${this.user.cooperativeId}/`, this.cooperative)
          .then(() => {
            swal(this.$t("editedCoopMsg"), {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "cooperative"});
          })
      }
    }
  },
  validations: {
    cooperative: {
      businessName: {required}
    }
  }
}
</script>

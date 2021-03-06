<template>
  <div class="container">
    <div class="row justify-content-center p-sm-5">
      <div class="col-lg-8">
        <div class="text-left">
          <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
        </div>
      </div>

      <form v-on:submit.prevent="submit" class="col-lg-8 needs-validation" novalidate>
        <input-form
          :label="$t('name')"
          name="name"
          type="text"
          v-model="period.name"
          :error="$v.period.name.$error"
          :error-message="$t('required')">
        </input-form>

        <div class="row">
          <div class="col-12 col-sm-6">
            <datepicker-form
              :label="$t('from')"
              name="from"
              format="dd/MM/yyyy"
              v-model="from"
              :error="$v.from.$error"
              :error-message="$t('required')"
              @input="onDateSelected('from', $event)">
            </datepicker-form>
          </div>
          <div class="col-12 col-sm-6">
            <datepicker-form
              :label="$t('to')"
              name="to"
              format="dd/MM/yyyy"
              v-model="to"
              :disabled-dates="disabledDates"
              :error="$v.to.$error"
              :error-message="$t('required')"
              @input="onDateSelected('to', $event)">
            </datepicker-form>
          </div>
        </div>

        <div class="row">
          <div class="col-12 col-sm-4">
            <input-form
              :label="$t('budget')"
              name="money"
              type="number"
              v-model="period.actionsBudget"
              :error="$v.period.actionsBudget.$error"
              :error-message="budgetErrorMsg">
            </input-form>
          </div>
          <div class="col-12 col-sm-8 pt-sm-4 mb-4 mb-sm-0">
            <small class="form-text text-muted font-italic">{{$t('budgetHelp')}}</small>
          </div>
        </div>

        <error-form :error="error" />

        <div class="d-flex flex-column flex-sm-row mb-3">
          <button type="button" class="btn btn-secondary mb-3 mb-sm-0" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
          <button type="submit" class="btn btn-success ml-0 ml-sm-3"><i class="fa fa-save"></i> {{$t("save")}}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import InputForm from "../../components/input-form.vue";
import DatePickerForm from "../../components/datepicker-form.vue";
import {required, minValue} from "vuelidate/lib/validators";
import {httpGet, httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";
import ErrorForm from "../../components/error-form.vue";
import errorHandlerMixin from "./../../mixins/error-handler";

export default {
  components: {
    "input-form": InputForm,
    "datepicker-form": DatePickerForm,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
  created() {
    if (this.$route.params.periodId && this.$route.params.periodId !== "0") {
      httpGet(`/periods/${this.$route.params.periodId}`)
        .then((response) => {
          this.period = response.data;
          this.from = this.period.dateFrom;
          this.to = this.period.dateTo;
        });
    }
    return httpGet("/principles/")
      .then((response) => {
        this.principles = response.data;
      });
  },
  computed: {
    disabledDates() {
      return { to: new Date(this.from) };
    },
    budgetErrorMsg() {
      if (!this.$v.period.actionsBudget.$error) {
        return "";
      }
      if (!this.$v.period.actionsBudget.required) {
        return this.$t("required");
      }
      if (!this.$v.period.actionsBudget.minValue) {
        return this.$t("positiveNumber");
      }
      return "";
    }
  },
  data() {
    const isNew = this.$route.params.periodId == "0";
    return {
      period: {
        name: "",
        dateFrom: "",
        dateTo: "",
        actionsBudget: null
      },
      from: this.period ? this.period.dateFrom : "",
      to: this.period ? this.period.dateTo : "",
      principles: [],
      isNew,
      title: isNew ? "createPeriod" : "editPeriod"
    };
  },
  methods: {
    onDateSelected(dateField, value) {
      this.period[`date_${dateField}`] = new Date(value).toISOString().slice(0, 10);
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const periodId = this.$route.params.periodId;
        let promise = null;
        if (this.isNew) {
          promise = httpPost("periods/", this.period);
        } else {
          promise = httpPut(`/periods/${periodId}/`, this.period);
        }
        return promise
          .then(() => {
            const periodPerformed = this.isNew ? "created" : "edited";
            swal(`The period has been ${periodPerformed}!`, {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "periods-list"});
          })
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations: {
    from: {required},
    to: {required},
    period: {
      name: {required},
      actionsBudget: {required, minValue: minValue(0)}
    }
  }
};
</script>

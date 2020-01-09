<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        :label="$t('name')"
        name="name"
        type="text"
        v-model="period.name"
        :error="$v.period.name.$error"
        error-message="Required">
      </input-form>

      <div class="form-row">
        <div class="col-6">
          <datepicker-form
            :label="$t('from')"
            name="from"
            format="dd/MM/yyyy"
            v-model="from"
            :error="$v.from.$error"
            error-message="Required"
            @input="onDateSelected('from', $event)">
          </datepicker-form>
        </div>
        <div class="col-6">
          <datepicker-form
            :label="$t('to')"
            name="to"
            format="dd/MM/yyyy"
            v-model="to"
            :disabled-dates="disabledDates"
            :error="$v.to.$error"
            error-message="Required"
            @input="onDateSelected('to', $event)">
          </datepicker-form>
        </div>
      </div>

      <div class="form-row">
        <div class="col-3">
          <input-form
            :label="$t('budget')"
            name="money"
            type="number"
            v-model="period.actionsBudget">
          </input-form>
        </div>
      </div>

      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> {{$t("save")}}</button>
			</div>
    </form>
  </div>
</template>

<script>
import InputForm from "../../components/input-form.vue";
import DatePickerForm from "../../components/datepicker-form.vue";
import {required} from "vuelidate/lib/validators";
import {httpGet, httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";

export default {
  components: {
    "input-form": InputForm,
    "datepicker-form": DatePickerForm
  },
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
    }
  },
  data() {
    const isNew = this.$route.params.periodId == "0";
    return {
      period: {
        name: "",
        dateFrom: "",
        dateTo: ""
      },
      from: this.period ? this.period.dateFrom : "",
      to: this.period ? this.period.dateTo : "",
      principles: [],
      isNew,
      title: isNew ? this.$t("createPeriod") : this.$t("editPeriod")
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
          });
      }
    }
  },
  validations: {
    from: {required},
    to: {required},
    period: {
      name: {required}
    }
  }
};
</script>

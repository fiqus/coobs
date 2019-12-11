<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        label="Name"
        name="name"
        type="text"
        v-model="period.name"
        :error="$v.period.name.$error"
        error-message="Required">
      </input-form>

      <div class="form-row">
        <div class="col-6">
          <datepicker-form
            label="From"
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
            label="To"
            name="to"
            format="dd/MM/yyyy"
            v-model="to"
            :error="$v.to.$error"
            error-message="Required"
            @input="onDateSelected('to', $event)">
          </datepicker-form>
        </div>
      </div>

      <div class="form-row">
        <div class="col-3">
          <input-form
            label="Actions budget"
            name="money"
            type="number"
            v-model="period.actions_budget">
          </input-form>
        </div>
      </div>

      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> Cancel</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> Save</button>
			</div>
    </form>
  </div>
</template>

<script>
  import InputForm from "../../components/input-form.vue";
  import TextareaForm from "../../components/textarea-form.vue";
  import SelectForm from "../../components/select-form.vue";
  import DatePickerForm from '../../components/datepicker-form.vue';
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut, httpPost} from "../../api-client.js";
  import swal from 'sweetalert';

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "select-form": SelectForm,
      "datepicker-form": DatePickerForm
    },
    created() {
      if (this.$route.params.periodId && this.$route.params.periodId !== "0") {
        httpGet(`/periods/${this.$route.params.periodId}`)
          .then((response) => {
            this.period = response.data;
            this.from = this.period.date_from;
            this.to = this.period.date_to;
          });
      }
      return httpGet(`/principles/`)
        .then((response) => {
          this.principles = response.data;
        });
    },
    data() {
      const isNew = this.$route.params.periodId == "0";
      return {
        period: {
          name: "",
          date_from: "",
          date_to: ""
        },
        from: this.period ? this.period.date_from : "",
        to: this.period ? this.period.date_to : "",
        principles: [],
        isNew,
        title: isNew ? "Create period" : "Edit period"
      }
    },
    methods: {
      onDateSelected(dateField, value) {
        this.period[`date_${dateField}`] = new Date(value).toISOString().slice(0,10);
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
  }
</script>
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
        v-model="partner.name"
        :error="$v.partner.name.$error"
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
            v-model="partner.actions_budget">
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
import DatePickerForm from "../../components/datepicker-form.vue";
import {required} from "vuelidate/lib/validators";
import {httpGet, httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";

export default {
  components: {
    "input-form": InputForm,
    "textarea-form": TextareaForm,
    "select-form": SelectForm,
    "datepicker-form": DatePickerForm
  },
  created() {
    if (this.$route.params.partnerId && this.$route.params.partnerId !== "0") {
      httpGet(`/partners/${this.$route.params.partnerId}`)
        .then((response) => {
          this.partner = response.data;
          this.from = this.partner.date_from;
          this.to = this.partner.date_to;
        });
    }
    return httpGet("/principles/")
      .then((response) => {
        this.principles = response.data;
      });
  },
  data() {
    const isNew = this.$route.params.partnerId == "0";
    return {
      partner: {
        name: "",
        date_from: "",
        date_to: ""
      },
      from: this.partner ? this.partner.date_from : "",
      to: this.partner ? this.partner.date_to : "",
      principles: [],
      isNew,
      title: isNew ? "Create partner" : "Edit partner"
    };
  },
  methods: {
    onDateSelected(dateField, value) {
      this.partner[`date_${dateField}`] = new Date(value).toISOString().slice(0, 10);
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const partnerId = this.$route.params.partnerId;
        let promise = null;
        if (this.isNew) {
          promise = httpPost("partners/", this.partner);
        } else {
          promise = httpPut(`/partners/${partnerId}/`, this.partner);
        }
        return promise
          .then(() => {
            const partnerPerformed = this.isNew ? "created" : "edited";
            swal(`The partner has been ${partnerPerformed}!`, {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "partners-list"});
          });
      }
    }
  },
  validations: {
    from: {required},
    to: {required},
    partner: {
      name: {required}
    }
  }
};
</script>

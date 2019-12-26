<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        label="First Name"
        name="firstName"
        type="text"
        v-model="partner.first_name"
        error-message="Required">
      </input-form>

      <input-form
        label="Last Name"
        name="lastName"
        type="text"
        v-model="partner.last_name"
        error-message="Required">
      </input-form>


      <div class="form-row">
        <div class="col-3">
          <input-form
            label="Email"
            name="email"
            type="email"
            v-model="partner.email"
            error-message="Required">
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
import {required} from "vuelidate/lib/validators";
import {httpGet, httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";

export default {
  components: {
    "input-form": InputForm,
  },
  created() {
    if (this.$route.params.partnerId && this.$route.params.partnerId !== "0") {
      return httpGet(`/partners/${this.$route.params.partnerId}`)
        .then((response) => {
          this.partner = response.data;
        });
    }
  },
  data() {
    const isNew = this.$route.params.id == "0";
    return {
      partner: {
        firstName: "",
        lastName: "",
        email: ""
      },
      isNew,
      title: isNew ? "Create partner" : "Edit partner"
    };
  },
  methods: {
    submit() {
      this.$v.$touch();
      //if (!this.$v.$invalid) {
      if(true) {
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
    partner: {
      firstName: {required},
      lastName: {required},
      email: {required}
    }
  }
};
</script>

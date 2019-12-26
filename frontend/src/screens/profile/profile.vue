<template>
<div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">Hello {{partner.username}}!</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <div class="form-row">
        <div class="col-6">
          <input-form
            label="First name"
            name="first name"
            type="text"
            v-model="partner.first_name"
            :error="$v.partner.first_name.$error"
            error-message="Required">
          </input-form>
        </div>
        <div class="col-6">
          <input-form
            label="Last name"
            name="last name"
            type="text"
            v-model="partner.last_name"
            :error="$v.partner.last_name.$error"
            error-message="Required">
          </input-form>
        </div>
      </div>
      <div class="form-row">
        <div class="col-12">
          <input-form
            label="Username"
            name="username"
            type="text"
            v-model="partner.username"
            :error="$v.partner.username.$error"
            error-message="Required">
          </input-form>
        </div>
      </div>
      <div class="form-row">
        <div class="col-12">
          <input-form
            label="Email"
            name="email"
            type="text"
            v-model="partner.email"
            :error="$v.partner.email.$error"
            error-message="Required">
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
import {required} from "vuelidate/lib/validators";
import {httpGet, httpPut} from "../../api-client.js";
import swal from "sweetalert";
import {getUser} from "./../../services/user-service";

export default {
  components: {
    "input-form": InputForm
  },
  created() {
    const partnerId = getUser().id;
    httpGet(`/partners/${partnerId}/`)
      .then((response) => {
        this.partner = response.data;
      });
  },
  data() {
    return {
      partner: {},
      title: "Edit partner"
    };
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const partnerId = getUser().id;
        httpPut(`/partners/${partnerId}/`, this.partner)
          .then(() => {
            swal("The partner has been edited!", {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "partner"});
          });
      }
    }
  },
  validations: {
    partner: {
      username: {required},
      first_name: {required},
      last_name: {required},
      cooperative: {required},
      email: {required},
    }
  }
};
</script>

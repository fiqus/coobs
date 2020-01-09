<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        :label="$t('firstName')"
        name="firstName"
        type="text"
        v-model="partner.firstName"
        :error="$v.partner.firstName.$error"
        error-message="Required">
      </input-form>

      <input-form
        :label="$t('lastName')"
        name="lastName"
        type="text"
        v-model="partner.lastName"
        :error="$v.partner.lastName.$error"
        error-message="Required">
      </input-form>

      <input-form
        label="Email"
        name="email"
        type="email"
        v-model="partner.email"
        :error="$v.partner.email.$error"
        error-message="Required">
      </input-form>

      <input-form
        :label="$t('pass')"
        name="password"
        type="password"
        v-if="isNew"
        v-model="partner.password"
        :error="$v.partner.password.$error"
        error-message="Required">
      </input-form>

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
import {httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";
import * as api from "./../../services/api-service";

export default {
  components: {
    "input-form": InputForm,
  },
  async created() {
    const partnerId = this.$route.params.partnerId;
    if (partnerId && partnerId !== "0") {
      this.partner = await api.getPartner(partnerId);
    }
  },
  data() {
    const isNew = this.$route.params.partnerId == "0";
    return {
      partner: {
        firstName: "",
        lastName: "",
        email: "",
        password: ""
      },
      isNew,
      title: isNew ? "createPartner" : "editPartner"
    };
  },
  methods: {
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
    partner: {
      firstName: {required},
      lastName: {required},
      email: {required},
      password: {required}
    }
  }
};
</script>

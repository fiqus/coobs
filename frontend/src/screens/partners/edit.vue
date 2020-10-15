<template>
  <div class="container">
    <div class="row justify-content-center p-sm-5">
      <div class="col-lg-8">
        <div class="text-left">
          <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
        </div>
      </div>
      <form v-on:submit.prevent="submit" class="col-lg-8 needs-validation" novalidate>
        <div class="row">
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('firstName')"
              name="firstName"
              type="text"
              v-model="partner.firstName"
              :error="$v.partner.firstName.$error"
              error-message="Required">
            </input-form>
          </div>

          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('lastName')"
              name="lastName"
              type="text"
              v-model="partner.lastName"
              :error="$v.partner.lastName.$error"
              error-message="Required">
            </input-form>
          </div>
        </div>

        <input-form
          label="Email"
          name="email"
          type="email"
          v-model="partner.email"
          :error="$v.partner.email.$error"
          error-message="Required">
        </input-form>

        <div class="row">
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('password')"
              name="password"
              type="password"
              v-model="partner.password"
              :error="$v.partner.password && $v.partner.password.$error"
              :error-message="passwordErrorMessage"
              :help-text="$t('goodPasswordHelpText')">
            </input-form>
          </div>
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('confirmPassword')"
              name="confirm password"
              type="password"
              v-model="partner.confirmPassword"
              :error="$v.partner.confirmPassword && $v.partner.confirmPassword.$error"
              :error-message="$t('passwordNotMatch')">
            </input-form>
          </div>
        </div>

        <error-form :error="error" />

        <div class="d-flex flex-column flex-sm-row mb-3">
          <button type="button" class="btn btn-secondary mb-3 mb-sm-0" @click.stop="$router.go(-1)">
            <i class="fa fa-arrow-left"></i> {{$t("cancel")}}
          </button>
          <button type="submit" class="btn btn-success ml-0 ml-sm-3">
            <i class="fa fa-save"></i> {{$t("save")}}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import InputForm from "../../components/input-form.vue";
import ErrorForm from "../../components/error-form.vue";
import {required, minLength, sameAs} from "vuelidate/lib/validators";
import {httpPut, httpPost} from "../../api-client.js";
import swal from "sweetalert";
import * as api from "./../../services/api-service";
import errorHandlerMixin from "./../../mixins/error-handler";

export default {
  components: {
    "input-form": InputForm,
    "error-form": ErrorForm
  },
  async created() {
    const partnerId = this.$route.params.partnerId;
    if (partnerId && partnerId !== "0") {
      this.partner = await api.getPartner(partnerId);
    }
  },
  mixins: [errorHandlerMixin],
  computed: {
    passwordErrorMessage() {
      if (!this.$v.partner.password.$error) {
        return "";
      }
      if (!this.$v.partner.password.required) {
        return this.$t("required");
      }
      if (!this.$v.partner.password.goodPassword) {
        return this.$t("goodPasswordErrorMessage");
      }
      return "";
    }
  },
  data() {
    const isNew = this.$route.params.partnerId == "0";
    return {
      partner: {
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: ""
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
            const partnerPerformed = this.isNew ? this.$t("created") : this.$t("edited");
            swal(`${this.$t('partnerHasBeen')} ${partnerPerformed}!`, {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "partners-list"});
          })
          .catch((err) => {
            this.handleError(err);
          })
      }
    }
  },
  validations: {
    partner: {
      firstName: {required},
      lastName: {required},
      email: {required},
      password: {
        required,
        goodPassword: (password) => {
          return minLength(password, 8) &&
            /[a-zA-Z]/.test(password) &&
            /[1-9]/.test(password);
        }
      },
      confirmPassword: {sameAs: sameAs("password")}
    }
  }
};
</script>

<template>
  <div class="container">
    <div class="row justify-content-center p-sm-5">
      <div class="col-lg-8">
        <div class="text-left">
          <h1 class="h4 text-gray-900 mb-4">{{$t("profile")}}</h1>
        </div>
      </div>

      <form v-on:submit.prevent="submit" class="col-lg-8 needs-validation" novalidate>
        <div class="row">
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('firstName')"
              name="first name"
              type="text"
              v-model="partner.firstName"
              :error="$v.partner.firstName.$error"
              error-message="Required">
            </input-form>
          </div>
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('lastName')"
              name="last name"
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
          type="text"
          v-model="partner.email"
          :error="$v.partner.email.$error"
          error-message="Required">
        </input-form>

        <div class="form-group row">
          <div class="col-12 col-sm-3">
            <input-form
              class="mb-0"
              :label="$t('hoursToInvest')"
              name="hours"
              type="number"
              v-model="partner.hoursToInvest"
              :error="$v.partner.hoursToInvest.$error"
              :error-message="$t('positiveNumber')">
            </input-form>
          </div>
          <div class="col-12 col-sm-9 mt-sm-4  mb-sm-0">
            <small class="form-text text-muted font-italic">{{$t('hoursToInvestHelp')}}</small>
          </div>
        </div>

        <div class="form-row">
          <div class="col-12">
            <button type="button" class="btn btn-light border mb-3 text-gray-600" @click="changingPassword = !changingPassword">{{$t('changePassword')}}</button>
          </div>
        </div>

        <transition name="fade">
          <div class="row" v-if="changingPassword">
            <div class="col-12 col-sm-6">
              <input-form
                :label="$t('newPassword')"
                name="new password"
                type="password"
                v-model="partner.newPassword"
                :error="$v.partner.newPassword && $v.partner.newPassword.$error"
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
        </transition>

        <error-form :error="error" />

        <div class="d-flex flex-column flex-sm-row mb-3">
          <button type="button" class="btn btn-secondary mb-3 mb-sm-0" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
          <button type="submit" class="btn btn-success ml-0 ml-sm-3"><i class="fa fa-save"></i> {{$t("save")}}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s
  }
  .fade-enter, .fade-leave-to {
    opacity: 0
  }
</style>


<script>
import InputForm from "../../components/input-form.vue";
import {required, sameAs, minLength, minValue} from "vuelidate/lib/validators";
import {httpGet, httpPatch} from "../../api-client.js";
import swal from "sweetalert";
import ErrorForm from "../../components/error-form.vue";
import errorHandlerMixin from "./../../mixins/error-handler";

const requiredFields = (changingPassword) => {
  const validations = {
    firstName: {required},
    lastName: {required},
    email: {required},
    hoursToInvest: {minValue: minValue(0)}
  };
  if (changingPassword) {
    validations.newPassword = {
      required,
      goodPassword: (password) => {
        return minLength(password, 8) &&
          /[a-zA-Z]/.test(password) &&
          /[1-9]/.test(password);
      }
    };
    validations.confirmPassword = {sameAs: sameAs("newPassword")};
  }
  return {partner: validations};
}

export default {
  components: {
    "input-form": InputForm,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
  created() {
    this.loadProfile();
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    requiredFields() {
      return requiredFields(this.changingPassword);
    },
    passwordErrorMessage() {
      if (!this.$v.partner.newPassword || !this.$v.partner.newPassword.$error) {
        return "";
      }
      if (!this.$v.partner.newPassword.required) {
        return this.$t("required");
      }
      if (!this.$v.partner.newPassword.goodPassword) {
        return this.$t("goodPasswordErrorMessage");
      }
      return "";
    }
  },
  data() {
    return {
      changingPassword: false,
      partner: {}
    };
  },
  methods: {
    loadProfile() {
      const partnerId = this.user.id;
      return httpGet(`/partners/${partnerId}/`)
        .then((response) => {
          this.partner = response.data;
        });
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const partnerId = this.user.id;
        httpPatch(`/partners/${partnerId}/`, this.partner)
          .then(() => {
            swal(this.$t("partnerEdited"), {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.loadProfile()
              .then(() => {
                const currentUser = this.user;
                const {firstName, lastName, email, hoursToInvest} = this.partner;
                const newUser = Object.assign({}, currentUser, {firstName, lastName, email, hoursToInvest});
                this.$store.commit("setUser", newUser);
                this.$v.$reset();
              })
          })
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations() {
    return this.requiredFields;
  }
};
</script>

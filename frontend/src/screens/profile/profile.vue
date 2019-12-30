<template>
<div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t("profile")}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <div class="form-row">
        <div class="col-6">
          <input-form
            :label="$t('firstName')"
            name="first name"
            type="text"
            v-model="partner.firstName"
            :error="$v.partner.firstName.$error"
            error-message="Required">
          </input-form>
        </div>
        <div class="col-6">
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
      <div class="form-row">
        <div class="col-12">
          <button type="button" class="btn btn-light mb-3 text-gray-600" @click="changingPassword = !changingPassword">Change password</button>
        </div>
      </div>
      <transition name="fade">
        <div class="form-row" v-if="changingPassword">
          <div class="col-6">
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
          <div class="col-6">
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
      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> {{$t("save")}}</button>
			</div>
    </form>
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
import {required, sameAs, minLength} from "vuelidate/lib/validators";
import {httpGet, httpPatch} from "../../api-client.js";
import swal from "sweetalert";
import {getUser, saveUser} from "./../../services/user-service";

const requiredFields = (changingPassword) => {
  const validations = {
    firstName: {required},
    lastName: {required},
    email: {required}
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
    "input-form": InputForm
  },
  created() {
    this.loadProfile();
  },
  computed: {
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
      const partnerId = getUser().id;
      return httpGet(`/partners/${partnerId}/`)
        .then((response) => {
          this.partner = response.data;
        });
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const partnerId = getUser().id;
        httpPatch(`/partners/${partnerId}/`, this.partner)
          .then(() => {
            swal(this.$t("partnerEdited"), {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.loadProfile()
              .then(() => {
                const currentUser = getUser();
                const {firstName, lastName, email} = this.partner;
                const newUser = Object.assign({}, currentUser, {firstName, lastName, email});
                saveUser(newUser, this);
              })
          });
      }
    }
  },
  validations() {
    return this.requiredFields;
  }
};
</script>

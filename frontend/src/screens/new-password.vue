<template>
  <div class="row justify-content-center">
    <div class="col-xl-8 col-lg-10 col-md-7">
      <div class="sign-in o-hidden mt-5">
        <div class="card-body p-0">
          <div class="row">
            <div class="col-lg-2"></div>
            <div class="col-lg-8">
              <div class="p-5">
                <div class="text-center">
                  <h1 id="changePassTitle" class="h4 sign-in-text mb-4">{{$t('changePassTitle')}}</h1>
                  <div id="passwordChanged" hidden="hidden">
                    <h1 class="h4 sign-in-text mb-4">{{$t('passwordChanged-1')}}</h1>
                    <p class="mb-5">{{$t('passwordChanged-2')}}</p>
                  </div>
                </div>
                <form id="changePassForm" v-on:submit.prevent="submit" class="user needs-validation" novalidate>
                  <input-form
                    :label="$t('newPassword')"
                    name="new password"
                    type="password"
                    v-model="user.password"
                    :error="$v.user.password && $v.user.password.$error"
                    :error-message="passwordErrorMessage"
                    :help-text="$t('goodPasswordHelpText')">
                  </input-form>
                  <input-form
                    :label="$t('confirmPassword')"
                    name="confirm password"
                    type="password"
                    v-model="user.repeatPassword"
                    :error="$v.user.repeatPassword && $v.user.repeatPassword.$error"
                    :error-message="$t('passwordNotMatch')">
                  </input-form>
                  <error-form :error="error" />
                  <button id="changePasswordBtn" type="summary" class="btn btn-user btn-block btn-change-pass">{{$t("changePassword")}}</button>
                </form>
                <div class="text-center">
                  <a type="summary" id="signInBtn" hidden="hidden" class="btn btn-user btn-block btn-sign-in-dark" href="#/login">{{$t("login")}}</a>
                </div>                
              </div>
            </div>
            <div class="col-lg-2"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InputForm from '../components/input-form.vue'
import ErrorForm from "../components/error-form.vue";
import { required, email, minLength, sameAs } from 'vuelidate/lib/validators';
import {httpPost} from '../api-client';
import swal from 'sweetalert';

export default {
  components: {
    "input-form": InputForm,
    "error-form": ErrorForm
  },
  props:{
    token: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      user: {
        password: "",
        repeatPassword: ""
      }
    }
  },
  computed: {
    passwordErrorMessage() {
      if (!this.$v.user.newPassword || !this.$v.user.newPassword.$error) {
        return "";
      }
      if (!this.$v.user.newPassword.required) {
        return this.$t("required");
      }
      if (!this.$v.user.newPassword.goodPassword) {
        return this.$t("goodPasswordErrorMessage");
      }
      return "";
    }
  },  
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const body = {...this.user};
        var bodyFormData = new FormData();
        bodyFormData.set('password', `${body.password}`);
        bodyFormData.set('token', `${this.token}`);
        httpPost("/password_reset/confirm/", bodyFormData)
          .then((res) => {
            const {status} = res.data;
            document.getElementById('changePassTitle').setAttribute('hidden', 'hidden');
            document.getElementById('changePasswordBtn').setAttribute('hidden', 'hidden');
            document.getElementById('changePassForm').setAttribute('hidden', 'hidden');
            document.getElementById('passwordChanged').removeAttribute('hidden');
            document.getElementById('signInBtn').removeAttribute('hidden');
          })
          .catch((err) => {
            swal(err.response.data.detail.password[0], {
              icon: "error",
              buttons: false,
              timer: 2000              
            });
          });
      }
    }
  },
  validations: {
    user: {
      password: {
        required,
        goodPassword: (password) => {
          return minLength(password, 8) &&
            /[a-zA-Z]/.test(password) &&
            /[1-9]/.test(password);
        }
      },
      repeatPassword: {
        sameAsPassword: sameAs('password')
      }
    }
  }
}
</script>


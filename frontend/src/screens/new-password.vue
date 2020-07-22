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
                    name="password"
                    type="password"
                    v-model="user.password"
                    placeholder="Password..."
                    :error="$v.user.password.$error"
                    error-message="Ingrese un password válido">
                  </input-form>
                  <input-form
                    name="password"
                    type="password"
                    v-model="user.repeatPassword"
                    placeholder="Repeat..."
                    :error="$v.user.repeatPassword.$error"
                    error-message="Las passwords no coinciden">
                  </input-form>
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
import { required, email, sameAs } from 'vuelidate/lib/validators';
import {httpPost} from '../api-client';
import swal from 'sweetalert';

export default {
  components: {
    InputForm
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
            swal(err.response.data.detail, {
              icon: "error"
            });
          });
      }
    }
  },
  validations: {
    user: {
      password: {
        required
      },
      repeatPassword: {
        sameAsPassword: sameAs('password')
      }
    }
  }
}
</script>


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
                  <h1 class="h4 sign-in-text mb-4">{{$t('forgottenPassTitle')}}</h1>
                  <p v-if="!resentSent" class="mb-5">{{$t('forgottenPassDescription')}}</p>
                  <div v-if="resentSent">
                    <p class="mb-5">
                      {{$t('emailSentText-1')}} <br/>
                      {{$t('emailSentText-2')}}
                    </p>
                  </div>
                </div>
                <form v-on:submit.prevent="submit" class="user needs-validation" novalidate>
                  <input-form
                    name="email"
                    type="email"
                    v-model="user.email"
                    placeholder="Email"
                    :error="$v.user.email.$error"
                    :error-message="$t('invalidEmail')">
                  </input-form>
                  <button type="summary" class="btn btn-user btn-block btn-sign-in-dark">{{$t("sendForgottenPassEmail")}}</button>
                </form>
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
import { required, email } from 'vuelidate/lib/validators';
import {httpPost} from '../api-client';
import swal from 'sweetalert';

export default {
  components: {
    InputForm
  },
  data() {
    return {
      user: {
        email: ""
      },
      resentSent: false
    }
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const data = {email: this.user.email};
        httpPost("/password_reset/reset_password/", data, true)
          .then(() => {
            this.resentSent = true;
          })
          .catch((err) => {
            swal({
              title: "Error",
              text: err.response.data.detail.email[0],
              icon: "error",
              button: "OK",
              timer: 10000
            });
          });
      }
    }
  },
  validations: {
    user: {
      email: {
        required,
        email
      }
    }
  }
}
</script>


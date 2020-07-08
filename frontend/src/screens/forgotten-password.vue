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
                  <p id="forgottenPasswordDescrition" class="mb-5">{{$t('forgottenPassDescription')}}</p>
                  <div id="emailSent" hidden="hidden">
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
                    error-message="Ingrese un email válido">
                  </input-form>
                  <button type="summary" class="btn btn-user btn-block btn-sign-in">{{$t("sendForgottenPassEmail")}}</button>
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
      }
    }
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const body = {...this.user};
        var bodyFormData = new FormData();
        bodyFormData.set('email', `${body.email}`);
        //FIXME por alguna razón el proxy no funca
        // httpPost("/api/password_reset/reset_password/", bodyFormData)
        httpPost("http://localhost:8000/api/password_reset/reset_password/", bodyFormData)
          .then((res) => {
            const {status} = res.data;
            document.getElementById('forgottenPasswordDescrition').setAttribute('hidden', 'hidden');
            document.getElementById('emailSent').removeAttribute('hidden');
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
      email: {
        required,
        email
      }
    }
  }
}
</script>


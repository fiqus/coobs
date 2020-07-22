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
                  <h1 class="h4 sign-in-text">{{$t('loginTitle-1')}}</h1>
                  <h1 class="h4 sign-in-text mb-5">{{$t('loginTitle-2')}}</h1>
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
                  <input-form
                    name="password"
                    type="password"
                    v-model="user.password"
                    :placeholder="$t('password')"
                    :error="$v.user.password.$error"
                    error-message="Ingrese un password válido">
                  </input-form>
                  <button type="summary" class="btn btn-user btn-block btn-sign-in">{{$t("login")}}</button>
                </form>
                <hr>
                <div class="text-center">
                  <a class="small sign-in-bottom-text" @click.prevent="signup()" href="#">{{$t("createAccount")}}</a>
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
        email: "",
        password: ""
      }
    }
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const body = {...this.user};
        httpPost("/token/", body)
          .then((res) => {
            const {access, refresh} = res.data;
            const tokenData = this.$jwt.decode(access);
            this.$store.commit("setUser", {...tokenData.user, access, refresh});
            this.$store.commit("setCooperative", tokenData.cooperative);
            this.$router.push({name: "dashboard"});
          })
          .catch((err) => {
            swal(err.response.data.detail, {
              icon: "error"
            });
          });
      }
    },
    signup() {
     window.location = window.location.origin + '/#section-signup';
    },
  },
  validations: {
    user: {
      email: {
        required,
        email
      },
      password: {
        required
      }
    }
  }
}
</script>


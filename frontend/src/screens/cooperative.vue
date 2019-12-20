<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        label="Name"
        name="name"
        type="text"
        v-model="cooperative.name"
        :disabled="false">
      </input-form>

      <input-form
        label="Business name"
        name="business name"
        type="text"
        v-model="cooperative.business_name"
        :error="$v.cooperative.business_name.$error"
        error-message="Required">
      </input-form>
      <datepicker-form
        label="Starting date"
        name="starting date"
        format="dd/MM/yyyy"
        v-model="cooperative.starting_date"
        @input="onDateSelected('from', $event)">
      </datepicker-form>
      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> Cancel</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> Save</button>
			</div>
    </form>
  </div>
</template>

<script>
  import InputForm from "../components/input-form.vue";
  import TextareaForm from "../components/textarea-form.vue";
  import DatePickerForm from '../components/datepicker-form.vue';
  import BootstrapToggle from 'vue-bootstrap-toggle'
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut} from "../api-client.js";
  import swal from 'sweetalert';

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "bootstrap-toggle": BootstrapToggle,
      "datepicker-form": DatePickerForm
    },
    created() {
      // TODO deberíamos usar el cooperative id del usuario logueado
      // ${this.$route.params.cooperativeId}
      httpGet(`/cooperatives/1`)
        .then((response) => {
          this.cooperative = response.data;
        });
    },
    data() {
      return {
        cooperative: {},
        title: "Edit cooperative"
      }
    },
    methods: {
      onDateSelected(dateField, value) {
        this.cooperative[`starting_date_${dateField}`] = new Date(value).toISOString().slice(0,10);
      },      
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          // TODO deberíamos usar el cooperative id del usuario logueado
          httpPut(`/cooperatives/1/`, this.cooperative)
            .then(() => {
              swal("The cooperative has been edited!", {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              this.$router.push({name: "cooperative"});
            })
        }
      }
    },
    validations: {
      cooperative: {
        business_name: {required}
      }
    }
  }
</script>

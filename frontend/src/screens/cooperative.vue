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
        :disabled="false"
        :error="$v.cooperative.name.$error">
      </input-form>

      <textarea-form
        label="Business name"
        name="business name"
        type="text"
        v-model="cooperative.businessName"
        :error="$v.cooperative.businessName.$error"
        error-message="Required">
      </textarea-form>

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
  import BootstrapToggle from 'vue-bootstrap-toggle'
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut} from "../api-client.js";
  import swal from 'sweetalert';

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "bootstrap-toggle": BootstrapToggle
    },
    created() {
      httpGet(`http://127.0.0.1:8000/api/cooperatives/1`)
        .then((response) => {
          this.cooperative = response.data;
        });

      // if (this.$route.params.cooperativeId) {
      //   httpGet(`http://127.0.0.1:8000/api/cooperatives/${this.$route.params.cooperativeId}`)
      //     .then((response) => {
      //       this.cooperative = response.data;
      //     });
      // }
    },
    data() {
      return {
        cooperative: {},
        isNew: !Boolean(this.$route.params.cooperativeId),
        title: "Edit cooperative"
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          httpPut(`/cooperatives/${this.$route.params.cooperativeId}/`, this.cooperative)
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
        businessName: {required}
      }
    }
  }
</script>

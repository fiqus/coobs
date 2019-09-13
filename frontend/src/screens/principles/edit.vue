<template>
  <div class="row justify-content-center">
    <div class="col-lg-10">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-8 needs-validation" novalidate>
      <input-form
        label="Name"
        name="name"
        type="text"
        v-model="principle.name"
        :error="$v.principle.name.$error"
        error-message="Required">
      </input-form>

      <textarea-form
        label="Description"
        name="description"
        type="text"
        v-model="principle.description"
        :error="$v.principle.description.$error"
        error-message="Required">
      </textarea-form>

      <div class="action-bar-buttons">
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> Cancel</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> Save</button>
			</div>
    </form>
  </div>
</template>

<script>
  import InputForm from "../../components/input-form.vue";
  import TextareaForm from "../../components/textarea-form.vue";
  import {required} from "vuelidate/lib/validators";
  import {findPrinciple} from "../../mock-data";

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm
    },
    created() {
      if (this.$route.params.principleId) {
        this.principle = findPrinciple(this.$route.params.principleId)
      }
    },
    data() {
      return {
        principle: {
          name: "",
          description: ""
        },
        isNew: !Boolean(this.$route.params.principleId),
        title: this.isNew ? "Edit principle" : "Create a principle"
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
      }
    },
    validations: {
      principle: {
        name: {required},
        description: {required}
      }
    }
  }
</script>

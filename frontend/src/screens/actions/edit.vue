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
        v-model="action.name"
        :error="$v.action.name.$error"
        error-message="Required">
      </input-form>

      <textarea-form
        label="Description"
        name="description"
        type="text"
        v-model="action.description"
        :error="$v.action.description.$error"
        error-message="Required">
      </textarea-form>

      <datepicker-form
        label="Date"
        name="date"
        v-model="date"
        :error="$v.date.$error"
        error-message="Required"
        @input="onDateSelected">
      </datepicker-form>

      <select-form
        v-model="action.principle"
        :options="principles"
        default-value="Select a principle"
        :error="$v.action.principle.$error"
        error-message="Required">
      </select-form>

      <input-form
        label="Invested money"
        name="money"
        type="number"
        v-model="action.invested_money">
      </input-form>

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
  import SelectForm from "../../components/select-form.vue";
  import DatePickerForm from '../../components/datepicker-form.vue';
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut, httpPost} from "../../api-client.js";

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "select-form": SelectForm,
      "datepicker-form": DatePickerForm
    },
    created() {
      if (this.$route.params.actionId && this.$route.params.actionId !== "0") {
        httpGet(`/actions/${this.$route.params.actionId}`)
          .then((response) => {
            this.action = response.data;
            this.date = this.action.date;
          });
      }
      return httpGet(`/principles/`)
        .then((response) => {
          this.principles = response.data;
        });
    },
    data() {
      return {
        action: {},
        date: this.action ? this.action.date : "",
        principles: [],
        title: !this.$route.params.actionId ? "Create action" : "Edit action"
      }
    },
    methods: {
      onDateSelected(newDate) {
        this.action.date = new Date(newDate).toISOString().slice(0,10);
      },
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          const actionId = this.$route.params.actionId;
          let promise = null;
          if (!actionId) {
            promise = httpPost("actions/", this.action);
          } else {
            promise = httpPut(`/actions/${actionId}/`, this.action);
          }
          return promise
            .then(() => {
              const actionPerformed = !actionId ? "created" : "edited";
              swal(`The action has been ${actionPerformed}!`, {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              this.$router.push({name: "actions-list"});
            })
        }
      }
    },
    validations: {
      date: {required},
      action: {
        name: {required},
        description: {required},
        principle: {required}
      }
    }
  }
</script>

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

      <div class="form-group">
        <label>Date</label>
        <datepicker
          input-class="form-control width-30"
          v-model="date"
          @selected="onDateSelected">
        </datepicker>
      </div>

      <select-form
        v-model="action.principle"
        :options="principles"
        default-value="Select a principle">
      </select-form>

      <input-form
        label="Invested money"
        name="money"
        type="number"
        v-model="action.investedMoney"
        :error="$v.action.investedMoney.$error"
        error-message="Required">
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
  import Datepicker from 'vuejs-datepicker';
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut, httpPost} from "../../api-client.js";

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "select-form": SelectForm,
      "datepicker": Datepicker
    },
    created() {
      if (this.$route.params.actionId) {
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
        isNew: !this.$route.params.actionId,
        title: this.isNew ? "Create action" : "Edit action"
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
              swal("The action has been edited!", {
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
      action: {
        name: {required},
        description: {required},
        principle: {required},
        investedMoney: {required}
      }
    }
  }
</script>

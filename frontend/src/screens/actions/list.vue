<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">Actions</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'action-edit', params: {actionId: 0}}">
        Add new
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <custom-table
      :headers="headers"
      :data="actions"
      :actions="{edit: true, delete: true}"
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
  import {httpGet, httpDelete} from "../../api-client.js";
  import CustomTable from "../../components/custom-table.vue";
  import {formatText} from "../../utils";

  export default {
    components: {
      "custom-table": CustomTable
    },
    created() {
      httpGet("/actions")
        .then((response) => {
          this.actions = response.data;
        })
    },
    data() {
      return {
        headers: [
          {key: "date", value: "Date"},
          {key: "description", value: "Description", parser: (p) => formatText(p.description, 50)},
          {key: "principle", value: "Principle", parser: (p) => formatText(p.principle_name, 50)},
        ],
        actions: []
      }
    },
    methods: {
      onEdit(action) {
        this.$router.push({name: "action-edit", params: {actionId: action.id}});
      },
      onDelete(action) {
        httpDelete(`/actions/${action.id}`)
          .then(() => {
            swal("The action has been deleted!", {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            return httpGet("/actions")
              .then((response) => {
                this.actions = response.data;
              })
          });
      }
    }
  }
</script>

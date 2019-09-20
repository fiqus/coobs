<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">Actions</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'action-edit'}">
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
  import {httpGet} from "../../api-client.js";
  import CustomTable from "../../components/custom-table.vue";
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
          {key: "principle", value: "Principle", parser: (p) => formatText(p.principle, 50)},
        ],
        actions: []
      }
    },
    methods: {
      onEdit() {},
      onDelete() {}
    }
  }
</script>

<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">Principles</h3>
    </div>
    <custom-table
      :headers="headers"
      :data="principles"
      :actions="{edit: true}"
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
  import CustomTable from "../../components/custom-table.vue";
  import {formatText} from "../../utils";
  import {deletePrinciple} from "../../mock-data";
  import {httpGet} from "../../api-client.js";
  import swal from 'sweetalert';

  function parseBoolean(value) {
    const icon = value ? "check" : "times";
    return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
  }

  export default {
    components: {
      "custom-table": CustomTable
    },
    created() {
      httpGet("/principles")
        .then((response) => {
          this.principles = response.data;
        })
    },
    data() {
      return {
        headers: [
          {key: "name", value: "Name", parser: (p) => formatText(p.name)},
          {key: "description", value: "Description", parser: (p) => formatText(p.description, 50)},
          {key: "visible", value: "Visible", parser: (p) => parseBoolean(p.visible)},
        ],
        principles: []
      }
    },
    methods: {
      onEdit(principle) {
        this.$router.push({name: "principle-edit", params: {principleId: principle.id}});
      },
      onDelete(principle) {
        swal({
          title: "Are you sure?",
          text: "Once deleted, you will not be able to ...",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        })
        .then((willDelete) => {
          if (willDelete) {
            this.principles = deletePrinciple(principle.id);
            swal("The principle has been deleted!", {
              icon: "success",
            });
          }
        });
      }
    }
  }
</script>


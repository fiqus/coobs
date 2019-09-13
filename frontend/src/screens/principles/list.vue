<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">Principles</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'principle-edit'}">
        Add new
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <custom-table
      :headers="headers"
      :data="principles"
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
  import CustomTable from "../../components/custom-table.vue";
  import {formatText} from "../../utils";
  import {getPrinciples, deletePrinciple} from "../../mock-data";

  import swal from 'sweetalert';

  export default {
    components: {
      "custom-table": CustomTable
    },
    data() {
      return {
        headers: [
          {key: "name", value: "Name", parser: (p) => formatText(p.name)},
          {key: "description", value: "Description", parser: (p) => formatText(p.description, 50)},
        ],
        principles: getPrinciples()
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


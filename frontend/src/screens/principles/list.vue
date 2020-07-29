<template>
  <div class="custom-container">
    <div class="row">
      <h3 class="col-10">{{$t("principles")}}</h3>
    </div>
    <loader :loading='isLoading'/>
    <simple-table
      :headers="headers"
      :data="principles"
      :actions="{edit: true}"
      empty-state-msg="You don't have any principles yet!"
      @onEdit="onEdit">
    </simple-table>
  </div>
</template>

<script>
  import SimpleTable from "../../components/simple-table.vue";
  import {formatText} from "../../utils";
  import {deletePrinciple} from "../../mock-data";
  import {httpGet} from "../../api-client.js";
  import swal from 'sweetalert';
  import Loader from "../../components/loader-overlay.vue";

  function parseBoolean(value) {
    const icon = value ? "check" : "times";
    return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
  }

  export default {
    components: {
      "simple-table": SimpleTable,
      "loader": Loader
    },
    created() {
      httpGet("/principles")
        .then((response) => {
          this.principles = response.data;
          this.isLoading = false;
        })
    },
    data() {
      return {
        headers: [
          {key: "name", value:  "name", parser: (p) => formatText(this.$t(p.nameKey, p.name))},
          {key: "description", value:  "description", parser: (p) => formatText(p.description, 50)},
          {key: "visible", value:  "visible", parser: (p) => parseBoolean(p.visible)},
        ],
        principles: [],
        isLoading: true
      }
    },
    methods: {
      onEdit(principle) {
        this.$router.push({name: "principle-edit", params: {principleId: principle.id}});
      }
    }
  }
</script>


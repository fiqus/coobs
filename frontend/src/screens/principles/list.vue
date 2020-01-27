<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("principles")}}<i class="fas fa-fw fa-map-signs"></i></h3>
    </div>
    <spinner :loading='isLoading'/>
    <loader :loading='isLoading'/>
    <custom-table
      :headers="headers"
      :data="principles"
      :actions="{edit: true}"
      empty-state-msg="You don't have any principles yet!"
      @onEdit="onEdit">
    </custom-table>
  </div>
</template>

<script>
  import CustomTable from "../../components/custom-table.vue";
  import {formatText} from "../../utils";
  import {deletePrinciple} from "../../mock-data";
  import {httpGet} from "../../api-client.js";
  import swal from 'sweetalert';
  import Loader from "../../components/loader-overlay.vue";
  import Spinner from "../../components/spinner.vue";

  function parseBoolean(value) {
    const icon = value ? "check" : "times";
    return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
  }

  export default {
    components: {
      "custom-table": CustomTable,
      "loader": Loader,
      "spinner": Spinner      
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


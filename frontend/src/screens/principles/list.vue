<template>
  <div class="custom-container">
    <div class="row">
      <h3 class="col-10">{{$t("principles")}}</h3>
    </div>
    <loader :loading='isLoading'/>
    <detail-modal 
      :title="$t('principleDetail')">
      <template v-slot:modal-body>
        <label class="bold">{{$t('name')}}:</label>
        <span name="name"
          type="text">{{$t(modalPrinciple.principleData.nameKey)}}
        </span><br/>
        <label class="bold">{{$t('descriptionICA')}}:</label>
        <span name="description" type="text">
          {{$t(modalPrinciple.principleData.description)}}
        </span><br/>
        <label class="bold">{{$t('description')}}:</label>
        <div name="customDescription" v-html="modalPrinciple.principleData.customDescription"/><br/>        
      </template>
    </detail-modal>

    <simple-table
      :headers="headers"
      :data="principles"
      :actions="{edit: true, showViewButton: true}"
      empty-state-msg="You don't have any principles yet!"
      @onQuickView="onQuickView"
      @onEdit="onEdit">
    </simple-table>
  </div>
</template>

<script>
  import SimpleTable from "../../components/simple-table.vue";
  import {sanitizeHtml, formatText} from "../../utils";
  import {deletePrinciple} from "../../mock-data";
  import {httpGet} from "../../api-client.js";
  import swal from 'sweetalert';
  import Loader from "../../components/loader-overlay.vue";
  import DetailModal from "../../components/detail-modal.vue";
  import * as api from "./../../services/api-service";

  function parseBoolean(value) {
    const icon = value ? "check" : "times";
    return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
  }

  export default {
    components: {
      "simple-table": SimpleTable,
      "loader": Loader,
      "detail-modal": DetailModal
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
          // @TODO [DMC] Should we sanitize to display here?
          {key: "description", value:  "descriptionICA", parser: (p) => formatText(sanitizeHtml(p.description), 50)},
          {key: "visible", value:  "visible", parser: (p) => parseBoolean(p.visible)},
        ],
        principles: [],
        isLoading: true,
        modalPrinciple: {principleData:{}}
      }
    },
    methods: {
      onEdit(principle) {
        this.$router.push({name: "principle-edit", params: {principleId: principle.id}});
      },
      async onQuickView(principle) {
        const principleData = await api.getPrinciple(principle.id);
        this.modalPrinciple = {principleData};
        $('#detailModal').modal()
      }
    }
  }
</script>


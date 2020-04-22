<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("sustainableDevelopmentGoals")}}</h3>
    </div>
    <loader :loading='isLoading'/>

    <detail-modal 
      :title="$t('goalDetail')">
      <template v-slot:modal-body>
        <label class="bold">{{$t('name')}}:</label>
        <span name="name"
          type="text">{{modalAction.goalData.name}}
        </span><br/>
        <label class="bold">{{$t('description')}}:</label>
        <span name="description"
          type="text">
          {{modalAction.goalData.description}}
        </span><br/>
        <a :href=modalAction.goalData.url target="_blank">
          {{$t('moreInfo')}}
        </a><br/>
      </template>
    </detail-modal>

    <simple-table
      :headers="headers"
      :data="sustainableDevelopmentGoals"      
      :actions="{showViewButton: true}"
      :sortEnabled=true
      @onQuickView="onQuickView">
    </simple-table>
  </div>
</template>

<script>
  import SimpleTable from "../components/simple-table.vue";
  import DetailModal from "../components/detail-modal.vue";  
  import {formatText} from "../utils";
  import {httpGet} from "../api-client.js";
  import swal from 'sweetalert';
  import Loader from "../components/loader-overlay.vue";
  import * as api from "./../services/api-service";

  export default {
    components: {
      "simple-table": SimpleTable,
      "loader": Loader,
      "detail-modal": DetailModal
    },
    created() {
      return httpGet("/sustainable-development-goals")
        .then((response) => {
          this.sustainableDevelopmentGoals = response.data;
          this.isLoading = false;
        })
    },
    data() {
      return {
        headers: [
          {key: "name", value:  "name", parser: (g) => formatText(this.$t(g.nameKey, g.name))},
          {key: "description", value:  "description", parser: (g) => formatText(this.$t(g.descriptionKey, g.description), 50)}
        ],
        sustainableDevelopmentGoals: [],
        isLoading: true,
        modalAction: {goalData:{}}
      }
    },
    methods: {
      onQuickView(goal) {
        return api.getSustainableDevelopmentGoal(goal.id).then((goalData) => {
          this.modalAction = {goalData: goalData};
          $('#detailModal').modal();
        });
      }    
    }
  }
</script>


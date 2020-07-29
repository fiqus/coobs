<template>
  <div class="custom-container">
    <div class="row">
      <h3 class="col-10">{{$t("sdgObjectives")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'sdg-objectives-edit', params: {sdgObjectiveId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <loader :loading='isLoading'/>

    <detail-modal 
      :title="$t('sdgObjectiveDetail')">
      <template v-slot:modal-body>
        <label class="bold">{{$t('sustainableDevelopmentGoal')}}:</label>
        <span name="sdgName"
          type="text">{{$t(modalSDGObjective.sdgObjectiveData.sdgName)}}
        </span><br/>
        <label class="bold">{{$t('period')}}:</label>
        <span name="period"
          type="text">{{modalSDGObjective.sdgObjectiveData.periodName}}
        </span><br/>
        <label class="bold">{{$t('hoursToReach')}}:</label>
        <span name="hoursToReach"
          type="text">
          {{formatNumber(modalSDGObjective.sdgObjectiveData.hoursToReach)}}
        </span><br/>
        <label class="bold">{{$t('moneyToInvest')}}:</label>
        <span name="moneyToInvest"
          type="text">
          {{formatNumber(modalSDGObjective.sdgObjectiveData.moneyToInvest)}}
        </span><br/>
        <label class="bold">{{$t('actionsToPerform')}}:</label>
        <span name="actionsToPerform"
          type="text">
          {{modalSDGObjective.sdgObjectiveData.actionsToPerform}}
        </span><br/>
      </template>
    </detail-modal>

    <simple-table
      :headers="headers"
      :data="sdgObjectives"
      :actions="{edit: true, delete: true, showViewButton: true}"
      :empty-state-msg="$t('noSDGObjectivesMessage')" 
      :sortEnabled=true
      @onEdit="onEdit"
      @onDelete="onDelete"
      @onQuickView="onQuickView">
    </simple-table>
  </div>
</template>

<script>
import SimpleTable from "../../../components/simple-table.vue";
import DetailModal from "../../../components/detail-modal.vue";  
import {formatText, parseNumber} from "../../../utils";
import {httpGet, httpDelete} from "../../../api-client.js";
import swal from "sweetalert";
import Loader from "../../../components/loader-overlay.vue";
import * as api from "./../../../services/api-service";


export default {
  components: {
    "simple-table": SimpleTable,
    "loader": Loader,
    "detail-modal": DetailModal
  },
  created() {
    httpGet("/sdg-objectives")
      .then((response) => {
        this.sdgObjectives = response.data;
        this.isLoading = false;
      });
  },
  data() {
    return {
      headers: [
        {key: "period_name", value: "period", parser: (sdgObj) => formatText(sdgObj.periodName)},
        {key: "sdg_name", value: "sustainableDevelopmentGoal", parser: (sdgObj) => formatText(sdgObj.sdgName)}
        //TODO agregar traduccion para sdg
      ],
      sdgObjectives: [],
      isLoading: true,
      modalSDGObjective: {sdgObjectiveData:{}}
    };
  },
  methods: {
    formatNumber(number){
      return parseNumber(number, this.$i18n.locale());
    },
    onQuickView(sdgObj) {
      return api.getSDGObjective(sdgObj.id).then((sdgObjectiveData) => {
        this.modalSDGObjective = {sdgObjectiveData: sdgObjectiveData};
        $('#detailModal').modal();
      });
    },    
    onEdit(sdgObj) {
      this.$router.push({name: "sdg-objectives-edit", params: {sdgObjectiveId: sdgObj.id}});
    },
    onDelete(sdgObj) {
      swal({
        title: this.$t('areYouSure'),
        text: this.$t('onceSDGObjectiveDeleted'),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          httpDelete(`/sdg-objectives/${sdgObj.id}`)
            .then(() => {
              swal(this.$t("deletedSDGObjectiveMsg"), {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              return httpGet("/sdg-objectives")
                .then((response) => {
                  this.sdgObjectives = response.data;
                });
            });
        }
      });
    }
  }
};
</script>


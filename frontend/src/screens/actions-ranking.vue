<template>
  <div class="custom-container">
    <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center justify-content-between p-3">
      <h5 class="mb-0 text-gray-100">
        <i class="fas fa-exclamation-circle"></i>
        {{$t(error.message, error.message)}}
      </h5>
    </div>
    <div v-else>
      <loader :loading='isLoading'/>      
      <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="col-5">
          {{$t("actionsRanking")}}
        </h1>
        <div class="col-9">
          <small class="form-text text-muted font-italic ml-3">{{$t('actionsRankingHelp')}}</small>
        </div>        
      </div>
      <table class="table table-hover table-sm">
        <thead>
          <tr class="row">
            <th class="col-sm" scope="col">{{$t("cooperative")}}</th>
            <th v-for="principle in principles" class="col-sm align-center" v-align="center" scope="col" :key="principle.nameKey">{{$t(principle.nameKey)}}</th>
            <th class="col-sm align-right" scope="col">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="action in actionsByCoop" :key="action" class="row" v-bind:class="isCurrentCooperative(action.coopId)">
            <td class="col-sm">{{action.coopName}}</td>
            <td v-for="principle in action.actionsByPrinciple" :key="principle" class="col-sm" align="center">{{principle.value}}</td>
            <td class="col-sm font-weight-bold" align="right">{{action.total}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import {httpGet} from '../api-client';
  import Loader from "../components/loader-overlay.vue";

  export default {
    components: {
      "loader": Loader
    },    
    methods:{
      isCurrentCooperative(cooperativeId){
        if (this.$store.state.cooperative.id == cooperativeId) {
          return 'bg-gray-300';
        }
      },
      setErrorMsg(err){
        this.error = {
          exists: true,
          backgroundClass: " bg-danger",
          message: err.response.data.detail
        };
      },
      showActionsRanking(res){
        const {actions, principles} = res.data;
        if (!actions.length) {
          this.error = {
            exists: true,
            backgroundClass: " bg-warning",
            message: "notEnoughInfoForActionsRanking"
          };
          return;
        }

        function createCoopAcumObj(action){
          const actionsByPrinciple = principles.reduce((acc, principle) => {
            acc[principle.nameKey] = 0;
            return acc;
          }, []);
          return {"coopId": action.cooperativeId,"coopName": action.cooperativeName || action.cooperativeBusinessName, actionsByPrinciple, "total": 0};
        }
        
        const accumActionsByCoop = actions.reduce((acc, action) => {
          if (!acc[action.cooperativeId]) {
            acc[action.cooperativeId] = createCoopAcumObj(action);
          }

          acc[action.cooperativeId].actionsByPrinciple[action.principleNameKey] += action.actionsCount;
          acc[action.cooperativeId].total = actions.length;
          return acc;
        }, []);


        var actionsByCoop = accumActionsByCoop.reduce((acc, coop) => {
            coop.actionsByPrinciple = Object.keys(coop.actionsByPrinciple).map(k => {return {key: k, value: coop.actionsByPrinciple[k]}});
            acc.push(coop);
            return acc;
        }, []);
        this.actionsByCoop = actionsByCoop.sort((a, b) => {
            return a.coopName < b.coopName ? -1 : 1;
        });
        this.principles = principles;
      }
    },    
    created() {
      return httpGet('/actions-ranking')
        .then((res) => {
          this.showActionsRanking(res);
          this.isLoading = false;
        })
        .catch((err) => {
          this.setErrorMsg(err);
        })
    },
    data() {
      return {
        actionsByCoop: {},
        error: {
          exists: false,
          backgroundClass: " bg-danger",
          message: ""
        },
        isLoading: true
      }
    }
  }
</script>
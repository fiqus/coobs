<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
      <h6 class="m-0 font-weight-bold text-primary">{{objective.sdgName}}</h6>
    </div>
    <div class="card-body first-col-db" >
      <div>

        <!-- Hours -->
        <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('hoursToReach')}}</div>
        <div class="row no-gutters align-items-center">
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">0</div>
          </div>
          <div class="col center-col">
            <div class="progress progress-sm mr-2 progress-data">
              <div class="progress-bar custom-green" role="progressbar" :style=hoursProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{formatNumber(objective.hoursToReach)}}</div>
          </div>
        </div>
        <hr>

        <!-- Money -->
        <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('moneyToInvest')}}</div>
        <div class="row no-gutters align-items-center">
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">0</div>
          </div>
          <div class="col center-col">
            <div class="progress progress-sm mr-2 progress-data center">
              <div class="progress-bar custom-orange" role="progressbar" :style=moneyProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{formatNumber(objective.moneyToInvest)}}</div>
          </div>
        </div>
        <hr>

        <!-- Actions -->
        <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('actionsToPerform')}}</div>
        <div class="row no-gutters align-items-center">
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">0</div>
          </div>
          <div class="col center-col">
            <div class="progress progress-sm mr-2 progress-data">
              <div class="progress-bar custom-red" role="progressbar" :style=actionsProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
          <div class="col-3">
            <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{objective.actionsToPerform}}</div>
          </div>
        </div>
      </div>
      <div v-if="noActionsRelated" class="col-12">
        <small class="form-text text-muted font-italic ml-3">{{$t('noActionsRelatedToMonitor')}}</small>
      </div>
    </div>
  </div>
</template>

<script>
import { parseMoney } from "../utils";
export default {
  props: {
    objective: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatNumber(number) {
      return parseMoney(number);
    }
  },  
  computed: {
    hoursProgressStyle(){
      return `width: ${this.objective.investedHours / this.objective.hoursToReach * 100}%`;
    },
    moneyProgressStyle(){
      return `width: ${this.objective.investedMoney / this.objective.moneyToInvest * 100}%`;
    },
    actionsProgressStyle(){
      return `width: ${this.objective.performedActions / this.objective.actionsToPerform * 100}%`;
    },
    noActionsRelated(){
      return !(this.objective.investedHours && this.objective.investedMoney && this.objective.performedActions);
    }
  }
};
</script>


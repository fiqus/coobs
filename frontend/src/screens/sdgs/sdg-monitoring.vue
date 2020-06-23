<template>
    <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center p-3">
      <div class="col-sm-9">
        <h5 class="mb-0 text-gray-100">
          <i class="fas fa-exclamation-circle"></i>
          {{$t(error.message, error.message)}}
        </h5>
      </div>
      <div v-if="allPeriods.length" class="col-sm-2 float-right ">
        <div class="dropdown no-arrow float-right mx-3">
          <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
            <label class="text-gray-100">{{$t('periods')}}</label>
            <select id="period-select" class="ml-2 mr-5 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
              <option v-for="period in allPeriods" :key="period.id" :value="period.id">
                {{period.name}}
              </option>
            </select>
          </a>
        </div>
      </div>
    </div>
    <div v-else>
      <loader :loading='isLoading'/>
      <div>
        <!-- Page Heading -->
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
          <div class="dropdown no-arrow float-right">
            <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
              <label>{{$t('periods')}}</label>
              <select id="period-select" class="ml-2 mr-5 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
                <option v-for="period in allPeriods" :key="period.id" :value="period.id">
                  {{period.name}}
                </option>
              </select>
            </a>
          </div>
          <div class="col-9">
            <small class="form-text text-muted font-italic ml-3">{{$t('monitoringHelp')}}</small>
          </div>
        </div>
        <div v-for="(row, index) in monitoringData" :key="index" class="row">
          <div v-for="objective in row" :key="objective.id" class="col-xl-4 col-lg-4">
            <small-progress-card :objective="objective"></small-progress-card>
          </div>
        </div>
    </div>
  </div>
</template>

<script>
import * as api from "./../../services/api-service";
import Loader from "../../components/loader-overlay.vue";
import moment from "moment";
import _ from "lodash";
import SmallProgressCard from "../../components/small-progress-card.vue";

export default {
  components: {
    "loader": Loader,
    "small-progress-card": SmallProgressCard
  },
  methods: {
    formatData(data){
      let pos = 0;
      return data.reduce((acum, element, idx) => {
        if (idx !== 0 && idx % 3 === 0) {
          pos++;
        }
        if (!acum[pos]){
          acum[pos] = [];
        }
        acum[pos].push(element);
        return acum;
      }, []);
    },
    showMonitoringData(data){
      this.monitoringData = this.formatData(data.monitoringData);
      this.selectedValue = data.period.id;
      this.allPeriods = data.allPeriods;
      this.isLoading = false;
    },
    async onPeriodChange(){
      this.error.exists = false;
      const params = this.selectedValue ? {periodId: this.selectedValue} : {};
      const data = await api.getSDGMonitoringData(params);
      if (!data.monitoringData.length) {
        this.error = {
          exists: true,
          backgroundClass: " bg-danger",
          message: "notEnoughInfoForMonitoring"
        };
      } else {
        this.showMonitoringData(data);
      }
    }    
  },
  async created() {
    const data = await api.getSDGMonitoringData();
    if (!data.monitoringData.length) {
      this.error = {
        exists: true,
        backgroundClass: " bg-danger",
        message: "notEnoughInfoForMonitoring"
      };
    } else {
      this.showMonitoringData(data);
    }
  },
  toggleTooltip(){
    this.$refs.tooltip.$emit('toggle');
  },
  data() {
    return {
      periodName: "",
      allPeriods: [],
      selectedValue: [],
      error: {
        exists: false,
        backgroundClass: " bg-danger",
        message: ""
      },
      isLoading: true,
      monitoringData: {}
    };
  }
};
</script>

<template>
  <div class="container">
    <div v-if="error" class="d-sm-flex align-items-center justify-content-between p-3 bg-danger">
      <h3 class="h5 mb-0 text-gray-100">
        <i class="fas fa-exclamation-circle"></i>
        {{error}}
      </h3>
    </div>
    <div v-else>
      <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h3 class="h5 mb-0 text-gray-800">
          {{$t("balanceSubtitle", {period: period.name, from: period.dateFrom, to: period.dateTo, budget: period.actionsBudget})}}
        </h3>
      </div>

      <balance-by-period-table v-for="(periodSummary, idx) in actionsByPeriod" :key="idx"
        :period-summary="periodSummary">
      </balance-by-period-table>
    </div>
  </div>
</template>

<script>
  import {httpGet} from '../api-client';
  import BalanceByPeriodTable from '../components/balance-by-period-table.vue';

  export default {
    components: {
      BalanceByPeriodTable
    },
    created() {
      return httpGet('/dashboard')
        .then((res) => {
          const {period, actions, principles} = res.data;
          this.actionsByPeriod = actions.reduce((obj, action) => {
            if (!Object.keys(obj).includes(action.principle)) {
              obj[action.principle] = {
                principleNameKey: action.principleNameKey,
                actions: []
              };
            }
            const {date, description, investedMoney, name} = action;
            obj[action.principle].actions.push({date, description, investedMoney, name});
            return obj;
          }, {});
          this.period = period;
        })
        .catch((err) => {
          this.error = err.response.data.detail;
        })
    },
    data() {
      return {
        actionsByPeriod: {},
        period: {},
        error: ""
      }
    }
  }
</script>

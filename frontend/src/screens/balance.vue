<template>
  <div class="container">
    <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center justify-content-between p-3">
      <h3 class="h5 mb-0 text-gray-100">
        <i class="fas fa-exclamation-circle"></i>
        {{$t(error.message, error.message)}}
      </h3>
    </div>
    <div v-else>
      <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h3 class="h5 mb-0 text-gray-800">
          {{$t("balanceSubtitle", {period: period.name, from: period.dateFrom, to: period.dateTo, budget: Number(period.actionsBudget)})}}
        </h3>
        <button type="button" class="btn btn-primary">{{$t("downloadBalance")}} <i class="fas fa-file-download"/></button>
      </div>

      <balance-by-period-table v-for="(periodSummary, idx) in actionsByPeriod" :key="idx"
        :period-summary="periodSummary">
      </balance-by-period-table>

      <table class="table table-hover">
        <thead>
          <tr class="row table-info h5">
            <th class="col-sm-10" scope="colgroup" colspan="4">{{$t("totalInvested")}}</th>
            <th class="col-sm-2" scope="col">${{totalInvested}}</th>
          </tr>
        </thead>
      </table>
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
          if (!period || !actions || !actions.length) {
            this.error = {
              exists: true,
              backgroundClass: " bg-warning",
              message: "notEnoughInfoForBalance"
            };
            return;
          }
          let invested = 0;
          this.actionsByPeriod = actions.reduce((obj, action) => {
            if (!Object.keys(obj).includes(action.principle)) {
              obj[action.principle] = {
                principleNameKey: action.principleNameKey,
                actions: []
              };
            }
            const {date, description, investedMoney, name} = action;
            invested += Number(investedMoney);
            obj[action.principle].actions.push({date, description, investedMoney, name});
            return obj;
          }, {});
          this.period = period;
          this.totalInvested = invested;
        })
        .catch((err) => {
          this.error = {
            exists: true,
            backgroundClass: " bg-danger",
            message: err.response.data.detail
          };
        })
    },
    data() {
      return {
        actionsByPeriod: {},
        totalInvested: 0,
        period: {},
        error: {
          exists: false,
          backgroundClass: " bg-danger",
          message: ""
        }
      }
    }
  }
</script>

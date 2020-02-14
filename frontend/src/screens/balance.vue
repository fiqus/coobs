<template>
  <div class="container">
    <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center justify-content-between p-3">
      <h5 class="mb-0 text-gray-100">
        <i class="fas fa-exclamation-circle"></i>
        {{$t(error.message, error.message)}}
      </h5>
      <div v-if="allPeriods.length">
        <div class="dropdown no-arrow float-right mx-3">
          <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
            <select class="period-select mr-2 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
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
      <div v-if="downloading">
        <button type="button" class="btn btn-primary float-right my-n1" v-on:click="download" :title='$t("downloadBalance")' disabled="true">{{$t("downloading")}}...
          <b-spinner small type="grow"></b-spinner>
        </button>
      </div>
      <div v-else>
        <button type="button" class="btn btn-primary float-right my-n1" v-on:click="download" :title='$t("downloadBalance")'>{{$t("downloadBalance")}}</button>
      </div>
      <div class="dropdown no-arrow float-right mx-3">
        <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
          <select id="period-select" class="mr-2 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
            <option v-for="period in allPeriods" :key="period.id" :value="period.id">
              {{period.name}}
            </option>
          </select>
        </a>
      </div>
      <div id="nodeToRenderAsPDF">
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
          <h3 class="h5 mb-0 text-gray-800">
            {{$t("balanceSubtitle", {period: period.name, from: period.dateFrom, to: period.dateTo, budget: Number(period.actionsBudget)})}}
          </h3>
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
  </div>
</template>

<script>
import {httpGet} from "../api-client";
import BalanceByPeriodTable from "../components/balance-by-period-table.vue";
import html2pdf from "html2pdf.js";
import Loader from "../components/loader-overlay.vue";

function print(period, translator, parent){
  const self = parent;
  const html = $("#nodeToRenderAsPDF")[0];
  const opt = {
    margin:       [5, 5, 5, 5],
    filename:     `Balance - ${period.name}.pdf`,
    image:        { type: "jpg", quality: 0.98 },
    html2canvas:  { scale: 1 },
    jsPDF:        { unit: "mm", format: "a4", orientation: "portrait"},
    pagebreak:    {mode: ["avoid-all", "css"]}
  };

  html2pdf().from(html).set(opt).toPdf().get("pdf").then((pdf) => {
    var totalPages = pdf.internal.getNumberOfPages();

    for (let i = 1; i <= totalPages; i++) {
      pdf.setPage(i);
      pdf.setFontSize(10);
      pdf.setTextColor(150);
      pdf.text(translator("page") + " " + i + " " + translator("of") + " " + totalPages, pdf.internal.pageSize.width/2-10, pdf.internal.pageSize.height - 5);
    } 
  }).save().then(() => {
    self.downloading = false;
  });
}

export default {
  components: {
    BalanceByPeriodTable,
    "loader": Loader
  },
  methods: {
    setErrorMsg(err){
      this.error = {
        exists: true,
        backgroundClass: " bg-danger",
        message: err.response.data.detail
      };
    },
    download() {
      this.downloading = true;
      print(this.period, this.$t, this);
    },
    showBalance(res){
      const {period, actions, allPeriods, totalInvested} = res.data;
      if (!period || !actions || !actions.length) {
        this.error = {
          exists: true,
          backgroundClass: " bg-warning",
          message: "notEnoughInfoForBalance"
        };
        return;
      }
      this.allPeriods = allPeriods;
      this.actionsByPeriod = actions.reduce((obj, action) => {
        if (!action.public) {
          return obj;
        }
        if (!Object.keys(obj).includes(action.principle.toString())) {
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
      this.selectedValue = period.id;
      this.totalInvested = totalInvested;
      this.isLoading = false;
    },
    async onPeriodChange(){
      this.error.exists = false;
      const params = this.selectedValue ? {periodId: this.selectedValue} : {};
      return httpGet("/balance", params)
        .then((res) => {
          this.showBalance(res);
        })
        .catch((err) => {
          this.setErrorMsg(err);
        });
    }      
  },    
  created() {
    return httpGet("/balance")
      .then((res) => {
        this.showBalance(res);
      })
      .catch((err) => {
        this.setErrorMsg(err);
      });
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
      },
      allPeriods: [],
      selectedValue: [],
      downloading: false,
      isLoading: true
    };
  }
};
</script>
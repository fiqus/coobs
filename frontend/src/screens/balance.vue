<template>
  <div class="custom-container">
    <loader :loading='isLoading'/>

    <div v-if="error.exists" :class="error.backgroundClass" class="p-3">
      <h5 class="mb-0 text-gray-100">
        <i class="fas fa-exclamation-circle"></i>
        {{$t(error.message, error.message)}}
      </h5>
    </div>
    <div v-else-if="!isLoading && existsCurrentPeriod">
      <div class="float-right ml-5 col-sm-2">
        <button type="button" class="btn btn-primary my-n1" v-on:click="download" :disabled="downloading || !currentPeriodHasActions">
          {{downloading ? `${$t("downloading")}...` : $t("downloadBalance")}}
          <b-spinner v-if="downloading" small type="grow"></b-spinner>
        </button>
      </div>
      <div class="dropdown no-arrow float-right mx-3 col-sm-2">
        <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
          <label>{{$t('periods')}}</label>
          <select id="period-select" class="ml-2 mr-2 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
            <option v-for="period in allPeriods" :key="period.id" :value="period.id">
              {{period.name}}
            </option>
          </select>
        </a>
      </div>
      <div class="d-sm-flex align-items-center justify-content-between mb-4 col-sm-7">
        <h3 class="h5 mb-0 text-gray-800">
          {{$t("balanceSubtitle", {period: period.name, from: format(period.dateFrom), to: format(period.dateTo), budget: formatNumber(Number(period.actionsBudget))})}}
        </h3>
      </div>
    </div>

    <missing-data-empty-state v-if="!error.exists && !isLoading && (!existsCurrentPeriod || !currentPeriodHasActions)"
      :hasPeriod="existsCurrentPeriod"
      :hasActions="currentPeriodHasActions">
    </missing-data-empty-state>
    <div v-else-if="!isLoading && existsCurrentPeriod && currentPeriodHasActions">
      <div id="nodeToRenderAsPDF">
        <balance-by-period-table groupedBy="principle" v-for="(periodSummary, idx) in actionsByPeriod" :key="idx"
          :period-summary="periodSummary">
        </balance-by-period-table>

        <table class="table table-hover">
          <thead>
            <tr class="row table-info h5">
              <th class="col-sm-8" scope="colgroup" colspan="4">{{$t("totalInvested")}}</th>
              <th class="col-sm-2 align-right" scope="col">{{formatNumber(totalHoursInvested)}}</th>
              <th class="col-sm-2 align-right" scope="col">${{formatNumber(totalInvested)}}</th>
            </tr>
          </thead>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import * as api from "../services/api-service";
import BalanceByPeriodTable from "../components/balance-by-period-table.vue";
import html2pdf from "html2pdf.js";
import Loader from "../components/loader-overlay.vue";
import {sanitizeMarkdown, formatToUIDate, parseNumber} from "../utils";
import MissingDataEmptyState from "../components/missing-data-empty-state.vue";

function print(period, translator, parent) {
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

const uncollapseEveryElement = () => {
  let elementsToUncollapse = $('#nodeToRenderAsPDF').find('tr.collapse');
  elementsToUncollapse.push(...$('#nodeToRenderAsPDF').find('tbody.collapse'));
  for (var i=0, len=elementsToUncollapse.length|0; i<len; i=i+1|0) {
      elementsToUncollapse[i].classList.add('show');
  }  
}

export default {
  components: {
    BalanceByPeriodTable,
    "loader": Loader,
    "missing-data-empty-state": MissingDataEmptyState,
  },
  methods: {
    format(date) {
      return formatToUIDate(date);
    },
    formatNumber(number) {
      return parseNumber(number, this.$i18n.locale());
    },
    setErrorMsg(err) {
      if (err && err.response && err.response.data && err.response.data.detail) {
        this.error = {
          exists: true,
          backgroundClass: " bg-danger",
          message: err.response.data.detail
        };
      } else {
        console.error(err);
      }
    },
    download() {
      this.downloading = true;
      uncollapseEveryElement();
      print(this.period, this.$t, this);
    },
    showBalance(res) {
      const {period, actions, allPeriods, totalInvested, totalHoursInvested} = res.data;
      this.existsCurrentPeriod = period.id || period.length;
      this.currentPeriodHasActions = actions && actions.length;
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
        const {date, description, investedMoney, investedHours, name} = action;
        obj[action.principle].actions.push({date, description: sanitizeMarkdown(description), investedMoney, investedHours, name});
        return obj;
      }, {});
      this.period = period;
      this.selectedValue = period.id;
      this.totalHoursInvested = totalHoursInvested;
      this.totalInvested = totalInvested;
      this.isLoading = false;
    },
    async onPeriodChange() {
      this.error.exists = false;
      this.isLoading = true;
      const params = this.selectedValue ? {periodId: this.selectedValue} : {};
      return api.getBalance(params)
        .then((res) => {
          this.showBalance(res);
        })
        .catch((err) => {
          this.isLoading = false;
          this.setErrorMsg(err);
        });
    }
  },
  created() {
    return api.getBalance()
      .then((res) => {
        this.showBalance(res);
      })
      .catch((err) => {
        this.isLoading = false;
        this.setErrorMsg(err);
      });
  },
  data() {
    return {
      actionsByPeriod: {},
      totalInvested: 0,
      totalHoursInvested: 0,
      period: {},
      error: {
        exists: false,
        backgroundClass: " bg-danger",
        message: ""
      },
      allPeriods: [],
      selectedValue: [],
      downloading: false,
      isLoading: true,
      existsCurrentPeriod: false,
      currentPeriodHasActions: false,
    };
  }
};
</script>
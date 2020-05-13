<template>
<div class="container-fluid">
  <table class="table table-hover">
    <thead>
      <tr class="row thead-light">
        <th v-if="groupedBy === 'sdg'" class="col-sm-12" scope="colgroup" colspan="4">{{$t(periodSummary.objectiveNameKey, periodSummary.objectiveNameKey)}}</th>
        <th v-if="groupedBy !== 'sdg'" class="col-sm-12" scope="colgroup" colspan="4">{{$t(periodSummary.principleNameKey, periodSummary.principleNameKey)}}</th>
      </tr>
      <tr class="row">
        <th class="col-sm-3" scope="col">{{$t("action")}}</th>
        <th class="col-sm-5" scope="col">{{$t("description")}}</th>
        <th class="col-sm-2" scope="col">{{$t("date")}}</th>
        <th class="col-sm-2 align-right" scope="col">{{$t("investedMoney")}}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="action in periodSummary.actions" :key="action.name" class="row">
        <td class="col-sm-3">{{action.name}}</td>
        <td class="col-sm-5">{{action.description}}</td>
        <td class="col-sm-2">{{action.date | formatToUIDate}}</td>
        <td class="col-sm-2" align="right">${{formatNumber(Number(action.investedMoney))}}</td>
      </tr>
    </tbody>
  </table>
  </div>
</template>

<script>
import {parseMoney} from "../utils";
export default {
  props: {
    periodSummary: {
      type: Object,
      required: true
    },
    groupedBy: String
  },
  methods: {
    formatNumber(number) {
      return parseMoney(number);
    }
  }  
};
</script>


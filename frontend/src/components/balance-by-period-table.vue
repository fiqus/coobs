<template>
<div class="container-fluid">
  <table class="table table-hover">
    <thead>
      <tr class="row thead-light cursorPointer" @click.stop="expanded = !expanded">
        <th v-if="groupedBy === 'sdg'" class="col-sm-12" scope="colgroup" colspan="4">{{$t(periodSummary.objectiveNameKey, periodSummary.objectiveNameKey)}}</th>
        <th v-if="groupedBy !== 'sdg'" class="col-sm-12" scope="colgroup" colspan="4">{{$t(periodSummary.principleNameKey, periodSummary.principleNameKey)}}</th>
      </tr>
      <tr :class="{'show': expanded}" class="row collapse">
        <th class="col-sm-2" scope="col">{{$t("date")}}</th>
        <th class="col-sm-2" scope="col">{{$t("action")}}</th>
        <th class="col-sm-4" scope="col">{{$t("description")}}</th>
        <th class="col-sm-2 align-right" scope="col">{{$t("investedHours")}}</th>
        <th class="col-sm-2 align-right" scope="col">{{$t("investedMoney")}}</th>
      </tr>
    </thead>
    <tbody :class="{'show': expanded}" class="collapse">
      <tr v-for="action in periodSummary.actions" :key="action.name" class="row">
        <td class="col-sm-2">{{action.date | formatToUIDate}}</td>
        <td class="col-sm-2">{{action.name}}</td>
        <td class="col-sm-4" v-html="action.description"></td>
        <td class="col-sm-2" align="right">{{Number(action.investedHours)|| 0}}</td>
        <td class="col-sm-2" align="right">${{formatNumber(Number(action.investedMoney))}}</td>
      </tr>
    </tbody>
  </table>
  </div>
</template>

<script>
import {sanitizeMarkdown, parseNumber} from "../utils";

export default {
  props: {
    periodSummary: {
      type: Object,
      required: true
    },
    groupedBy: String
  },
  created(){
    this.periodSummary.actions.map( action => {
      action.description = sanitizeMarkdown(action.description);
      return action;
    })
  },
  methods: {
    formatNumber(number) {
      return parseNumber(number, this.$i18n.locale());
    }
  },
  data() {
    return {
      expanded: true
    }
  }
};
</script>


<template>
  <div class="custom-container">

    <h2>{{$t("publicActionsFeed")}}</h2>
    <loader :loading='isLoading'/>

    <detail-modal
      :title="$t('actionDetail')">
      <template v-slot:modal-body>
        <label class="bold">{{$t('name')}}:</label>
        <span name="name"
          type="text">{{modalAction.actionData.name}}
        </span><br/>
        <label class="bold">{{$t('description')}}:</label>
        <div name="description" v-html="modalAction.actionData.description">
        </div><br/>
        <!-- <span name="description"
          type="text">
          {{modalAction.actionData.description}}
        </span><br/> -->
        <label class="bold">{{$t('principles')}}:</label><br/>
        <span class="multiselect__tag" v-for="principle in modalAction.actionData.principles" v-bind:key="principle" 
          name="principles" type="text">
          {{$t(principle.nameKey)}}
        </span><br/>
        <div v-if="$store.state.cooperative.sustainableDevelopmentGoalsActive">
          <label class="bold">{{$t('sustainableDevelopmentGoals')}}:</label><br/>
          <span class="multiselect__tag" v-for="goal in modalAction.actionData.sustainableDevelopmentGoals" v-bind:key="goal" 
            name="sustainableDevelopmentGoals" type="text">
            {{$t(goal.name)}}
          </span><br/>
        </div>
        <label class="bold">{{$t('partners')}}:</label><br/>
        <span class="multiselect__tag" v-for="partner in modalAction.actionData.partnersSelected" v-bind:key="partner" 
          name="partners" type="text">
          {{partner}}
        </span><br/>
        <label class="bold">{{$t('startingDate')}}:</label>
        <span name="startingDate"
          type="text">{{modalAction.actionData.date | formatToUIDate}}
        </span><br/>
        <label class="bold">{{$t('investedHours')}}:</label>
        <span name="investedHours"
          type="text">{{formatNumber(modalAction.actionData.investedHours)}}
        </span><br/>
        <label class="bold">{{$t('investedMoney')}}:</label>
        <span name="investedMoney"
          type="text">$ {{formatNumber(modalAction.actionData.investedMoney)}}
        </span><br/>
      </template>
    </detail-modal>

    <simple-table v-if="actions.length"
        :headers="headers"
        :data="actions"
        :actions="{edit: false, delete: false, showViewButton: true}"
        :empty-state-msg="$t('emptyActionMsg')"
        :pagination="pagination"
        :ordering="ordering"
        @onQuickView="onQuickView">
    </simple-table>
    <div v-if="!actions.length">{{$t('emptyActionMsg')}}</div>
  </div>
</template>

<script>
import SimpleTable from "../../components/simple-table.vue";
import DetailModal from "../../components/detail-modal.vue";
import Loader from "../../components/loader-overlay.vue";
import {sanitizeMarkdown, formatText, capitalizeFirstChar, formatToUIDate, parseNumber} from "../../utils";
import * as api from "./../../services/api-service";
import MissingDataEmptyState from "../../components/missing-data-empty-state.vue";

const parsePrinciples = (translator, principles) => {
  let result = "";
  principles.forEach((principle) => {
    const princripleName = translator(principle.nameKey);
    result = result.concat(`<span class="multiselect__tag" style="padding: 4px 6px 4px 6px !important;">${princripleName}</span>`)
  });
  return result;
}

export default {
  components: {
    "simple-table": SimpleTable,
    "loader": Loader,
    "detail-modal": DetailModal,
    "missing-data-empty-state": MissingDataEmptyState
  },
  created() {
    return api.getPublicActions().then((data) => {
      this.actions = data.actions;
      this.isLoading = false;
    });
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date", parser: (p) => formatToUIDate(p.date), sortEnabled: false},
        {key: "cooperative", value: "cooperative", parser: (p) => capitalizeFirstChar("TODO!"/*p.cooperative.name*/), sortEnabled: false},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50), sortEnabled: false},
        // {key: "description", value: "description", parser: (p) => formatText(p.description, 50)},
        {key: "principles", value: "principles", parser: (p) => parsePrinciples(this.$t, p.principles)}
      ],
      actions: [],
      isLoading: true,
      modalAction: {actionData:{}, principles: {}, sustainableDevelopmentGoals:{}},
    };
  },
  methods: {
    formatNumber(number){
      return parseNumber(number, this.$i18n.locale());
    },
    onQuickView(action) {
      api.getAction(action.id).then((actionData) => {
        actionData.partnersSelected = actionData.partnersInvolved.map((partner) => {
          return `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`
        });
        actionData.description = sanitizeMarkdown(actionData.description);
        this.modalAction = {actionData};
        $('#detailModal').modal()
      });
    }
  }
};
</script>

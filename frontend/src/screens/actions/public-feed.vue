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

    <div v-if="!isLoading && !actions.length">{{$t('emptyData')}}</div>
    <infinite-scroll
        :headers="headers"
        :elements="actions"
        :noMoreDataMsg="$t('noMoreData')"
        @onGetMore="onGetMore"
        @onViewDetail="onViewDetail">
    </infinite-scroll>
  </div>
</template>

<script>
import InfiniteScroll from "../../components/infinite-scroll.vue";
import DetailModal from "../../components/detail-modal.vue";
import Loader from "../../components/loader-overlay.vue";
import {sanitizeMarkdown, formatText, capitalizeFirstChar, formatToUIDate, parseNumber} from "../../utils";
import * as api from "./../../services/api-service";

const parsePrinciples = (translator, principles) => {
  let result = "";
  principles.forEach((principle) => {
    const princripleName = translator(principle.nameKey);
    result = result.concat(`<div><span class="multiselect__tag" style="padding: 4px 6px 4px 6px !important;">${princripleName}</span></div>`)
  });
  return result;
}

export default {
  components: {
    "infinite-scroll": InfiniteScroll,
    "loader": Loader,
    "detail-modal": DetailModal
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date", parser: (p) => formatToUIDate(p.date)},
        {key: "cooperative", value: "cooperative", parser: (p) => capitalizeFirstChar(p.cooperativeName)},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50)},
        {key: "description", value: "description", parser: (p) => formatText(p.description||"", 100)},
        {key: "principles", value: "principles", parser: (p) => parsePrinciples(this.$t, p.principles)}
      ],
      actions: [],
      isLoading: true,
      modalAction: {actionData:{}, principles: {}, sustainableDevelopmentGoals:{}},
    };
  },
  methods: {
    formatNumber(number) {
      return parseNumber(number, this.$i18n.locale());
    },
    onGetMore({more, done}) {
      const limit = 2;
      //this.isLoading = true;
      return api.getPublicActions(more, limit).then((data) => {
        this.isLoading = false;
        return done(data.actions);
      });
    },
    onViewDetail(action) {
      return api.getAction(action.id).then((actionData) => {
        actionData.partnersSelected = actionData.partnersInvolved.map((partner) => {
          return `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`
        });
        actionData.description = sanitizeMarkdown(actionData.description||"");
        this.modalAction = {actionData};
        $('#detailModal').modal()
      });
    }
  }
};
</script>

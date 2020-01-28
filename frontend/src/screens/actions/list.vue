<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t('actions')}}<i class="fas fa-fw fa-clipboard-list"></i></h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'action-edit', params: {actionId: 0}}">
        {{$t("addNew")}}   
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <spinner :loading='isLoading'/>
    <loader :loading='isLoading'/>
      <custom-table
        :headers="headers"
        :data="actions"
        :actions="{edit: true, delete: true, showViewButton: true}"
        :empty-state-msg="$t('emptyActionMsg')"
        @onEdit="onEdit"
        @onDelete="onDelete"
        @onQuickView="onQuickView">
      </custom-table>
    
  </div>
</template>

<script>
import {httpGet, httpDelete} from "../../api-client.js";
import CustomTable from "../../components/custom-table.vue";
import Loader from "../../components/loader-overlay.vue";
import Spinner from "../../components/spinner.vue";
import ActionQuickView from "../../components/action-quick-view.vue";
import {formatText} from "../../utils";
import swal from "sweetalert";
import * as api from "./../../services/api-service";

function parseBoolean(value) {
  const icon = value ? "check" : "times";
  return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
}

export default {
  components: {
    "custom-table": CustomTable,
    "loader": Loader,
    "spinner": Spinner
  },
  created() {
    httpGet("/actions")
      .then((response) => {
        this.actions = response.data;
        this.isLoading = false;
      });
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date"},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50)},
        {key: "description", value: "description", parser: (p) => formatText(p.description, 50)},
        //{key: "principle", value: "principle", parser: (p) => formatText(this.$t(p.principleNameKey), 50)},
        {key: "public", value: "public", parser: (p) => parseBoolean(p.public)},
      ],
      actions: [],
      isLoading: true
    };
  },
  methods: {
    onEdit(action) {
      this.$router.push({name: "action-edit", params: {actionId: action.id}});
    },
    onDelete(action) {
      swal({
        title: this.$t("areYouSure"),
        text: this.$t("onceActionDeleted"),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          httpDelete(`/actions/${action.id}`)
            .then(() => {
              swal( this.$t("deletedActionMsg"), {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              return httpGet("/actions")
                .then((response) => {
                  this.actions = response.data;
                });
            });
        }
      });
    },
    onQuickView(action) {
      Promise.all([
        api.getPrinciples(),
        api.getAction(action.id)
      ]).then(([principles, actionData]) => {
        console.log(principles, actionData);
      });


    }
  }
};
</script>
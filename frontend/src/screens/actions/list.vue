<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t('actions')}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'action-edit', params: {actionId: 0}}">
        {{$t("addNew")}}   
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <custom-table
      :headers="headers"
      :data="actions"
      :actions="{edit: true, delete: true}"
      :empty-state-msg="$t('emptyActionMsg')"
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
import {httpGet, httpDelete} from "../../api-client.js";
import CustomTable from "../../components/custom-table.vue";
import {formatText} from "../../utils";
import swal from "sweetalert";

export default {
  components: {
    "custom-table": CustomTable
  },
  created() {
    httpGet("/actions")
      .then((response) => {
        this.actions = response.data;
      });
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date"},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50)},
        {key: "description", value: "description", parser: (p) => formatText(p.description, 50)},
        {key: "principle", value: "principle", parser: (p) => formatText(p.principleName, 50)},
      ],
      actions: []
    };
  },
  methods: {
    onEdit(action) {
      this.$router.push({name: "action-edit", params: {actionId: action.id}});
    },
    onDelete(action) {
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
  }
};
</script>

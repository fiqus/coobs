<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("partners")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'partner-edit', params: {partnerId: 0}}">
        Add new
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <custom-table
      :headers="headers"
      :data="partners"
      :actions="{edit: true, delete: true}"
      empty-state-msg="You don't have any partners yet!"
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
import CustomTable from "../../components/custom-table.vue";
import {formatText} from "../../utils";
import {httpGet, httpDelete} from "../../api-client.js";
import swal from "sweetalert";
import {getUser} from "./../../services/user-service";

function parseBoolean(value) {
  return `<i class="fas fa-dollar-sign fa-1x"></i> ${value}`;
}

export default {
  components: {
    "custom-table": CustomTable
  },
  created() {
    const cooperativeId = getUser().cooperative;
    httpGet(`/cooperatives/${cooperativeId}/partners`)
      .then((response) => {
        this.partners = response.data;
      });
  },
  data() {
    return {
      headers: [
        {key: "name", value: "Name", parser: (p) => formatText(p.name)},
        {key: "date_from", value: "From", parser: (p) => formatText(p.date_from, 50)},
        {key: "date_to", value: "To", parser: (p) => formatText(p.date_to, 50)},
        {key: "actions_budget", value: "Budget", parser: (p) => parseBoolean(p.actions_budget)},
      ],
      partners: []
    };
  },
  methods: {
    onEdit(partner) {
      this.$router.push({name: "partner-edit", params: {partnerId: partner.id}});
    },
    onDelete(partner) {
      httpDelete(`/partners/${partner.id}`)
        .then(() => {
          swal("The partner has been deleted!", {
            icon: "success",
            buttons: false,
            timer: 2000
          });
          return httpGet("/partners")
            .then((response) => {
              this.partners = response.data;
            });
        });
    }
  }
};
</script>


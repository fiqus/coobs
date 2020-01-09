<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("partners")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'partner-edit', params: {partnerId: 0}}">
        {{$t("addNew")}}
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
import {capitalizeFirstChar} from "./../../utils";

export default {
  components: {
    "custom-table": CustomTable
  },
  created() {
    const {cooperativeId} = this.$store.state.user;
    httpGet(`/partners`)
      .then((response) => {
        const loggedUserEmail = this.$store.state.user.email;
        response.data.map(partner => {
          partner.noActions = partner.email === loggedUserEmail;
          return partner;
        });
        this.partners = response.data;
      });
  },
  data() {
    return {
      headers: [
        {key: "firstName", value: "firstName", parser: (p) => capitalizeFirstChar(formatText(p.firstName))},
        {key: "lastName", value: "lastName", parser: (p) => capitalizeFirstChar(formatText(p.lastName))}
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


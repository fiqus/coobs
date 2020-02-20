<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("partners")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'partner-edit', params: {partnerId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <loader :loading='isLoading'/>
    <custom-table
      :headers="headers"
      :data="listPartners"
      :actions="{edit: true, delete: true, showViewButton: false}"
      :sortEnabled=true
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
import CustomTable from "../../components/simple-table.vue";
import {formatText} from "../../utils";
import {httpGet, httpDelete} from "../../api-client.js";
import swal from "sweetalert";
import {capitalizeFirstChar} from "./../../utils";
import Loader from "../../components/loader-overlay.vue";

export default {
  components: {
    "custom-table": CustomTable,
    "loader": Loader
  },
  created() {
    const {cooperativeId} = this.$store.state.user;
    httpGet(`/partners`)
      .then((response) => {
        this.partners = response.data;
        this.isLoading = false;
      });
  },
  computed: {
    listPartners() {
      const loggedUserEmail = this.$store.state.user.email;
      return this.partners.map(partner => {
        partner.noActions = partner.email === loggedUserEmail;
        return partner;
      });
    }
  },
  data() {
    return {
      headers: [
        {key: "firstName", value: "firstName", parser: (p) => capitalizeFirstChar(formatText(p.firstName))},
        {key: "lastName", value: "lastName", parser: (p) => capitalizeFirstChar(formatText(p.lastName))}
      ],
      partners: [],
      isLoading: true
    };
  },
  methods: {
    onEdit(partner) {
      this.$router.push({name: "partner-edit", params: {partnerId: partner.id}});
    },
    onDelete(partner) {
      swal({
        title: this.$t('areYouSure'),
        text: this.$t('oncePartnerDeleted'),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          return httpDelete(`/partners/${partner.id}`)
            .then(() => {
              swal(this.$t('partnerDeleted'), {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              return httpGet("/partners")
                .then((response) => {
                  this.partners = response.data;
                });
            })
            .catch((err) => {
              swal(err.response.data.detail, {
                icon: "error"
              });
            });
        }
      });
    }
  }
};
</script>


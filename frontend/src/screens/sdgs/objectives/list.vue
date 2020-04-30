<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("sdg_objectives")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'sdg-objectives-edit', params: {sdgObjectiveId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <loader :loading='isLoading'/>
    <simple-table
      :headers="headers"
      :data="sdgObjectives"
      :actions="{edit: true, delete: true, showViewButton: false}"
      :empty-state-msg="$t('noSDGObjectivesMessage')" 
      :sortEnabled=true
      @onEdit="onEdit"
      @onDelete="onDelete">
    </simple-table>
  </div>
</template>

<script>
import SimpleTable from "../../../components/simple-table.vue";
import {formatText} from "../../../utils";
import {httpGet, httpDelete} from "../../../api-client.js";
import swal from "sweetalert";
import Loader from "../../../components/loader-overlay.vue";


export default {
  components: {
    "simple-table": SimpleTable,
    "loader": Loader
  },
  created() {
    httpGet("/sdg-objectives")
      .then((response) => {
        this.sdgObjectives = response.data;
        this.isLoading = false;
      });
  },
  data() {
    return {
      headers: [
        {key: "period_name", value: "period", parser: (sdgObj) => formatText(sdgObj.periodName)},
        {key: "sdg_name", value: "sustainable_development_goal", parser: (sdgObj) => formatText(sdgObj.sdgName)}, 
        //TODO agregar traduccion para sdg
      ],
      sdgObjectives: [],
      isLoading: true
    };
  },
  methods: {
    onEdit(sdgObj) {
      this.$router.push({name: "sdg-objectives-edit", params: {sdgObjectiveId: sdgObj.id}});
    },
    onDelete(sdgObj) {
      swal({
        title: this.$t('areYouSure'),
        text: this.$t('onceSDGObjectiveDeleted'),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          httpDelete(`/sdg-objectives/${sdgObj.id}`)
            .then(() => {
              swal(this.$t("deletedSDGObjectiveMsg"), {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              return httpGet("/sdg-objectives")
                .then((response) => {
                  this.sdgObjectives = response.data;
                });
            });
        }
      });
    }
  }
};
</script>


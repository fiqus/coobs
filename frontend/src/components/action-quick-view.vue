<template>
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLongTitle">{{$t('actionDetail')}}</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <label class="bold">{{$t('name')}}:</label>
        <span name="name"
          type="text">{{modalAction.actionData.name}}
        </span><br/>
        <label class="bold">{{$t('description')}}:</label>
        <span name="description"
          type="text">
          {{modalAction.actionData.description}}
        </span><br/>
        <label class="bold">{{$t('principles')}}:</label><br/>
        <span class="multiselect__tag" v-for="principle in modalAction.principles" v-bind:key="principle" 
          name="principles" type="text">
          {{$t(principle.nameKey)}}
        </span><br/>
        <label class="bold">{{$t('partners')}}:</label><br/>
        <span class="multiselect__tag" v-for="partner in modalAction.actionData.partnersSelected" v-bind:key="partner" 
          name="partners" type="text">
          {{partner}}
        </span><br/>
        <label class="bold">{{$t('startingDate')}}:</label>
        <span name="startingDate"
          type="text">{{modalAction.actionData.date}}
        </span><br/>
        <label class="bold">{{$t('investedHours')}}:</label>
        <span name="investedHours"
          type="text">{{modalAction.actionData.investedHours}}
        </span><br/>
        <label class="bold">{{$t('investedMoney')}}:</label>
        <span name="investedMoney"
          type="text">$ {{modalAction.actionData.investedMoney}}
        </span><br/>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">{{$t('close')}}</button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    modalAction: {
      type: Object,
    }
  },
};
</script>


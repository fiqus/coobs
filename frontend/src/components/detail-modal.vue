<template>
      <div class="modal fade" id="actionDetailModal" tabindex="-1" role="dialog" aria-labelledby="actionDetailModalTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{title}}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <slot name="modal-body"/>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">{{$t('close')}}</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String
    }
  }
};
</script>
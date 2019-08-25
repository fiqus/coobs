<template>
  <div class="row justify-content-center">
    <div class="col-xl-4 col-lg-3 col-md-3">
      <div class="card o-hidden border-0 shadow-lg my-5">
        <div class="card-body p-5">
          <!-- In this slot will be the screen content of this layout -->
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

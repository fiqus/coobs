<template>
  <div class="bg-gray-100 login-screen">
    <div class="container login-card">
      <slot name="page-content"></slot>
    </div>

    <!-- Copyright Section -->
    <section class="copyright py-4 text-center text-gray-600">
      <div class="container">
        <small>{{$t("createdByFiqus")}} | COOBS 2019</small>
      </div>
    </section>
  </div>
</template>

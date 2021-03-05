<template>
  <div class="row justify-content-center help-content-container">
    <!-- @TODO Change the iframe to an ajax request! -->
    <iframe src="/help/" scrolling="no" onload="this.style.height = this.contentWindow.document.documentElement.scrollHeight + 'px';" style="border: none;width: 90%;"></iframe>
  </div>
</template>
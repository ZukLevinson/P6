<template>
  <div navbar no-flex flex row>
    <div id="logo" lg-3 flex row>
      <h1>Word Complete</h1>
    </div>
    <div id="information"></div>
    <div id="links" lg-3 flex row>
      <router-link to="/"><h3>Home</h3></router-link>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({})
export default class Navbar extends Vue {}
</script>
<style lang="scss" scoped>
a {
  text-decoration: none;
  display: flex;
  color: black;
}
.router-link-exact-active {
  color: gray;
  text-decoration: underline;
}
</style>
<template>
  <div class="home" flex col>
    <div id="header" lg-3 flex row>
      <p ml-2> Type your words... </p>
    </div>
    <div id="text-box"></div>
    <div id="stats" lg-3></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({})
export default class Home extends Vue {}
</script>

<style lang="scss" scoped>
p {
  font-family: "Roboto", sans-serif;
  font-size: 4em;
  color:#3C3E3F;
  display: table-cell;
}
</style>
<template>
  <div flex col id="app">
    <navbar />
    <router-view />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Navbar from "@/components/Navbar.vue";

@Component({
  components: {
    Navbar,
  },
})
export default class App extends Vue {}
</script>

<style lang="scss">
html,
body {
  margin: 0;
}

[navbar] {
  min-height: 5vh;
  top: 0;
  box-shadow: 0px 0 7px rgb(206, 206, 206);
}

[flex] {
  display: flex;

  &[row] {
    flex-direction: row;
  }
  &[col] {
    flex-direction: column;
  }

  & > * {
    flex: 12 12 auto;
  }
}

[fill-width] {
  width: 100%;
}

[fill-height] {
  height: 100%;
}

[no-flex] {
  flex: 0 !important;
}

#app {
  position: relative;
  width: 100vw;
  height: 100vh;
  background-color: #f4f4f4;
  font-family: "Noto Sans JP", sans-serif;
}

[lg-3] {
  width: 25%;
  flex: 3;
}

h1 {
  font-size: 1.5em;
  margin: auto;
  text-align: center;
}

h3 {
  font-size: 1em;
  margin: auto;
  text-align: center;
}

@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@100;300;400;500;700;900&family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap");
</style>

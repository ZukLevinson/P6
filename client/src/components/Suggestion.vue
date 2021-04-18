<template>
  <div id="container" flex row>
    <h1 :style="style">
      {{ text }}
    </h1>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";

@Component({})
export default class Suggestion extends Vue {
  @Prop({ required: true }) readonly text!: string;
  @Prop({ default: false }) readonly big!: boolean;

  private style: Record<string, string> = {
    color: "gray",
    "font-size": "1.3em",
  };

  mounted(): void {
    if (this.big) {
      this.style = {
        color: "black",
        "font-size": "1.7em",
      };
    }
  }
}
</script>
<style lang="scss" scoped>
#container {
  user-select: none;

  &,
  & > * {
    transition: all 0.1s ease-out;
  }

  &:hover {
    font-size: 120%;
    cursor: pointer;
  }
}
</style>
<template>
  <div class="home" flex col>
    <div v-if="is_active" id="suggestions" lg-3 flex row>
      <suggestion text="hi1" />
      <suggestion text="hi2" :big="true" />
      <suggestion text="hi3" />
    </div>
    <div v-else id="heading" lg-3 flex col>
      <div flex row>
        <h1 style="margin-top:auto">Word Prediction</h1>
      </div>
      <div lg-5>
        <h3>You must write at least one word</h3>
      </div>
    </div>
    <div id="text-zone" flex row>
      <textarea v-model="input_text" id="text-box" placeholder="Type...">
      </textarea>
    </div>
    <div id="stats" lg-3></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Suggestion from "@/components/Suggestion.vue";

@Component({
  components: {
    Suggestion,
  },
})
export default class Home extends Vue {
  private input_text = "";

  get is_active(){
    console.log(this.input_text.split(" ").length)
    return this.input_text.split(" ").length > 1;
  }

  mounted(): void {
    document.addEventListener("keydown", (): void => {
      const box: HTMLElement | null = document.getElementById("text-box");

      if (box != null) {
        box.focus();
      }
    });
  }
}
</script>

<style lang="scss" scoped>
p {
  font-family: "Roboto", sans-serif;
  font-size: 4em;
  color: #3c3e3f;
  display: table-cell;
}

textarea {
  background: rgba(0, 0, 0, 0);
  border: none;
  flex: 1;
  resize: none;

  &:focus {
    outline: none !important;
  }
}
</style>
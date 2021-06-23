<template>
  <wall json-file="circle-members" :ordered-group-names="orderedGroupNames">
    <template v-slot:heading
      ><figure class="wall__logo grid_separator--l">
        <img src="./img/circle-logo.png" alt="Circle Membership logo" /></figure
    ></template>
    <template v-slot:member="{ member }">
      <span class="wall__name">{{ member }}</span>
    </template>
  </wall>
</template>

<script>
import Wall from '../../Wall.vue';

export default {
  name: 'CircleWall',

  components: { Wall },

  data() {
    return {
      orderedGroupNames: [
        "Chairman's Circle",
        'Leadership Circle',
        "Editor's Circle",
      ],
    };
  },
};
</script>

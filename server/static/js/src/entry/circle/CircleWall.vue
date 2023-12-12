<template>
  <wall json-file="circle-members" :ordered-group-names="orderedGroupNames">
    <template #heading>
      <h2 class="is-sr-only">Our Circle Members</h2>
      <figure class="wall__logo grid_separator--l" aria-hidden="true">
        <img src="./img/circle-logo.png" alt="Circle Membership logo" /></figure
    ></template>
    <template #subheading="{ group }">
      <template v-if="group.name === foundersLabel"
        ><p class="grid_separator--s">
          <em
            >In honor of our three founders: Ross Ramsey, Evan Smith and John
            Thornton</em
          >
        </p></template
      >
    </template>
    <template #member="{ member }">
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
        "Founders' Circle",
        "CEO's Circle",
        "Chairman's Circle",
        'Leadership Circle',
        "Editor's Circle",
      ],
      foundersLabel: "Founders' Circle",
    };
  },
};
</script>

<template>
  <wall json-file="council-members" :ordered-group-names="orderedGroupNames">
    <template #heading>
      <h2 class="is-sr-only">IRC Members</h2>
      <figure class="wall__logo grid_separator--l" aria-hidden="true">
        <img src="./img/council-logo.png" alt="Circle Membership logo" />
      </figure>
      [Placeholder image - to be replaced]
    </template>
    <template #member="{ member }">
      <span class="wall__name">{{ member }}</span>
    </template>
  </wall>
</template>

<script>
import Wall from '../../Wall.vue';

export default {
  name: 'CouncilWall',

  components: { Wall },

  data() {
    return {
      orderedGroupNames: [''],
    };
  },
};
</script>

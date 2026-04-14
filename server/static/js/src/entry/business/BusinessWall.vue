<template>
  <wall
    json-file="austin-business-member-roster"
    :ordered-group-names="orderedGroupNames"
  >
    <template #heading>
      <div class="border--yellow_notch"></div>
      <h2 class="grid_separator">We’re honored to have the support of the following Austin Current business members</h2>
    </template>
    <template #member="{ member }">
      <span class="wall__name"
        ><a :href="member.url">{{ member.business_name }}</a></span
      >
    </template>
  </wall>
</template>

<script>
import Wall from '../../Wall.vue';

export default {
  name: 'BusinessWall',

  components: { Wall },

  data() {
    return {
      orderedGroupNames: ['Maximum Impact', 'Events & Newsletter', 'Members & Webpage'],
    };
  },
};
</script>

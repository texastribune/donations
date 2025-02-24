<template>
  <wall
    json-file="business-member-roster"
    :ordered-group-names="orderedGroupNames"
  >
    <template #heading>
      <div class="border--yellow_notch"></div>
      <h2 class="grid_separator">Our Business Members</h2>
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
      orderedGroupNames: ['Big Tex', 'Lone Star', "Hat's Off"],
    };
  },
};
</script>

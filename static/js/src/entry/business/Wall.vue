<template>
  <div
    v-if="!loading && !error"
  >
    <div
      v-for="(group, index) in data"
      :key="group.id"
      :class="{ 'grid_separator--l': index !== data.length - 1 }"
      class="business-wall__group"
    >
      <h2
        class="business-wall__heading grid_separator--s"
      >
        {{ group.heading }}
      </h2>
      <ul class="business-wall__list">
        <li
          v-for="(member, index) in group.members"
          :key="index"
          class="business-wall__item"
        >
          <span class="business-wall__star fa fa-star" />
          <span class="business-wall__name">
            {{ member }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {
  DONATION_LEVELS,
  POSITION_IN_PAGE_A,
  POSITION_IN_PAGE_B,
  POSITION_IN_PAGE_C
} from './constants';

export default {
  name: 'Wall',

  data() {
    return {
      loading: true,
      error: false,
      data: [
        { id: 0, heading: DONATION_LEVELS[POSITION_IN_PAGE_A].header, members: [] },
        { id: 1, heading: DONATION_LEVELS[POSITION_IN_PAGE_B].header, members: [] },
        { id: 2, heading: DONATION_LEVELS[POSITION_IN_PAGE_C].header, members: [] },
      ],
    };
  },

  mounted() {
    this.getCircleMembers();
  },

  methods: {
    getCircleMembers() {
      const url = 'https://membership.texastribune.org/circle-members.json';

      axios.get(url)
        .then(({
          data: {
            'Chairman\'s Circle': chairman,
            'Editor\'s Circle': editor,
            'Leadership Circle': leadership,
          },
        }) => {
          this.data[0].members = chairman;
          this.data[1].members = leadership;
          this.data[2].members = editor;
          this.loading = false;
        })
        .catch(() => {
          this.error = true;
          this.loading = false;
        });
    },
  },
};
</script>

<template>
  <div v-if="!loading && !error">
    <div
      v-for="(group, index) in data"
      :key="group.id"
      :class="{ 'grid_separator--l': index !== data.length - 1 }"
      class="circle-wall__group"
    >
      <h2 class="circle-wall__heading grid_separator--s">
        {{ group.heading }}
      </h2>
      <ul class="circle-wall__list">
        <li
          v-for="(member, memberIndex) in group.members"
          :key="memberIndex"
          class="circle-wall__item"
        >
          <span class="circle-wall__star fa fa-star" />
          <span class="circle-wall__name"> {{ member }} </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Wall',

  data() {
    return {
      loading: true,
      error: false,
      data: [
        { id: 0, heading: "Chairman's Circle", members: [] },
        { id: 1, heading: 'Leadership Circle', members: [] },
        { id: 2, heading: "Editor's Circle", members: [] },
      ],
    };
  },

  mounted() {
    this.getCircleMembers();
  },

  methods: {
    getCircleMembers() {
      const url = 'https://membership.texastribune.org/circle-members.json';

      axios
        .get(url)
        .then(
          ({
            data: {
              "Chairman's Circle": chairman,
              "Editor's Circle": editor,
              'Leadership Circle': leadership,
            },
          }) => {
            this.data[0].members = chairman;
            this.data[1].members = leadership;
            this.data[2].members = editor;
            this.loading = false;
          }
        )
        .catch(() => {
          this.error = true;
          this.loading = false;
        });
    },
  },
};
</script>

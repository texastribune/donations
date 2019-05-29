<template>
  <section class="wall grid_separator--l">
    <figure class="wall__logo grid_separator--l">
      <img src="../../../../img/circle-logo.png" alt="Circle Membership logo" />
    </figure>
    <div v-if="!loading && !error">
      <div
        v-for="(group, index) in data"
        :key="group.id"
        :class="{ 'grid_separator--l': index !== data.length - 1 }"
        class="wall__group"
      >
        <h2 class="wall__heading grid_separator--s">{{ group.heading }}</h2>
        <ul class="wall__list">
          <li
            v-for="(member, memberIndex) in group.members"
            :key="memberIndex"
            class="wall__item"
          >
            <span class="wall__star c-icon c-icon--yellow c-icon--baseline"
              ><svg aria-hidden="true"><use xlink:href="#star"></use></svg
            ></span>
            <span class="wall__name">{{ member }}</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
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

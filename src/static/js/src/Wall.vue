<template>
  <section class="wall">
    <div v-if="!loading && !error">
      <slot name="heading"></slot>
      <section
        v-for="(group, groupIndex) in memberGroups"
        :key="group.name"
        :class="{ 'grid_separator--l': groupIndex !== memberGroups.length - 1 }"
        class="wall__group"
      >
        <template v-if="group.members">
          <h3 class="wall__heading grid_separator--s">{{ group.name }}</h3>
          <slot name="subheading" :group="group"></slot>
          <ul class="wall__list">
            <li
              v-for="(member, memberIndex) in group.members"
              :key="memberIndex"
              class="wall__item"
            >
              <span class="wall__star c-icon c-icon--yellow c-icon--baseline"
                ><svg aria-hidden="true"><use xlink:href="#star"></use></svg
              ></span>
              <slot name="member" :member="member"></slot>
            </li>
          </ul>
        </template>
      </section>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

function formatMemberGroups(rawGroups, orderedGroupNames) {
  const formattedGroups = [];

  orderedGroupNames.forEach((groupName, index) => {
    formattedGroups[index] = {
      name: groupName,
      members: rawGroups[groupName],
    };
  });

  return formattedGroups;
}

export default {
  name: 'Wall',

  props: {
    jsonFile: {
      type: String,
      required: true,
    },

    orderedGroupNames: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      loading: true,
      error: false,
      memberGroups: {},
    };
  },

  mounted() {
    this.getMembers();
  },

  methods: {
    getMembers() {
      const url = `https://membership.texastribune.org/${this.jsonFile}.json`;

      axios
        .get(url)
        .then(({ data: rawGroups }) => {
          this.memberGroups = formatMemberGroups(
            rawGroups,
            this.orderedGroupNames
          );
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

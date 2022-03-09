<template>
  <summary-box heading="profile settings">
    <template #content>
      <info-list :items="data">
        <template #text="{ item: { key, text } }">
          <template v-if="key === 'email'">
            <span class="t-wrap-break">{{ text }}</span>
          </template>
          <template v-else>
            {{ text }}
          </template>
        </template>
      </info-list>
    </template>

    <template #links>
      <user-internal-nav
        show-edit-profile
        show-reset-pw
        :pw-reset-ga-label="ga.userPortal.labels.home"
      />
    </template>
  </summary-box>
</template>

<script>
import SummaryBox from '../../../components/SummaryBox.vue';
import InfoList from '../../../components/InfoList.vue';

export default {
  name: 'SummaryProfileSettings',

  components: { SummaryBox, InfoList },

  props: {
    email: {
      type: String,
      required: true,
    },

    firstName: {
      type: String,
      required: true,
    },

    lastName: {
      type: String,
      required: true,
    },

    zip: {
      type: String,
      required: true,
    },
  },

  computed: {
    data() {
      const data = [];
      const { firstName, lastName, email, zip } = this;

      if (firstName && lastName) {
        data.push({
          key: 'name',
          heading: 'Name',
          text: `${firstName} ${lastName}`,
        });
      }

      data.push({
        key: 'email',
        heading: 'Login email',
        text: email,
      });

      if (zip) {
        data.push({
          key: 'zip',
          heading: 'ZIP code',
          text: zip,
        });
      }

      return data;
    },
  },
};
</script>

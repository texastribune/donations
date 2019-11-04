<template>
  <ul class="c-link-list t-links-underlined">
    <li v-if="!isNeverGiven" class="has-m-btm-marg">
      <span class="c-link-list__arrow has-text-teal">
        <strong>&rarr;</strong>
      </span>
      <span class="has-text-gray-dark">
        <router-link :to="{ name: 'payments' }">
          See your donation history
        </router-link>
      </span>
    </li>
    <li v-if="isRecurringDonor || isSingleDonor || isCircleDonor">
      <span class="c-link-list__arrow has-text-teal">
        <strong>&rarr;</strong>
      </span>
      <span class="has-text-gray-dark">
        <router-link :to="{ name: 'membership' }">
          See your membership status
        </router-link>
      </span>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'AmbassadorLinks',

  props: {
    isRecurringDonor: {
      type: Boolean,
      required: true,
    },

    isSingleDonor: {
      type: Boolean,
      required: true,
    },

    isCircleDonor: {
      type: Boolean,
      required: true,
    },

    isNeverGiven: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<template>
  <summary-box heading="become a member" :display="{ hasMobileBottom: false }">
    <template #content>
      <p class="has-text-gray-dark">
        Our nonprofit newsroom relies on the support of readers like you to keep
        our stories free and accessible for all. Are you ready to join our
        member community?
      </p>
    </template>

    <template #links>
      <user-internal-nav show-join-now />
    </template>

    <template #bottom>
      <link-email :ga-label="ga.userPortal.labels.home">
        <template #heading>
          <h2 class="t-size-s">Already a member?</h2>
        </template>
      </link-email>
    </template>
  </summary-box>
</template>

<script>
import LinkEmail from '../../../link-email/components/MiniForm.vue';
import SummaryBox from '../../../components/SummaryBox.vue';

export default {
  name: 'SummaryNeverGiven',

  components: { SummaryBox, LinkEmail },
};
</script>

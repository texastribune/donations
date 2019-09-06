<template>
  <form :key="formKey" @submit.prevent="onSubmit">
    <p v-if="badEmail" role="alert" class="has-b-btm-marg has-text-error">
      <strong
        >Error: You can't change your login email to {{ badEmail }} because an
        account already exists with that email address.</strong
      >
    </p>
    <p v-if="showSuccess" role="alert" class="has-b-btm-marg has-text-success">
      <strong>Success! Your profile has been updated.</strong>
    </p>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.firstName.rules"
      :name="currentFields.firstName.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <text-input
          v-model="currentFields.firstName.value"
          :error-messages="errors"
          :flags="flags"
          :name="currentFields.firstName.name"
          :label="currentFields.firstName.label"
          @updateFlags="updateFlags"
        />
      </div>
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.lastName.rules"
      :name="currentFields.lastName.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <text-input
          v-model="currentFields.lastName.value"
          :error-messages="errors"
          :flags="flags"
          :name="currentFields.lastName.name"
          :label="currentFields.lastName.label"
          @updateFlags="updateFlags"
        />
      </div>
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.email.rules"
      :name="currentFields.email.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <text-input
          v-model="currentFields.email.value"
          :error-messages="errors"
          :flags="flags"
          :name="currentFields.email.name"
          :label="currentFields.email.label"
          @updateFlags="updateFlags"
        >
          <template v-slot:extra>
            <p v-show="showConfirmedEmail" class="t-size-xs has-text-error">
              <strong>Are you sure?</strong> Changing this email will
              immediately log you out of texastribune.org, and you won't be able
              to log back in with
              <strong>{{ initialFields.email.value }}</strong
              >.
            </p>
          </template>
        </text-input>
      </div>
    </validation-provider>
    <validation-provider
      v-show="showConfirmedEmail"
      v-slot="{ errors, flags }"
      :rules="confirmedEmailRules"
      :name="currentFields.confirmedEmail.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <text-input
          v-model="currentFields.confirmedEmail.value"
          :error-messages="errors"
          :flags="flags"
          :name="currentFields.confirmedEmail.name"
          :label="currentFields.confirmedEmail.label"
          prevent-paste
          @updateFlags="updateFlags"
        />
      </div>
    </validation-provider>
    <validation-provider
      v-slot="{ errors, flags }"
      :rules="currentFields.zip.rules"
      :name="currentFields.zip.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <text-input
          v-model="currentFields.zip.value"
          :error-messages="errors"
          :flags="flags"
          :name="currentFields.zip.name"
          :label="currentFields.zip.label"
          @updateFlags="updateFlags"
        />
      </div>
    </validation-provider>
    <validation-provider
      v-slot="{ flags }"
      :rules="currentFields.marketing.rules"
      :name="currentFields.marketing.name"
      immediate
      slim
    >
      <div class="has-b-btm-marg">
        <checkbox
          v-model="currentFields.marketing.value"
          :flags="flags"
          :name="currentFields.marketing.name"
          :label="currentFields.marketing.label"
          @updateFlags="updateFlags"
        />
      </div>
    </validation-provider>
    <submit :disabled="!formIsValid || !formHasChanged" value="Save" />
  </form>
</template>

<script>
import formMixin from '../../../form/mixins';

export default {
  name: 'EditContactInfoForm',

  mixins: [formMixin],

  props: {
    badEmail: {
      type: String,
      required: true,
    },

    showSuccess: {
      type: Boolean,
      required: true,
    },
  },

  computed: {
    emailHasChangedAndIsValid() {
      const { changed, valid } = this.currentFields.email;
      return changed && valid;
    },

    showConfirmedEmail: {
      get() {
        const { isVisible } = this.currentFields.confirmedEmail;
        return isVisible;
      },

      set(isVisible) {
        this.currentFields.confirmedEmail.isVisible = isVisible;
      },
    },

    confirmedEmailRules() {
      return { required: true, is: this.currentFields.email.value };
    },
  },

  watch: {
    emailHasChangedAndIsValid(newHasChangedAndIsValid) {
      if (newHasChangedAndIsValid) {
        this.showConfirmedEmail = true;
      } else {
        this.showConfirmedEmail = false;
        this.resetValue('confirmedEmail');
      }
    },
  },

  methods: {
    onSubmit() {
      this.$emit('onSubmit', this.currentFields);
      this.logToGtm();
    },

    logToGtm() {
      const allEvents = [];
      const baseEvent = {
        event: this.ga.customEventName,
        gaCategory: this.ga.userPortal.category,
        gaLabel: this.ga.userPortal.labels['edit-contact-info'],
      };

      if (this.currentFields.email.changed) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-email'],
        });
      }
      if (
        this.currentFields.firstName.changed ||
        this.currentFields.lastName.changed
      ) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-name'],
        });
      }
      if (this.currentFields.zip.changed) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['edit-zip'],
        });
      }

      const { changed, value } = this.currentFields.marketing;

      if (changed && value) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['marketing-opt-in'],
        });
      }
      if (changed && !value) {
        allEvents.push({
          ...baseEvent,
          gaAction: this.ga.userPortal.actions['marketing-opt-out'],
        });
      }

      allEvents.forEach(event => {
        window.dataLayer.push(event);
      });
    },
  },
};
</script>

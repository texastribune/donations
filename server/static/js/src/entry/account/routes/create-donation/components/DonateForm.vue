<template>
  <validation-observer v-slot="{ handleSubmit }">
    <form :key="formKey" @submit.prevent="handleSubmit(onSubmit)">
      <p
        v-if="showSuccess"
        role="alert"
        class="has-b-btm-marg has-text-success"
      >
        <strong>Success! Please direct the donor to the card reader for payment processing.</strong>
      </p>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required"
        name="firstName"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.firstName.value"
            label="First name"
            name="firstName"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required"
        name="lastName"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.lastName.value"
            label="Last name"
            name="lastName"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required|email"
        name="email"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.email.value"
            label="Email"
            name="email"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        name="installmentPeriod"
        slim>
        <div class="has-b-btm-marg">
          <radios
            v-model="currentFields.installmentPeriod.value"
            label="Frequency"
            name="installmentPeriod"
            :classes="'form__radios form__radios--stack-at-medium'"
            :options="frequencyOptions"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        rules="required|numeric"
        name="amount"
        slim
      >
        <div class="has-b-btm-marg">
          <text-input
            v-model="currentFields.amount.value"
            label="Amount"
            name="amount"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>
      <validation-provider
        v-slot="{ errors, pristine, changed, valid }"
        name="payFees"
        slim
      >
        <div class="has-b-btm-marg">
          <checkbox
            v-model="currentFields.payFees.value"
            :label="`I agree to pay ${feeAmount} ${currentFields.installmentPeriod.value} for processing fees. This directs more money to our mission.`"
            name="payFees"
            :error-messages="errors"
            :pristine="pristine"
            :changed="changed"
            :valid="valid"
            @updateFlags="updateFlags"
          />
        </div>
      </validation-provider>

      <submit value="Create Donation" />
    </form>
  </validation-observer>
</template>

<script>
import { localize } from 'vee-validate';

import formMixin from '../../../form/mixins/form';
import { isValidDonationAmount } from '../../../../../utils/validators';

localize({
  en: {
    fields: {
      email: {
        required: 'You must have an email to log into texastribune.org.',
        email: 'Please enter a valid email address.',
      },

      firstName: {
        required:
          'Please provide your first and last name. They appear with comments on texastribune.org to promote a more transparent and personable atmosphere.',
      },

      lastName: {
        required:
          'Please provide your first and last name. They appear with comments on texastribune.org to promote a more transparent and personable atmosphere.',
      },

      amount: {
        required:
          'Please enter a donation amount.',
        numeric: 'The donation amount must contain only numbers.',
      },
    },
  },
});

export default {
  name: 'DonateForm',

  mixins: [formMixin],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'One-time donation', value: 'once', recurring: false },
        { id: 1, text: 'Monthly donation', value: 'monthly', recurring: true },
        { id: 2, text: 'Yearly donation', value: 'yearly', recurring: true },
      ],
    }
  },

  computed: {
    feeAmount() {
      if ("amount" in this.currentFields) {
        let amount = this.currentFields.amount.value;
        const { installmentPeriod: { recurring } } = this.currentFields;

        if (!isValidDonationAmount(amount)) {
          return "";
        }

        if (amount.charAt(0) === '$') {
          amount = amount.substring(1);
        }

        amount = parseFloat(amount.trim());

        // https://support.stripe.com/questions/passing-the-stripe-fee-on-to-customers
        const feeRate = recurring ? 0.027 : 0.022
        const total = (amount + 0.3) / (1 - feeRate);
        // Fee rounded to two decimal places.
        const fee = Math.round((total - amount) * 100) / 100;

        return `$${fee.toFixed(2)}`;
      }
      return "";
    }
  },

  props: {
    showSuccess: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

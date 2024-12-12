<template>
  <form
    ref="form"
    action="/blast"
    method="post"
    class="form blast-form"
    @submit="$event.preventDefault()"
  >
    <div v-show="serverErrorMessage" class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col">
          <p class="form__error form__error--prominent">
            {{ serverErrorMessage }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col blast-buckets">
          <form-buckets :all-levels="allLevels" :store-module="storeModule" />
        </div>
      </div>
    </div>

    <div class="grid_container--m">
      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="email address"
            type="email"
            base-classes="form__text form__text--standard"
            name="stripeEmail"
            inputmode="email"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="first name"
            base-classes="form__text form__text--standard"
            name="first_name"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :store-module="storeModule"
            :show-error="showErrors"
            label-text="last name"
            base-classes="form__text form__text--standard"
            name="last_name"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <pay-fees :store-module="storeModule" base-classes="form__fees" />
        </div>
      </div>

      <div class="grid_row">
        <div class="col">
          <native-pay
            :store-module="storeModule"
            :form-is-valid="isValid"
            :supported="nativeIsSupported"
            base-classes="form__native"
            @setLocalValue="setLocalValue"
            @setCardValue="setCardValue"
            @onSubmit="onSubmit"
          />
        </div>
      </div>

      <div
        v-if="nativeIsSupported && showManualPay"
        class="grid_separator--l"
        aria-hidden="true"
      />

      <div
        :aria-live="nativeIsSupported ? 'polite' : false"
        class="grid_separator"
      >
        <div v-if="showManualPay">
          <div class="grid_row">
            <div class="col">
              <manual-pay
                :card="card"
                base-classes="form__manual"
                @setCardValue="setCardValue"
              />
            </div>
          </div>

          <div class="grid_row">
            <div class="col">
              <manual-submit
                :form-is-valid="isValid && card.isValid"
                :is-fetching-token="isFetchingToken"
                base-classes="form__submit button button--yellow button--l"
                value="Activate"
                @setLocalValue="setLocalValue"
                @setCardValue="setCardValue"
                @onSubmit="onSubmit"
              />
            </div>
          </div>
        </div>
      </div>

      <div v-if="genericErrorMessage" class="grid_separator">
        <div class="grid_row">
          <div class="col">
            <p
              role="alert"
              class="form__error form__error--normal form__error--centered"
            >
              {{ genericErrorMessage }}
            </p>
          </div>
        </div>
      </div>

      <p class="subtext">
        This site is protected by reCAPTCHA and the Google
        <a href="https://policies.google.com/privacy">Privacy Policy</a> and
        <a href="https://policies.google.com/terms">Terms of Service</a> apply.
      </p>

      <local-hidden :value="stripeToken" name="stripeToken" />
      <local-hidden :value="recaptchaToken" name="recaptchaToken" />
      <hidden name="amount" :store-module="storeModule" />
      <hidden name="level" :store-module="storeModule" />
      <hidden name="installment_period" :store-module="storeModule" />
      <hidden name="description" :store-module="storeModule" />
      <hidden name="campaign_id" :store-module="storeModule" />
      <hidden name="referral_id" :store-module="storeModule" />
      <hidden name="pay_fees_value" :store-module="storeModule" />
    </div>
  </form>
</template>

<script>
import Hidden from '../../connected-elements/Hidden.vue';
import PayFees from '../../connected-elements/PayFees.vue';
import TextInput from '../../connected-elements/TextInput.vue';
import FormBuckets from '../../connected-elements/FormBuckets.vue';
import ManualPay from '../../payment-elements/ManualPay.vue';
import ManualSubmit from '../../payment-elements/ManualSubmit.vue';
import NativePay from '../../payment-elements/NativePay.vue';
import LocalHidden from '../../local-elements/Hidden.vue';
import formStarter from '../../mixins/connected-form/starter';
import { BLAST_LEVELS } from './constants';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    PayFees,
    ManualPay,
    ManualSubmit,
    NativePay,
    FormBuckets,
  },

  mixins: [formStarter],

  data() {
    return {
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      storeModule: 'blastForm',
      allLevels: BLAST_LEVELS,
    };
  },
};
</script>

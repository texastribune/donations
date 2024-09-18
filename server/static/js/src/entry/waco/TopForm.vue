<template>
  <form
    ref="form"
    action="/donate"
    method="post"
    class="form"
    @submit="$event.preventDefault()"
  >
    <div v-if="serverErrorMessage" class="grid_row grid_separator">
      <div class="col">
        <p class="form__error form__error--prominent">
          {{ serverErrorMessage }}
        </p>
      </div>
    </div>

    <div class="grid_row">
      <div class="col">
        <radios
          :options="frequencyOptions"
          :store-module="storeModule"
          base-classes="form__radios form__radios--stack-at-medium"
          name="installment_period"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s grid_separator grid_align--end grid_gap">
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :show-error="showErrors"
          :show-frequency="true"
          label-text="amount* ($)"
          base-classes="form__text form__text--heavy"
          name="amount"
          inputmode="decimal"
        />
      </div>

      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :show-error="showErrors"
          label-text="email address*"
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
          label-text="first name*"
          base-classes="form__text form__text--standard"
          name="first_name"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :show-error="showErrors"
          label-text="last name*"
          base-classes="form__text form__text--standard"
          name="last_name"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :required="false"
          :show-error="showErrors"
          label-text="I am giving because"
          base-classes="form__text form__text--standard"
          name="reason"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :store-module="storeModule"
          :required="false"
          :show-error="showErrors"
          label-text="zip code*"
          base-classes="form__text form__text--standard"
          name="zipcode"
          inputmode="numeric"
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
              value="Donate"
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
       By donating, you will receive member communications at the email address you provide.
    </p>

    <p class="subtext">
      This site is protected by reCAPTCHA and the Google
      <a href="https://policies.google.com/privacy">Privacy Policy</a> and
      <a href="https://policies.google.com/terms">Terms of Service</a> apply.
    </p>

    <local-hidden :value="stripeToken" name="stripeToken" />
    <local-hidden :value="recaptchaToken" name="recaptchaToken" />
    <hidden name="description" :store-module="storeModule" />
    <hidden name="campaign_id" :store-module="storeModule" />
    <hidden name="referral_id" :store-module="storeModule" />
    <hidden name="pay_fees_value" :store-module="storeModule" />
  </form>
</template>

<script>
import Hidden from '../../connected-elements/Hidden.vue';
import LocalHidden from '../../local-elements/Hidden.vue';
import Radios from '../../connected-elements/Radios.vue';
import PayFees from '../../connected-elements/PayFees.vue';
import TextInput from '../../connected-elements/TextInput.vue';
import updateValue from '../../connected-elements/mixins/update-value';
import ManualPay from '../../payment-elements/ManualPay.vue';
import ManualSubmit from '../../payment-elements/ManualSubmit.vue';
import NativePay from '../../payment-elements/NativePay.vue';
import formStarter from '../../mixins/connected-form/starter';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    Radios,
    PayFees,
    ManualPay,
    ManualSubmit,
    NativePay,
  },

  mixins: [formStarter, updateValue],

  data() {
    return {
      storeModule: 'baseForm',
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      frequencyOptions: [
        { id: 0, text: 'One-time donation', value: 'None' },
        { id: 1, text: 'Monthly donation', value: 'monthly' },
        { id: 2, text: 'Yearly donation', value: 'yearly' },
      ],
    };
  },
};
</script>

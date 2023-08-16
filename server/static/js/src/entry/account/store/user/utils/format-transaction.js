export default function formatTransaction({
  amount,
  date,
  period,
  payment_type: paymentType,
  credit_card: card,
  stripe_customer_id: stripeCustomerId,
  stripe_subscription_id: stripeSubscriptionId,
}) {
  const transaction = {
    amount,
    date,
    period,
    stripeCustomerId,
    stripeSubscriptionId,
  };

  if (paymentType && paymentType.toLowerCase() === 'credit card') {
    transaction.card = { brand: card.brand, last4: card.last4 };
  }

  return transaction;
}

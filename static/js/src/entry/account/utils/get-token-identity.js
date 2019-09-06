export default function getTokenIdentity(identities, tokenEmail) {
  const [goodIdentity] = identities.filter(({ email }) => email === tokenEmail);
  return goodIdentity;
}

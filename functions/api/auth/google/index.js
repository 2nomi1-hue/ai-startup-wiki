// Google OAuth 시작 — Google 로그인 페이지로 리다이렉트
export async function onRequestGet({ request, env }) {
  const redirectUri = new URL('/api/auth/google/callback', request.url).href;

  const params = new URLSearchParams({
    client_id: env.GOOGLE_CLIENT_ID,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'openid email profile',
    access_type: 'offline',
    prompt: 'select_account',
  });

  return Response.redirect(
    `https://accounts.google.com/o/oauth2/v2/auth?${params}`,
    302
  );
}

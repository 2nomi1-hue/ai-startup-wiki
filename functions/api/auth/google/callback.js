// Google OAuth 콜백 — code → token 교환 → 사용자 정보 → D1 저장
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const loginUrl = new URL('/login.html', request.url).href;

  if (!code) {
    return Response.redirect(loginUrl + '?error=oauth_failed', 302);
  }

  const redirectUri = new URL('/api/auth/google/callback', request.url).href;

  // authorization code → access token 교환 (함정 15: 같은 redirect_uri 필수)
  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      redirect_uri: redirectUri,
      grant_type: 'authorization_code',
    }),
  });

  if (!tokenRes.ok) {
    console.error('Token 교환 실패:', await tokenRes.text());
    return Response.redirect(loginUrl + '?error=token_failed', 302);
  }

  const { access_token } = await tokenRes.json();

  // access token으로 사용자 정보 가져오기
  const userRes = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
    headers: { 'Authorization': `Bearer ${access_token}` },
  });

  if (!userRes.ok) {
    return Response.redirect(loginUrl + '?error=userinfo_failed', 302);
  }

  const user = await userRes.json();

  // D1 users 테이블에 저장 (이미 있으면 무시)
  await env.DB.prepare(
    'INSERT OR IGNORE INTO users (email, auth_method) VALUES (?, ?)'
  ).bind(user.email, 'google_oauth').run();

  // 세션 쿠키 발급 후 홈으로 이동
  return new Response(null, {
    status: 302,
    headers: {
      'Location': '/',
      'Set-Cookie': `session_email=${encodeURIComponent(user.email)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=86400`,
    },
  });
}

// Magic Link 토큰 검증 함수
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const token = url.searchParams.get('token');
  const loginUrl = new URL('/login.html', request.url).href;

  if (!token) {
    return Response.redirect(loginUrl + '?error=invalid', 302);
  }

  // 토큰 조회 (미사용 토큰만)
  const row = await env.DB.prepare(
    'SELECT * FROM magic_link_tokens WHERE token = ? AND used = 0'
  ).bind(token).first();

  if (!row) {
    return Response.redirect(loginUrl + '?error=invalid', 302);
  }

  // 만료 시간 확인 (15분)
  if (new Date(row.expires_at) < new Date()) {
    return Response.redirect(loginUrl + '?error=expired', 302);
  }

  // 토큰 1회용 처리 — 재사용 차단
  await env.DB.prepare(
    'UPDATE magic_link_tokens SET used = 1 WHERE id = ?'
  ).bind(row.id).run();

  // 세션 쿠키 발급 후 홈으로 리다이렉트
  return new Response(null, {
    status: 302,
    headers: {
      'Location': '/',
      'Set-Cookie': `session_email=${encodeURIComponent(row.email)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=86400`,
    },
  });
}

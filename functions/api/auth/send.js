// Magic Link 이메일 발송 함수
export async function onRequestPost({ request, env }) {
  const { email } = await request.json();

  if (!email || !email.includes('@')) {
    return Response.json({ error: '유효한 이메일을 입력해주세요.' }, { status: 400 });
  }

  // 랜덤 토큰 생성
  const token = crypto.randomUUID().replace(/-/g, '') + crypto.randomUUID().replace(/-/g, '');
  // 15분 후 만료
  const expiresAt = new Date(Date.now() + 15 * 60 * 1000).toISOString();

  // users 테이블에 없으면 추가
  await env.DB.prepare(
    'INSERT OR IGNORE INTO users (email, auth_method) VALUES (?, ?)'
  ).bind(email, 'magic_link').run();

  // 기존 미사용 토큰 삭제 후 새 토큰 저장 (1회용 보장)
  await env.DB.prepare(
    'DELETE FROM magic_link_tokens WHERE email = ? AND used = 0'
  ).bind(email).run();

  await env.DB.prepare(
    'INSERT INTO magic_link_tokens (email, token, expires_at) VALUES (?, ?, ?)'
  ).bind(email, token, expiresAt).run();

  // Magic Link URL 생성
  const siteUrl = new URL(request.url).origin;
  const magicLink = `${siteUrl}/api/auth/verify?token=${token}`;

  // Resend로 이메일 발송
  const emailRes = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'onboarding@resend.dev',
      to: email,
      subject: '[AI 스타트업 위키] 로그인 링크',
      html: `
        <div style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px;">
          <h2 style="color:#e94560;">AI 스타트업 위키</h2>
          <p>아래 버튼을 클릭하면 바로 로그인됩니다.</p>
          <p style="color:#888;font-size:13px;">이 링크는 <strong>15분</strong> 후 만료되며 1회만 사용 가능합니다.</p>
          <a href="${magicLink}"
             style="display:inline-block;margin-top:16px;padding:12px 28px;background:#e94560;color:#fff;border-radius:6px;text-decoration:none;font-weight:bold;">
            로그인하기
          </a>
          <p style="margin-top:24px;color:#aaa;font-size:12px;">본인이 요청하지 않았다면 이 이메일을 무시하세요.</p>
        </div>
      `,
    }),
  });

  if (!emailRes.ok) {
    const err = await emailRes.text();
    console.error('Resend 오류:', err);
    return Response.json({ error: '이메일 발송에 실패했습니다.' }, { status: 500 });
  }

  return Response.json({ message: '이메일을 확인해주세요! (15분 내 클릭)' });
}

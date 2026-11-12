-- 004: AI кэш/шығын, реферал, Pro жазылым, рейтинг view-лары

CREATE TABLE ai_cache (
    id             bigserial PRIMARY KEY,
    subject_id     smallint NOT NULL REFERENCES subjects(id),
    question_hash  text NOT NULL,
    question_text  text NOT NULL,
    answer         text NOT NULL,
    sources        jsonb NOT NULL DEFAULT '[]'::jsonb,
    hits           int NOT NULL DEFAULT 0,
    created_at     timestamptz NOT NULL DEFAULT now(),
    UNIQUE (subject_id, question_hash)
);

CREATE TABLE ai_usage_log (
    id             bigserial PRIMARY KEY,
    user_id        bigint REFERENCES users(tg_id) ON DELETE SET NULL,
    kind           text NOT NULL,   -- teacher, explain, embed
    model          text,
    input_tokens   int NOT NULL DEFAULT 0,
    output_tokens  int NOT NULL DEFAULT 0,
    cached         boolean NOT NULL DEFAULT false,
    created_at     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_ai_usage_time ON ai_usage_log (created_at DESC);

CREATE TABLE ai_daily_usage (
    user_id  bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    day      date NOT NULL DEFAULT current_date,
    count    int NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, day)
);

CREATE TABLE daily_test_usage (
    user_id  bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    day      date NOT NULL DEFAULT current_date,
    count    int NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, day)
);

CREATE TABLE referrals (
    id           bigserial PRIMARY KEY,
    referrer_id  bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    referred_id  bigint NOT NULL UNIQUE REFERENCES users(tg_id) ON DELETE CASCADE,
    rewarded     boolean NOT NULL DEFAULT false,
    created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_referrals_referrer ON referrals (referrer_id);

CREATE TABLE subscriptions (
    id          bigserial PRIMARY KEY,
    user_id     bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    plan        text NOT NULL,   -- pro_1m, pro_3m, ...
    source      text NOT NULL DEFAULT 'payment',   -- payment, referral, admin
    starts_at   timestamptz NOT NULL DEFAULT now(),
    expires_at  timestamptz NOT NULL,
    status      text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled'))
);
CREATE INDEX idx_subscriptions_user ON subscriptions (user_id, expires_at DESC);

-- Kaspi: оқушы чек жібереді, админ қолмен растайды
CREATE TABLE payments (
    id               bigserial PRIMARY KEY,
    user_id          bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    plan             text NOT NULL,
    amount           int NOT NULL,
    provider         text NOT NULL DEFAULT 'kaspi',
    status           text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'rejected')),
    receipt_file_id  text,
    reviewed_by      bigint,
    created_at       timestamptz NOT NULL DEFAULT now(),
    reviewed_at      timestamptz
);
CREATE INDEX idx_payments_status ON payments (status, created_at);

-- Рейтинг
CREATE VIEW leaderboard_all AS
SELECT tg_id AS user_id, full_name, xp, rank() OVER (ORDER BY xp DESC) AS position
FROM users
WHERE NOT is_banned AND xp > 0;

CREATE VIEW leaderboard_weekly AS
SELECT u.tg_id AS user_id, u.full_name, SUM(e.amount)::int AS xp,
       rank() OVER (ORDER BY SUM(e.amount) DESC) AS position
FROM xp_events e
JOIN users u ON u.tg_id = e.user_id
WHERE e.created_at >= date_trunc('week', now()) AND NOT u.is_banned
GROUP BY u.tg_id, u.full_name;

CREATE VIEW leaderboard_monthly AS
SELECT u.tg_id AS user_id, u.full_name, SUM(e.amount)::int AS xp,
       rank() OVER (ORDER BY SUM(e.amount) DESC) AS position
FROM xp_events e
JOIN users u ON u.tg_id = e.user_id
WHERE e.created_at >= date_trunc('month', now()) AND NOT u.is_banned
GROUP BY u.tg_id, u.full_name;

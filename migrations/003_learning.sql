-- 003: оқу процесі (тест сессиялары, қателер, статистика, XP)

CREATE TABLE test_sessions (
    id           bigserial PRIMARY KEY,
    user_id      bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    subject_id   smallint NOT NULL REFERENCES subjects(id),
    topic_id     int REFERENCES topics(id) ON DELETE SET NULL,
    mode         text NOT NULL CHECK (mode IN ('topic', 'mixed', 'exam', 'mistakes')),
    total        int NOT NULL DEFAULT 0,
    score        int NOT NULL DEFAULT 0,
    started_at   timestamptz NOT NULL DEFAULT now(),
    finished_at  timestamptz
);
CREATE INDEX idx_sessions_user ON test_sessions (user_id, started_at DESC);

CREATE TABLE test_answers (
    id           bigserial PRIMARY KEY,
    session_id   bigint NOT NULL REFERENCES test_sessions(id) ON DELETE CASCADE,
    question_id  bigint NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    user_answer  jsonb,
    is_correct   boolean NOT NULL,
    time_spent   int,   -- секунд
    answered_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_answers_session ON test_answers (session_id);
CREATE INDEX idx_answers_question ON test_answers (question_id);

CREATE TABLE user_mistakes (
    user_id        bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    question_id    bigint NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    wrong_count    int NOT NULL DEFAULT 1,
    last_wrong_at  timestamptz NOT NULL DEFAULT now(),
    resolved       boolean NOT NULL DEFAULT false,
    PRIMARY KEY (user_id, question_id)
);
CREATE INDEX idx_mistakes_active ON user_mistakes (user_id) WHERE NOT resolved;

CREATE TABLE user_topic_stats (
    user_id     bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    topic_id    int NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    answered    int NOT NULL DEFAULT 0,
    correct     int NOT NULL DEFAULT 0,
    updated_at  timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, topic_id)
);

-- Апталық / айлық рейтинг үшін XP тарихы
CREATE TABLE xp_events (
    id          bigserial PRIMARY KEY,
    user_id     bigint NOT NULL REFERENCES users(tg_id) ON DELETE CASCADE,
    amount      int NOT NULL,
    reason      text NOT NULL,   -- test, daily, referral, ...
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_xp_events_time ON xp_events (created_at DESC, user_id);

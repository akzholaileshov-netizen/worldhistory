-- 001: негізгі кестелер (пәндер, тақырыптар, қолданушылар)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE subjects (
    id          smallserial PRIMARY KEY,
    code        text UNIQUE NOT NULL,
    name_kk     text NOT NULL,
    is_active   boolean NOT NULL DEFAULT true,
    sort_order  int NOT NULL DEFAULT 0,
    created_at  timestamptz NOT NULL DEFAULT now()
);

INSERT INTO subjects (code, name_kk, is_active, sort_order) VALUES
    ('world_history', 'Дүниежүзі тарихы', true, 1),
    ('kazakh_history', 'Қазақстан тарихы', false, 2);

CREATE TABLE topics (
    id          serial PRIMARY KEY,
    subject_id  smallint NOT NULL REFERENCES subjects(id),
    parent_id   int REFERENCES topics(id) ON DELETE CASCADE,
    name_kk     text NOT NULL,
    sort_order  int NOT NULL DEFAULT 0
);
CREATE INDEX idx_topics_subject ON topics (subject_id, parent_id, sort_order);

CREATE TABLE users (
    tg_id               bigint PRIMARY KEY,
    username            text,
    full_name           text NOT NULL DEFAULT '',
    grade               text,
    region              text,
    target_score        smallint,
    current_subject_id  smallint REFERENCES subjects(id),
    ref_code            text UNIQUE NOT NULL,
    referred_by         bigint REFERENCES users(tg_id),
    xp                  int NOT NULL DEFAULT 0,
    streak              int NOT NULL DEFAULT 0,
    best_streak         int NOT NULL DEFAULT 0,
    last_active         timestamptz NOT NULL DEFAULT now(),
    is_banned           boolean NOT NULL DEFAULT false,
    created_at          timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_users_xp ON users (xp DESC);
CREATE INDEX idx_users_referred_by ON users (referred_by);

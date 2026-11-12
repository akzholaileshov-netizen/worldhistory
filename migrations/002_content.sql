-- 002: контент (кітаптар, сұрақтар, дайын тесттер)

CREATE TABLE books (
    id          serial PRIMARY KEY,
    subject_id  smallint NOT NULL REFERENCES subjects(id),
    title       text NOT NULL,
    author      text,
    file_path   text,
    pages       int,
    is_pro      boolean NOT NULL DEFAULT false,
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_books_subject ON books (subject_id);

-- embedding өлшемі 768 (Gemini embedding-ді 768-ге қысып қолданамыз: арзанырақ және жылдамырақ)
CREATE TABLE book_chunks (
    id          bigserial PRIMARY KEY,
    book_id     int NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    topic_id    int REFERENCES topics(id) ON DELETE SET NULL,
    page_from   int,
    page_to     int,
    content     text NOT NULL,
    embedding   vector(768),
    fts         tsvector GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED
);
CREATE INDEX idx_chunks_book ON book_chunks (book_id);
CREATE INDEX idx_chunks_embedding ON book_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_chunks_fts ON book_chunks USING gin (fts);

-- type: single (бір жауап), multi (бірнеше жауап), open (нұсқасыз сұрақ-жауап)
CREATE TABLE questions (
    id           bigserial PRIMARY KEY,
    subject_id   smallint NOT NULL REFERENCES subjects(id),
    topic_id     int REFERENCES topics(id) ON DELETE SET NULL,
    type         text NOT NULL DEFAULT 'single' CHECK (type IN ('single', 'multi', 'open')),
    text         text NOT NULL,
    options      jsonb NOT NULL DEFAULT '[]'::jsonb,   -- ["A нұсқа", "B нұсқа", ...]
    correct      jsonb NOT NULL DEFAULT '[]'::jsonb,   -- дұрыс нұсқа индекстері [0] немесе [0, 2]
    answer_text  text,                                  -- open түрі үшін жауап
    difficulty   smallint NOT NULL DEFAULT 2 CHECK (difficulty BETWEEN 1 AND 3),
    explanation  text,                                  -- AI түсіндірмесі (бір рет жасалып кэштеледі)
    source       text,
    text_hash    text NOT NULL,
    is_active    boolean NOT NULL DEFAULT true,
    created_at   timestamptz NOT NULL DEFAULT now(),
    UNIQUE (subject_id, text_hash)
);
CREATE INDEX idx_questions_topic ON questions (subject_id, topic_id) WHERE is_active;

CREATE TABLE external_tests (
    id          serial PRIMARY KEY,
    subject_id  smallint NOT NULL REFERENCES subjects(id),
    topic_id    int REFERENCES topics(id) ON DELETE SET NULL,
    title       text NOT NULL,
    url         text NOT NULL,
    is_pro      boolean NOT NULL DEFAULT false,
    sort_order  int NOT NULL DEFAULT 0,
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_external_tests_subject ON external_tests (subject_id, topic_id, sort_order);

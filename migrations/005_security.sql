-- 005: қауіпсіздік. Supabase публичный API (anon/authenticated) арқылы дерекке қол жеткізуге тыйым.
-- Бот тікелей Postgres қосылымымен жұмыс істейді (RLS-ті айналып өтеді), сондықтан policy қажет емес.

DO $$
DECLARE t record;
BEGIN
    FOR t IN
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public' AND tablename <> 'schema_migrations'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t.tablename);
    END LOOP;
END $$;

ALTER VIEW leaderboard_all SET (security_invoker = true);
ALTER VIEW leaderboard_weekly SET (security_invoker = true);
ALTER VIEW leaderboard_monthly SET (security_invoker = true);

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
        REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
        REVOKE ALL ON ALL TABLES IN SCHEMA public FROM authenticated;
    END IF;
END $$;

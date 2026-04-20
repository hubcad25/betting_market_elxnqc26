-- Cleanup: Remove old region text column
ALTER TABLE public.ridings DROP COLUMN IF EXISTS region;

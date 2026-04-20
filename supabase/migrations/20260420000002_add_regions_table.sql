-- Create regions table
CREATE TABLE IF NOT EXISTS public.regions (
    id TEXT PRIMARY KEY, -- slug (ex: 'montreal-est')
    name TEXT NOT NULL,  -- label (ex: 'Montréal est')
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.regions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Regions are viewable by everyone" ON public.regions FOR SELECT USING (true);

-- Add region_id to ridings and prepare migration
ALTER TABLE public.ridings ADD COLUMN IF NOT EXISTS region_id TEXT REFERENCES public.regions(id);

-- Note: We keep 'region' text column temporarily to facilitate migration, 
-- we will drop it or rename it once data is moved.

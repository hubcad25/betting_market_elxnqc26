-- Create junction table for many-to-many relationship
CREATE TABLE IF NOT EXISTS public.riding_regions (
    riding_id TEXT REFERENCES public.ridings(id) ON DELETE CASCADE NOT NULL,
    region_id TEXT REFERENCES public.regions(id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (riding_id, region_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.riding_regions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Riding regions are viewable by everyone" ON public.riding_regions FOR SELECT USING (true);

-- Drop the old single region_id column from ridings
ALTER TABLE public.ridings DROP COLUMN IF EXISTS region_id;

-- Update historical results table to store full scores
ALTER TABLE public.riding_historical_results 
ADD COLUMN IF NOT EXISTS votes JSONB DEFAULT '{}'::jsonb;

-- Add Green Party if it doesn't exist
INSERT INTO public.parties (id, name, color)
VALUES ('PVQ', 'Parti Vert du Québec', '#3D9B35')
ON CONFLICT (id) DO NOTHING;

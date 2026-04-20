-- Refactor ridings table to be a fixed reference table
ALTER TABLE public.ridings DROP COLUMN IF EXISTS qc125_url;
ALTER TABLE public.ridings DROP COLUMN IF EXISTS current_projection;
ALTER TABLE public.ridings DROP COLUMN IF EXISTS last_election_result;
ALTER TABLE public.ridings DROP COLUMN IF EXISTS final_result;

ALTER TABLE public.ridings ADD COLUMN IF NOT EXISTS dgeq_code TEXT UNIQUE;
ALTER TABLE public.ridings ADD COLUMN IF NOT EXISTS qc125_id TEXT;
ALTER TABLE public.ridings ADD COLUMN IF NOT EXISTS poliwave_id TEXT;
ALTER TABLE public.ridings ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- Create table for historical results
CREATE TABLE IF NOT EXISTS public.riding_historical_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    riding_id TEXT REFERENCES public.ridings(id) ON DELETE CASCADE NOT NULL,
    election_year INTEGER NOT NULL,
    winning_party_id TEXT REFERENCES public.parties(id),
    margin_percent NUMERIC,
    turnout_percent NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(riding_id, election_year)
);

-- Create table for projections (Live/Volatile data)
CREATE TABLE IF NOT EXISTS public.riding_projections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    riding_id TEXT REFERENCES public.ridings(id) ON DELETE CASCADE NOT NULL,
    source TEXT NOT NULL, -- 'qc125', 'poliwave', 'bot_expert'
    projected_party_id TEXT REFERENCES public.parties(id),
    win_probability NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS on new tables
ALTER TABLE public.riding_historical_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.riding_projections ENABLE ROW LEVEL SECURITY;

-- RLS Policies for historical results
CREATE POLICY "Historical results are viewable by everyone" ON public.riding_historical_results
    FOR SELECT USING (true);

-- RLS Policies for projections
CREATE POLICY "Projections are viewable by everyone" ON public.riding_projections
    FOR SELECT USING (true);

-- Triggers for updated_at
CREATE TRIGGER update_riding_historical_results_updated_at 
    BEFORE UPDATE ON public.riding_historical_results 
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_riding_projections_updated_at 
    BEFORE UPDATE ON public.riding_projections 
    FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

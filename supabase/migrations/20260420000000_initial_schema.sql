-- Create custom types
CREATE TYPE user_type AS ENUM ('human', 'bot', 'system');
CREATE TYPE wildcard_status AS ENUM ('open', 'locked', 'resolved');

-- Create tables
CREATE TABLE public.parties (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    color TEXT,
    logo_url TEXT
);

CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users NOT NULL PRIMARY KEY,
    username TEXT UNIQUE,
    full_name TEXT,
    avatar_url TEXT,
    bio TEXT,
    user_type user_type DEFAULT 'human' NOT NULL,
    is_eligible_for_pot BOOLEAN DEFAULT TRUE NOT NULL,
    score INT DEFAULT 0 NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE public.ridings (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT,
    qc125_url TEXT,
    current_projection TEXT,
    last_election_result TEXT,
    final_result TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE public.predictions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    riding_id TEXT REFERENCES public.ridings(id) ON DELETE CASCADE NOT NULL,
    party_id TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, riding_id)
);

CREATE TABLE public.wildcards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    question TEXT NOT NULL,
    options JSONB NOT NULL,
    correct_answer TEXT,
    points_value INT DEFAULT 1 NOT NULL,
    status wildcard_status DEFAULT 'open' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE public.wildcard_responses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    wildcard_id UUID REFERENCES public.wildcards(id) ON DELETE CASCADE NOT NULL,
    answer TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, wildcard_id)
);

CREATE TABLE public.forum_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ridings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.parties ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wildcards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wildcard_responses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.forum_messages ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Profiles
CREATE POLICY "Public profiles are viewable by everyone" ON public.profiles
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Ridings
CREATE POLICY "Ridings are viewable by everyone" ON public.ridings
    FOR SELECT USING (true);

-- Parties
CREATE POLICY "Parties are viewable by everyone" ON public.parties
    FOR SELECT USING (true);

-- Predictions
CREATE POLICY "Predictions are viewable by everyone" ON public.predictions
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own predictions" ON public.predictions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own predictions" ON public.predictions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own predictions" ON public.predictions
    FOR DELETE USING (auth.uid() = user_id);

-- Wildcards
CREATE POLICY "Wildcards are viewable by everyone" ON public.wildcards
    FOR SELECT USING (true);

-- Wildcard Responses
CREATE POLICY "Wildcard responses are viewable by everyone" ON public.wildcard_responses
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own wildcard responses" ON public.wildcard_responses
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own wildcard responses" ON public.wildcard_responses
    FOR UPDATE USING (auth.uid() = user_id);

-- Forum Messages
CREATE POLICY "Forum messages are viewable by everyone" ON public.forum_messages
    FOR SELECT USING (true);

CREATE POLICY "Users can insert their own forum messages" ON public.forum_messages
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own forum messages" ON public.forum_messages
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own forum messages" ON public.forum_messages
    FOR DELETE USING (auth.uid() = user_id);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_ridings_updated_at BEFORE UPDATE ON public.ridings FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_predictions_updated_at BEFORE UPDATE ON public.predictions FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_wildcards_updated_at BEFORE UPDATE ON public.wildcards FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_wildcard_responses_updated_at BEFORE UPDATE ON public.wildcard_responses FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, avatar_url, full_name)
    VALUES (
        new.id,
        new.raw_user_meta_data->>'username',
        new.raw_user_meta_data->>'avatar_url',
        new.raw_user_meta_data->>'full_name'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

-- Seed initial parties
INSERT INTO public.parties (id, name, color) VALUES
('PQ', 'Parti Québécois', '#004C9D'),
('CAQ', 'Coalition Avenir Québec', '#00ADEF'),
('PLQ', 'Parti Libéral du Québec', '#ED1C24'),
('QS', 'Québec solidaire', '#FF5500'),
('PCQ', 'Parti conservateur du Québec', '#111111'),
('IND', 'Indépendant', '#808080');

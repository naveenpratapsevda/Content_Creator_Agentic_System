-- ═══════════════════════════════════════════════════════════════════════════════
-- SOVEREIGN CINEMA ENGINE - POSTGRESQL SCHEMA
-- Production-Grade Database Architecture
-- ═══════════════════════════════════════════════════════════════════════════════

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════════════════════════
-- PROJECTS TABLE - Core project tracking
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    description TEXT,
    
    -- Status tracking
    status TEXT NOT NULL DEFAULT 'research',
    -- Status values: 'research', 'script_review', 'approved', 'in_progress', 'completed', 'archived'
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    approved_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Quality metrics
    success_score INTEGER CHECK (success_score >= 0 AND success_score <= 100),
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    
    -- Financial tracking
    total_cost_usd DECIMAL(10, 2) DEFAULT 0.00,
    
    -- ChromaDB references
    chroma_research_id TEXT,
    chroma_memory_id TEXT,
    
    -- Metadata (flexible JSON storage)
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Soft delete
    deleted_at TIMESTAMPTZ,
    
    -- Indexes
    CHECK (status IN ('research', 'script_review', 'approved', 'in_progress', 'completed', 'archived'))
);

-- Indexes for fast queries
CREATE INDEX idx_projects_status ON projects(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
CREATE INDEX idx_projects_success_score ON projects(success_score DESC) WHERE success_score IS NOT NULL;
CREATE INDEX idx_projects_metadata ON projects USING GIN (metadata);

-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════════
-- SOURCES TABLE - Track content sources and their performance
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url TEXT UNIQUE NOT NULL,
    domain TEXT NOT NULL,
    title TEXT,
    
    -- Categorization
    category TEXT NOT NULL,
    -- Categories: 'news', 'youtube', 'blog', 'research_paper', 'social_media'
    
    subcategory TEXT,
    -- Examples: 'ai_news', 'tech_tutorial', 'entertainment', 'education'
    
    -- Performance metrics
    times_used INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5, 2) GENERATED ALWAYS AS (
        CASE 
            WHEN times_used > 0 THEN (success_count::DECIMAL / times_used * 100)
            ELSE 0
        END
    ) STORED,
    
    -- User feedback
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    user_notes TEXT,
    
    -- Timestamps
    first_used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CHECK (category IN ('news', 'youtube', 'blog', 'research_paper', 'social_media', 'other'))
);

-- Indexes
CREATE INDEX idx_sources_domain ON sources(domain);
CREATE INDEX idx_sources_category ON sources(category);
CREATE INDEX idx_sources_success_rate ON sources(success_rate DESC);
CREATE INDEX idx_sources_last_used ON sources(last_used_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- API_COSTS TABLE - Financial tracking for all API calls
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE api_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    
    -- Service identification
    service TEXT NOT NULL,
    -- Services: 'openai_gpt4o', 'openai_gpt4o_mini', 'openai_embedding', 'dalle3', 'elevenlabs', 'runway', etc.
    
    operation TEXT NOT NULL,
    -- Operations: 'research', 'script', 'storyboard', 'voice', 'image', 'video', 'embedding'
    
    -- Usage metrics
    tokens_used INTEGER,
    api_calls INTEGER DEFAULT 1,
    
    -- Cost tracking
    cost_usd DECIMAL(10, 4) NOT NULL,
    
    -- Timestamp
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Additional details
    details JSONB DEFAULT '{}'::jsonb
);

-- Indexes
CREATE INDEX idx_api_costs_project_id ON api_costs(project_id);
CREATE INDEX idx_api_costs_service ON api_costs(service);
CREATE INDEX idx_api_costs_created_at ON api_costs(created_at DESC);
CREATE INDEX idx_api_costs_operation ON api_costs(operation);

-- ═══════════════════════════════════════════════════════════════════════════════
-- USER_PREFERENCES TABLE - System settings and learned preferences
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE user_preferences (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    category TEXT NOT NULL,
    -- Categories: 'style', 'content', 'technical', 'financial', 'notification'
    
    description TEXT,
    
    -- Learning metadata
    confidence_score DECIMAL(3, 2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
    learned_from TEXT, -- 'manual', 'ai_inference', 'feedback_loop'
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_preferences_updated_at BEFORE UPDATE ON user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════════
-- PROJECT_SOURCES - Many-to-many relationship between projects and sources
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE project_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    
    -- Usage context
    usage_type TEXT NOT NULL,
    -- Types: 'primary_research', 'reference', 'inspiration', 'verification'
    
    contribution_score INTEGER CHECK (contribution_score >= 1 AND contribution_score <= 10),
    notes TEXT,
    
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(project_id, source_id)
);

CREATE INDEX idx_project_sources_project ON project_sources(project_id);
CREATE INDEX idx_project_sources_source ON project_sources(source_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- DAILY_INTELLIGENCE - Daily brief/suggestions from the agent
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE daily_intelligence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL UNIQUE,
    
    -- Intelligence content
    trending_topics JSONB NOT NULL DEFAULT '[]'::jsonb,
    -- Array of {topic, score, sources[]}
    
    suggested_ideas JSONB NOT NULL DEFAULT '[]'::jsonb,
    -- Array of {idea, viability_score, reasoning, chroma_id}
    
    news_summary JSONB NOT NULL DEFAULT '[]'::jsonb,
    -- Array of {title, source, url, relevance_score}
    
    -- Metadata
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    viewed BOOLEAN DEFAULT FALSE,
    viewed_at TIMESTAMPTZ,
    
    chroma_embedding_id TEXT
);

CREATE INDEX idx_daily_intelligence_date ON daily_intelligence(date DESC);
CREATE INDEX idx_daily_intelligence_viewed ON daily_intelligence(viewed);

-- ═══════════════════════════════════════════════════════════════════════════════
-- REVIEW_FEEDBACK - Post-project review responses
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE review_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- Review questions and answers
    qa_data JSONB NOT NULL,
    -- Structure: [{question: "", answer: "", sentiment: ""}]
    
    -- Extracted insights
    key_learnings JSONB DEFAULT '[]'::jsonb,
    style_preferences JSONB DEFAULT '{}'::jsonb,
    content_preferences JSONB DEFAULT '{}'::jsonb,
    
    -- Processing
    processed BOOLEAN DEFAULT FALSE,
    applied_to_memory BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_review_feedback_project ON review_feedback(project_id);
CREATE INDEX idx_review_feedback_processed ON review_feedback(processed);

-- ═══════════════════════════════════════════════════════════════════════════════
-- USEFUL VIEWS FOR DASHBOARD
-- ═══════════════════════════════════════════════════════════════════════════════

-- View: Project performance summary
CREATE OR REPLACE VIEW project_performance AS
SELECT 
    p.id,
    p.title,
    p.status,
    p.success_score,
    p.total_cost_usd,
    p.created_at,
    p.completed_at,
    COUNT(DISTINCT ps.source_id) as source_count,
    COALESCE(SUM(ac.cost_usd), 0) as calculated_cost
FROM projects p
LEFT JOIN project_sources ps ON p.id = ps.project_id
LEFT JOIN api_costs ac ON p.id = ac.project_id
WHERE p.deleted_at IS NULL
GROUP BY p.id;

-- View: Source performance leaderboard
CREATE OR REPLACE VIEW source_leaderboard AS
SELECT 
    s.id,
    s.domain,
    s.category,
    s.times_used,
    s.success_rate,
    s.user_rating,
    COUNT(DISTINCT ps.project_id) as project_count,
    AVG(p.success_score) as avg_project_success
FROM sources s
LEFT JOIN project_sources ps ON s.id = ps.source_id
LEFT JOIN projects p ON ps.project_id = p.id
GROUP BY s.id
ORDER BY s.success_rate DESC, s.times_used DESC;

-- View: Monthly cost analysis
CREATE OR REPLACE VIEW monthly_costs AS
SELECT 
    DATE_TRUNC('month', created_at) as month,
    service,
    operation,
    COUNT(*) as api_calls,
    SUM(tokens_used) as total_tokens,
    SUM(cost_usd) as total_cost
FROM api_costs
GROUP BY month, service, operation
ORDER BY month DESC, total_cost DESC;

-- ═══════════════════════════════════════════════════════════════════════════════
-- SEED DATA - Initial preferences
-- ═══════════════════════════════════════════════════════════════════════════════

INSERT INTO user_preferences (key, value, category, description, learned_from) VALUES
('operator_name', '"NAVEEN"', 'technical', 'System operator name', 'manual'),
('clearance_level', '"ALPHA"', 'technical', 'Access clearance level', 'manual'),
('default_style', '{"aesthetic": "minimalist", "color_scheme": "neon_green", "tone": "professional"}', 'style', 'Default visual style preferences', 'manual'),
('notification_settings', '{"daily_brief": true, "project_alerts": true, "cost_warnings": true}', 'notification', 'Notification preferences', 'manual'),
('cost_limits', '{"daily_usd": 50, "project_usd": 20, "alert_threshold": 0.8}', 'financial', 'Cost management settings', 'manual');

-- ═══════════════════════════════════════════════════════════════════════════════
-- MAINTENANCE FUNCTIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Function: Archive old projects
CREATE OR REPLACE FUNCTION archive_old_projects(days_threshold INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    archived_count INTEGER;
BEGIN
    UPDATE projects
    SET status = 'archived'
    WHERE status = 'completed'
    AND completed_at < NOW() - (days_threshold || ' days')::INTERVAL
    AND status != 'archived';
    
    GET DIAGNOSTICS archived_count = ROW_COUNT;
    RETURN archived_count;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate source success rate
CREATE OR REPLACE FUNCTION update_source_metrics(source_uuid UUID, project_success BOOLEAN)
RETURNS VOID AS $$
BEGIN
    UPDATE sources
    SET 
        times_used = times_used + 1,
        success_count = success_count + CASE WHEN project_success THEN 1 ELSE 0 END,
        last_used_at = NOW()
    WHERE id = source_uuid;
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════════════════════════
-- NOTES
-- ═══════════════════════════════════════════════════════════════════════════════

-- To create database:
-- createdb sovereign_cinema
-- psql -d sovereign_cinema -f database_schema.sql

-- To reset (CAREFUL - deletes all data):
-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;
-- Then run this file again
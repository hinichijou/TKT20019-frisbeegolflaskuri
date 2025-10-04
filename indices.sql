CREATE INDEX idx_user_rounds ON rounds (creator_id);
CREATE INDEX idx_round_participations ON participations (round_id);
CREATE INDEX idx_user_participations ON participations (participator_id);
CREATE INDEX idx_round_coursenames ON rounds (coursename);
CREATE INDEX idx_round_start_times ON rounds (start_time);
CREATE INDEX idx_user_results ON results (player_id);
CREATE INDEX idx_round_results ON results (round_id);
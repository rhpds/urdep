CREATE OR REPLACE FUNCTION urdep_propagate_subject_desired_state() RETURNS TRIGGER AS $$
  BEGIN
    UPDATE urdep_subject SET desired_state=NEW.desired_state WHERE uuid=NEW.uuid;
  END;
$$ LANGUAGE plpgsql;
